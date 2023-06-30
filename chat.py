
import config
import logging
# from typing import List
import pandas  as pd
import pandasai as pdai
from pandasai.prompts.generate_python_code import GeneratePythonCodePrompt

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
def answer(prompt: str, pai: pdai.PandasAI, df: pd.DataFrame):

    # Log a message indicating that the function has started
    LOGGER.info(f"Start answering based on prompt: {prompt}.")

    answer = pai.custom_run(df, prompt=prompt)

    # Log a message indicating the answer that was generated
    LOGGER.info(f"The returned answer is: {answer}")

    # Log a message indicating that the function has finished and return the answer.
    LOGGER.info(f"Answering module over.")
    return answer


def get_prompt(prompt, data_frame, suffix="\n\nCode:\n"):
    instruction = GeneratePythonCodePrompt(
        prompt=prompt,
        df_head=data_frame.head(5),
        num_rows=data_frame.shape[0],
        num_columns=data_frame.shape[1],
    )
    
    return str(instruction) + str(prompt) + suffix

def randomize_df(df, add_nulls=False):
    df['NullCount'] = df.isnull().sum(axis=1)
    df_sorted = df.sort_values('NullCount', ascending=True)

    df_final = df_sorted.drop('NullCount', axis=1)

    if add_nulls:
        # add a row of null values to top of the dataframe
        df_final = pd.concat([pd.Series([None for _ in range(df_final.shape[1])], index=df_final.columns), df_final]).reset_index(drop=True)

    return df_final