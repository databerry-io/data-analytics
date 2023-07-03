import streamlit as st
from src.sqlite import retrieve_prompt_log
import sqlite3

st.set_page_config(layout="wide", page_title="Data Analytics: Prompt DB", page_icon="📝")

st.markdown("# Prompt Database")
# st.sidebar.header("")

conn = sqlite3.connect('prompt_log.db')
cursor = conn.cursor()

col1, col2, col3, col4, col5 = st.columns((3, 10, 10, 30, 8))
with col1:
    st.markdown("**ID**")
with col2:
    st.markdown("**Prompt**")
with col3:
    st.markdown("**Answer**")
with col4:
    st.markdown("**Code Executed**")
with col5:
    st.markdown("**Error**")

st.markdown("---")

for log in retrieve_prompt_log(cursor):
    id, prompt, full_prompt, answer, code_executed, code_generated, error = log

    col1, col2, col3, col4, col5 = st.columns((3, 10, 10, 30, 8))

    with col1:
        st.write(id)
    with col2: 
        st.write(prompt)
    with col3:
        st.write(answer)
    with col4:
        st.code(code_executed, language="python")
        st.code(code_generated, language="python")
    with col5:
        st.code(error, language="python")

    with st.expander("See full prompt"):
        st.code(full_prompt)

    st.markdown("---")

# if log_data:
#     st.header("Prompt Log")
#     st.table(log_data)
# else:
#     st.info("No prompt log entries found.")

conn.close()