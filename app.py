from chat import *
import streamlit as st
from streamlit_chat import message
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# import config

import pandas as pd
# from pandasai import PandasAI
from src.pandasai_custom import CustomPandasAI
from src.prompts import *
from src.sqlite import * 

from pandasai.llm.openai import OpenAI
from pandasai.middlewares.streamlit import StreamlitMiddleware


from pandasai.exceptions import NoCodeFoundError
from dotenv import load_dotenv
import sqlite3
import config

load_dotenv()

conn = sqlite3.connect('prompt_log.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS prompt_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT,
                    full_prompt TEXT,
                    answer TEXT,
                    code_executed TEXT,
                    code_generated TEXT,
                    error TEXT
                )''')
conn.commit()

st.set_page_config(layout="wide")
#Creating the chatbot interface
# st.title("Data Analytics Chatbot")
st.markdown("<h1 style='text-align: center;'>Mobius: Data Analytics</h1>", unsafe_allow_html=True)

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'code_executed' not in st.session_state:
    st.session_state['code_executed'] = []

if 'generated_code' not in st.session_state:
    st.session_state['generated_code'] = []

# Define a function to clear the input text
def clear_input_text():
    global input_text
    input_text = ""

# We will get the user's input by calling the get_text function
def get_text():
    global input_text
    input_text = st.text_input("Ask your Question", key="input", on_change=clear_input_text)
    return input_text


@st.cache_data
def parse_csv(file):
    return pd.read_csv(file)

# Define a function to parse a PDF file and extract its text content
@st.cache_data
def parse_xlsx(file) -> pd.DataFrame:
    return pd.read_excel(file)

def convert_document_to_dict(document):
    return {
        'page_content': document.page_content,
        'metadata': document.metadata,  # assuming this is already a dictionary
    }

def main():
    with st.container():
        col1, col2, _ = st.columns((25,50,25))

        with col2:
            user_input= get_text()
            uploaded_files = st.file_uploader("**Upload Your CSV/XLSX File**", type=['xlsx', 'csv'], accept_multiple_files=True)

    df = []

    if uploaded_files:
        if "df" not in st.session_state:
            file_extension = uploaded_files[0].name.split(".")[-1].lower()
            if file_extension == 'xlsx':
                for uploaded_file in uploaded_files:
                    df.append(parse_xlsx(uploaded_file))
            elif file_extension == 'csv':
                for uploaded_file in uploaded_files:
                    df.append(parse_csv(uploaded_file))
            else:
                st.error("Unsupported file type. Please upload a CSV or XLSX file.")

            st.session_state.df = df
            llm = OpenAI(temperature=0)
            custom_prompts = {
                "generate_python_code": CustomGeneratePythonCodePrompt,
                "generate_response": CustomGenerateResponsePrompt,
            }

            custom_whitelist = ['random', 'matplotlib', 'seaborn', 'pandas']
            st.session_state.pai = CustomPandasAI(llm=llm, conversational=True, enable_cache=False,
                                                  non_default_prompts=custom_prompts,
                                                  custom_whitelisted_dependencies=custom_whitelist)
        else:
            pai = st.session_state.pai
            df = st.session_state.df

            # Use DF randomization to generate better df.head() for context
            random_df = randomize_df(copy_dfs(df), add_nulls=True)
            # st.dataframe(random_df.head(5))
            # Generate answer by call to PandasAI
            answer = run_prompt(user_input, pai, random_df)
            
            # Store the output in session history
            st.session_state.past.append(user_input)
            st.session_state.generated.append(answer)
            
            # Ensure that code_executed is not empty
            if pai.last_code_executed:
                st.session_state.code_executed.append(pai.last_code_executed)
            else:
                st.session_state.code_executed.append("# No code executed")

            # Ensure that code_generated is not empty
            if pai.last_code_generated:
                st.session_state.generated_code.append(pai.last_code_generated)
            else:
                st.session_state.generated_code.append("# No code generated")
            
            full_prompt = get_prompt(user_input, df)
            log_prompt(conn, cursor, user_input, full_prompt, answer, pai.last_code_executed, 
                       pai.last_code_generated, pai.last_error)

        with st.container():
            col1, col2, _ = st.columns((25,50,25))
            with col2:
                if "df" in st.session_state:
                    # Display the centered DataFrame
                    for item in st.session_state.df:
                        st.dataframe(item, height=1)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.title("Chat")
            with col2:
                st.title("Code")

    st.markdown("""---""")

    with st.container():
        col1, col2 = st.columns(2, gap="large")

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                with col1:
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))
            with col2:
                #wrapped_string = textwrap.fill(item, width=50, break_long_words=True)

                # Grab last code generated
                code_generated = st.session_state.generated_code[-1]
                st.code(code_generated, language='python')
            
                df = copy_dfs(st.session_state.df)
                pai = st.session_state.pai
                try:
                    # Replace any plots with streamlit plots for display
                    rerun_code = StreamlitMiddleware()(code_generated)

                    # Not the most rigorous implementation of checking for charts, but it works
                    has_chart = rerun_code != "import streamlit as st\n" + code_generated
                    output, result, environment = pai.get_code_output(rerun_code, df, use_error_correction_framework=False, has_chart=has_chart)

                    if not has_chart:
                        if output:
                            st.code(output)
                        if result:
                            st.code(result)
                    
                    # If there is code, generate a code summary to explain what the code does
                    if code_generated:
                        last_prompt = st.session_state.past[-1]
                        code_summary = pai.generate_code_summary(len(df), last_prompt, code_generated) # Change
                        st.info(code_summary)

                    dfs_in_env = extract_dfs(environment)

                    if dfs_in_env:
                        option = st.selectbox(
                            'Add dataframe to sources',
                            dfs_in_env)

                except NoCodeFoundError:
                    print("No code")

# Run the app
if __name__ == "__main__":
    main()

conn.close()