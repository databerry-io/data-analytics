
import config
import logging
# from typing import List
import pandas  as pd
from src.pandasai_custom import CustomPandasAI
# from pandasai.prompts.generate_python_code import GeneratePythonCodePrompt
# from pandasai.prompts.multiple_dataframes import MultipleDataframesPrompt
# from typing import List
from copy import deepcopy
import streamlit as st

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

# Define answer generation function
def run_prompt(prompt: str, pai: CustomPandasAI, df: pd.DataFrame):

    # Log a message indicating that the function has started
    LOGGER.info(f"Start answering based on prompt: {prompt}.")

    answer = pai.custom_run(df, prompt=prompt)

    # Log a message indicating the answer that was generated
    LOGGER.info(f"The returned answer is: {answer}")

    # Log a message indicating that the function has finished and return the answer.
    LOGGER.info(f"Answering module over.")
    return answer


def get_prompt(prompt: str, data_frame: pd.DataFrame, suffix: str=""):
    if isinstance(data_frame, list):
        heads = [
            df.head()
            for df in data_frame
        ]
        instruction = config.MULTIPLE_PYTHON_CODE_PROMPT(heads)
    else:
        instruction = config.PYTHON_CODE_PROMPT(
            prompt=prompt,
            df_head=data_frame.head(5),
            num_rows=data_frame.shape[0],
            num_columns=data_frame.shape[1],
        )
    
    return str(instruction) + str(prompt) + suffix

def randomize_df(df: pd.DataFrame, add_nulls: bool = False):
    """
    Sort df to ensure better df.head() representation
    """
    def _helper_randomizer(df):
        df['NullCount'] = df.isnull().sum(axis=1)
        df_sorted = df.sort_values('NullCount', ascending=True)

        df_final = df_sorted.drop('NullCount', axis=1)

        if add_nulls:
            # add a row of null values to top of the dataframe
            new_row = pd.Series([None] * len(df_final.columns), index=df_final.columns)

            # Concatenate the new row and DataFrame vertically
            df_final = pd.concat([pd.DataFrame([new_row]), df_final])

            # Reset the index while preserving the sorted order
            df_final.reset_index(drop=True, inplace=True)

        return df_final
    if isinstance(df, list):
        return list(map(_helper_randomizer, df))
    
    return _helper_randomizer(df)

def extract_dfs(env: dict):
    dfs = []
    for key in env:
        if isinstance(env[key], pd.DataFrame):
            dfs.append(key)
    return dfs

def copy_dfs(dfs):
    return deepcopy(dfs)

@st.cache_data
def generate_code_summary(_pai: CustomPandasAI, df_len: int, prompt: str, code: str):
    return _pai.generate_code_summary(df_len, prompt, code)