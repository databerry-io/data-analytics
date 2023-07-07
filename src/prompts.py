
from datetime import date

from pandasai.constants import END_CODE_TAG, START_CODE_TAG

from pandasai.prompts.base import Prompt
import pandas as pd

class GraphCleaupPrompt(Prompt):
    text: str = """
You are modifying the python code below to ensure the following criteria are met:
- Make sure to sort all dataframes before graphing
- Use no more than 6 intervals on the x-axis
- Make sure to add a title, as well as labels for the x-axis and y-axis.

Steps to follow:
- Add only up to 3 lines of code
- Insert these lines of code into the code below in the right location
- Return the final code

Original Code:

"""
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )
        
class ColumnKeyErrorPrompt(Prompt):
    """Prompt to generate Python code"""

    text: str = """
You are provided with the following pandas dataframes metadata:"""

    def __init__(
        self,
        code: str,
        error_returned: Exception,
        question: str,
        df_head: list[pd.DataFrame],
    ):
        for i, dataframe in enumerate(df_head, start=1):
            row, col = dataframe.shape
            self.text += f"""
Dataframe df{i}, with {row} rows and {col} columns.
The column names and their respective data types for this dataframe are:
{dataframe.dtypes}
"""

        instruction: str = f"""
The user asked the following question:
{question}

You generated this python code:
{code}

It fails with a column key error, meaning you tried to access a column that does not exist. The error returned was:
{error_returned}

Correct the python code by accessing the column names EXACTLY as they appear with the column names above. Do not generate the same code again.
"""  # noqa: E501

        self.text += instruction

    def __str__(self):
        return self.text
    
class NullValuesErrorPrompt(Prompt):
    """Prompt to generate Python code"""

    text: str = """
You are provided with the following pandas dataframes metadata:"""

    def __init__(
        self,
        code: str,
        error_returned: Exception,
        question: str,
        df_head: list[pd.DataFrame],
    ):
        for i, dataframe in enumerate(df_head, start=1):
            row, col = dataframe.shape
            self.text += f"""
Dataframe df{i}, with {row} rows and {col} columns.
The column names and their respective data types for this dataframe are:
{dataframe.dtypes}
"""

        instruction: str = f"""
The user asked the following question:
{question}

You generated this python code:
{code}

It fails with a column key error, meaning you tried to access a column that does not exist. The error returned was:
{error_returned}

Correct the python code by accessing the column names EXACTLY as they appear with the column names above. Do not generate the same code again.
"""  # noqa: E501

        self.text += instruction

    def __str__(self):
        return self.text


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

""" Prompt to generate Python code for multiple dataframes """

class CustomMultipleDataframesPrompt(Prompt):
    """Prompt to generate Python code"""

    text: str = """
Today is {today_date}.
You are provided with the following pandas dataframes:"""
    instruction: str = """
Obey the following rules:
- Think step by step.
- Following the user’s requirements carefully and to the letter.
- Make sure to filter out null, None, and NaN values.
- Make sure column names are case-sensitive match EXACTLY as they appear in the dataframe.
- Make sure to prefix the requested python code with {START_CODE_TAG} exactly and suffix the code with {END_CODE_TAG}.
- If the question relies on visualization, respond with "Refer to the visualization.".
Using the provided dataframes and no other dataframes, return the python code to get the answer to the following question:
        """ 

    def __init__(self, dataframes: list[pd.DataFrame]):
        for i, dataframe in enumerate(dataframes, start=1):
            row, col = dataframe.shape

            self.text += f"""
Dataframe df{i}, with {row} rows and {col} columns. The data types of the dataframe columns are:
{dataframe.dtypes}

This is the metadata of the dataframe df{i}:
{dataframe}"""

        self.text += self.instruction
        self.text = self.text.format(
            today_date=date.today(),
            START_CODE_TAG=START_CODE_TAG,
            END_CODE_TAG=END_CODE_TAG,
        )

    def __str__(self):
        return self.text
