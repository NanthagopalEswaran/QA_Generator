from typing import Any, Optional

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel

from .constants import QuestionType

general_qa_template = """Generate a {question_type} question based on the passage provided below.

Passage (seperated by 3 backticks):
```{passage}```

Instructions for Question Generation:
{question_specific_instructions}

Difficulty Level:
{difficulty}

Output Format Instructions:
{format_instructions}
"""


class BaseQuestion:
    """
    Base class to store all the prompts and parser related to question generation.
    """

    question_type: QuestionType

    class Output(BaseModel):
        """
        Output of the question generation.
        """

        question: str

    class OutputWithAnswer(BaseModel):
        """
        Output of the question generation with answer.
        """

        question: str
        answer: Any

    def __init__(self, question_type: str):
        """Create general question and answer generation prompts and parsers.

        Args:
            question_type (str): The type of question to generate.
        """

        self.output_parser = PydanticOutputParser(pydantic_object=BaseQuestion.Output)
        self.output_parser_with_answer = PydanticOutputParser(
            pydantic_object=BaseQuestion.OutputWithAnswer
        )
        self.generate_question_prompt = PromptTemplate(
            template=general_qa_template,
            input_variables=["passage", "difficulty"],
            partial_variables={
                "question_specific_instructions": "",
                "question_type": question_type,
                "format_instructions": self.output_parser.get_format_instructions(),
            },
        )
        self.generate_question_answer_prompt = PromptTemplate(
            template=general_qa_template,
            input_variables=["passage", "difficulty"],
            partial_variables={
                "question_specific_instructions": "",
                "question_type": question_type,
                "format_instructions": self.output_parser_with_answer.get_format_instructions(),
            },
        )

    def get_qa_prompt_and_parser(self, with_answer: bool = False):
        """
        Generate the prompt and parser for question and answer generation.

        Args:
            with_answer (bool): Whether to generate answer along with the question.

        Returns:
            tuple: A tuple containing the prompt and parser for qa generation.
        """

        if with_answer:
            return self.generate_question_answer_prompt, self.output_parser_with_answer
        else:
            return self.generate_question_prompt, self.output_parser


# True/false question generation
class TrueFalseQuestion(BaseQuestion):
    """
    A true/false question.
    """

    question_type = QuestionType.TRUE_FALSE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, question_type="true/false", **kwargs)


# Open-ended question generation
class OpenEndedQuestion(BaseQuestion):
    """
    An open-ended question.
    """

    question_type = QuestionType.OPEN_ENDED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, question_type="open-ended", **kwargs)


# Multiple choice question generation
class MultipleChoiceQuestion(BaseQuestion):
    """
    A multiple choice question.
    """

    question_type = QuestionType.MULTIPLE_CHOICE

    class Output(BaseModel):
        """
        Output of the multiple choice question generation.
        """

        question: str
        options: list[str]

    class OutputWithAnswer(BaseModel):
        """
        Output of the multiple choice question generation with answer.
        """

        question: str
        options: list[str]
        answer: Optional[str]

    def __init__(self):
        self.output_parser = PydanticOutputParser(pydantic_object=MultipleChoiceQuestion.Output)
        self.output_parser_with_answer = PydanticOutputParser(
            pydantic_object=MultipleChoiceQuestion.OutputWithAnswer
        )
        self.generate_question_prompt = PromptTemplate(
            template=general_qa_template,
            input_variables=["passage", "no_choices", "difficulty"],
            partial_variables={
                "question_type": "multiple choice",
                "question_specific_instructions": "No of Choices: {no_choices}",
                "format_instructions": self.output_parser.get_format_instructions(),
            },
        )

        self.generate_question_answer_prompt = PromptTemplate(
            template=general_qa_template,
            input_variables=["passage", "no_choices", "difficulty"],
            partial_variables={
                "question_type": "multiple choice",
                "question_specific_instructions": "No of Choices: {no_choices}",
                "format_instructions": self.output_parser_with_answer.get_format_instructions(),
            },
        )


def get_question_class(question_type: QuestionType, *args, **kwargs):
    """
    Get the question class based on the question type.

    Args:
        question_type (QuestionType): The type of question.

    Returns:
        BaseQuestion: The question class based on the question type.
    """

    if question_type == QuestionType.MULTIPLE_CHOICE:
        return MultipleChoiceQuestion(*args, **kwargs)
    elif question_type == QuestionType.TRUE_FALSE:
        return TrueFalseQuestion(*args, **kwargs)
    elif question_type == QuestionType.OPEN_ENDED:
        return OpenEndedQuestion(*args, **kwargs)
    else:
        raise ValueError("Invalid question type")
