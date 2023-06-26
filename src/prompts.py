
from datetime import date

from pandasai.constants import END_CODE_TAG, START_CODE_TAG

from pandasai.prompts.base import Prompt

class CustomGenerateResponsePrompt(Prompt):
    """Prompt to generate the response to the question in a conversational way"""

    text: str = """
    Question: {question}
    Answer: {answer}

    Rewrite the answer to the question in a conversational way. If the question relies on visualization, respond with "Refer to the visualization generated on the right.".
    """