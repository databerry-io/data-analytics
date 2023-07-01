import streamlit as st
from src.sqlite import retrieve_prompt_log
import sqlite3

st.set_page_config(layout="wide", page_title="Data Analytics: Prompt DB", page_icon="📝")

st.markdown("# Prompt Database")
# st.sidebar.header("")

conn = sqlite3.connect('prompt_log.db')
cursor = conn.cursor()
log_data = retrieve_prompt_log(cursor)

if log_data:
    st.header("Prompt Log")
    st.table(log_data)
else:
    st.info("No prompt log entries found.")

conn.close()