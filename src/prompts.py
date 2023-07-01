
from datetime import date

from pandasai.constants import END_CODE_TAG, START_CODE_TAG

from pandasai.prompts.base import Prompt

class CustomGenerateResponsePrompt(Prompt):
    """Prompt to generate the response to the question in a conversational way"""

    text: str = """
    Question: {question}
    Answer: {answer}

    Rewrite the answer to the question in a conversational way. ONLY use the information in the answer provided. If the question relies on visualization, respond with "Refer to the visualization generated on the right.".
    """

class CustomGeneratePythonCodePrompt(Prompt):
    """Prompt to generate Python code"""

    text: str = """
        Today is {today_date}.
        You are provided with a pandas dataframe (df) with {num_rows} rows and {num_columns} columns.
        This is the metadata of the dataframe:
        {df_head}.

        When asked about the data, your response should include a python code that describes the dataframe `df`. 
        Assume that columns may have None or NaN values. Make sure column names are case-sensitive match EXACTLY as they appear in the dataframe.
        Using the provided dataframe, df, return the python code and make sure to prefix the requested python code with {START_CODE_TAG} exactly and suffix the code with {END_CODE_TAG} exactly to get the answer to the following question:
        """  # noqa: E501

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            START_CODE_TAG=START_CODE_TAG,
            END_CODE_TAG=END_CODE_TAG,
            today_date=date.today()
        )

class CodeSummaryPrompt(Prompt):
    """Prompt to generate Python code"""
    # pylint: disable=too-few-public-methods

    text: str = """
        You are provided with {number_dataframes} dataframes that the user wants to analyze.

        This was the prompt:
        {prompt}

        You answered with the following code:
        {code}

        Generate a line-by-line explanation of the code you wrote in a way that a non-technical person can understand. You only have to explain what the 
        code lines do and nothing else.
    """

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )