
import config
import logging
# from typing import List
import pandas  as pd
import pandasai as pdai
from pandasai.prompts.generate_python_code import GeneratePythonCodePrompt
from pandasai.prompts.multiple_dataframes import MultipleDataframesPrompt
from typing import List, Union

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
def answer(prompt: str, pai: pdai.PandasAI, df: Union[pd.DataFrame, List[pd.DataFrame]]):

    # Log a message indicating that the function has started
    LOGGER.info(f"Start answering based on prompt: {prompt}.")

    answer = pai.custom_run(df, prompt=prompt)

    # Log a message indicating the answer that was generated
    LOGGER.info(f"The returned answer is: {answer}")

    # Log a message indicating that the function has finished and return the answer.
    LOGGER.info(f"Answering module over.")
    return answer


def get_prompt(prompt, data_frame, suffix="\n\nCode:\n", multiple=False):
    if multiple:
        heads = [
            dataframe.head()
            for dataframe in data_frame
        ]
        instruction = MultipleDataframesPrompt(heads)
    else:
        instruction = GeneratePythonCodePrompt(
            prompt=prompt,
            df_head=data_frame.head(5),
            num_rows=data_frame.shape[0],
            num_columns=data_frame.shape[1],
        )
    
    return str(instruction) + str(prompt) + suffix