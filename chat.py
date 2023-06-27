
import config
import logging
# from typing import List
import pandas  as pd
import pandasai as pdai

# Initialize logging with the specified configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOGS_FILE),
        logging.StreamHandler(),
    ],
)
LOGGER = logging.getLogger(__name__)

# Load documents from the specified directory using a DirectoryLoader object
#loader = DirectoryLoader(config.FILE_DIR, glob='*.pdf')
#documents = loader.load()
#documents = st.file_uploader("**Upload Your PDF File**", type=["pdf"])

# split the text to chuncks of of size 1000
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# Split the documents into chunks of size 1000 using a CharacterTextSplitter object
#texts = text_splitter.split_documents(documents)

# Create a vector store from the chunks using an OpenAIEmbeddings object and a Chroma object
#embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
#docsearch = Chroma.from_documents(texts, embeddings)

# Define answer generation function
def answer(prompt: str, pai: pdai.PandasAI, df: pd.DataFrame):

    # Log a message indicating that the function has started
    LOGGER.info(f"Start answering based on prompt: {prompt}.")

    answer = pai.custom_run(df, prompt=prompt)

    # Log a message indicating the answer that was generated
    LOGGER.info(f"The returned answer is: {answer}")

    # Log a message indicating that the function has finished and return the answer.
    LOGGER.info(f"Answering module over.")
    return answer


