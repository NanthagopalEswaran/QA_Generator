from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel


# Multiple choice question generation
class MultipleChoiceQuestion(BaseModel):
    """
    A multiple choice question.
    """

    question: str
    options: list[str]


multiple_choice_question_parser = PydanticOutputParser(pydantic_object=MultipleChoiceQuestion)


GENERATE_MULTIPLE_CHOICE_PROMPT = PromptTemplate(
    template="""Generate a multiple choice question with {no_choices} choices for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\n{format_instructions}""",
    input_variables=["passage", "no_choices"],
    partial_variables={
        "format_instructions": multiple_choice_question_parser.get_format_instructions()
    },
)


# Multiple choice question and answer generation
class MultipleChoiceQuestionAnswer(BaseModel):
    """
    A multiple choice question and its answer.
    """

    question: str
    options: list[str]
    answer: str


multiple_choice_question_answer_parser = PydanticOutputParser(
    pydantic_object=MultipleChoiceQuestionAnswer
)

GENERATE_MULTIPLE_CHOICE_QUESTION_ANSWER_PROMPT = PromptTemplate(
    template="""Generate a multiple choice question with {no_choices} choices and its answer for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\n{format_instructions}""",
    input_variables=["passage", "no_choices", "difficulty"],
    partial_variables={
        "format_instructions": multiple_choice_question_answer_parser.get_format_instructions()
    },
)


# True/false question generation
class TrueFalseQuestion(BaseModel):
    """
    A true/false question.
    """

    question: str


true_false_question_parser = PydanticOutputParser(pydantic_object=TrueFalseQuestion)

GENERATE_TRUE_FALSE_PROMPT = PromptTemplate(
    template="""Generate a true/false question for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\n{format_instructions}""",
    input_variables=["passage", "difficulty"],
    partial_variables={"format_instructions": true_false_question_parser.get_format_instructions()},
)


# True/false question and answer generation
class TrueFalseQuestionAnswer(BaseModel):
    """
    A true/false question and its answer.
    """

    question: str
    answer: bool


true_false_question_answer_parser = PydanticOutputParser(pydantic_object=TrueFalseQuestionAnswer)

GENERATE_TRUE_FALSE_QUESTION_ANSWER_PROMPT = PromptTemplate(
    template="""Generate a true/false question and its answer for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\n{format_instructions}""",
    input_variables=["passage", "difficulty"],
    partial_variables={
        "format_instructions": true_false_question_answer_parser.get_format_instructions()
    },
)


# Fill in the blank question generation
class FillInTheBlankQuestion(BaseModel):
    """
    A fill in the blank question.
    """

    question: str


fill_in_the_blank_question_parser = PydanticOutputParser(pydantic_object=FillInTheBlankQuestion)

GENERATE_FILL_IN_THE_BLANK_PROMPT = PromptTemplate(
    template="""Generate a fill in the blank question for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\nExample: The capital of France is __________.\n\n{format_instructions}""",
    input_variables=["passage", "difficulty"],
    partial_variables={
        "format_instructions": fill_in_the_blank_question_parser.get_format_instructions()
    },
)

# Fill in the blank question and answer generation


class FillInTheBlankQuestionAnswer(BaseModel):
    """
    A fill in the blank question and its answer.
    """

    question: str
    answer: str


fill_in_the_blank_question_answer_parser = PydanticOutputParser(
    pydantic_object=FillInTheBlankQuestionAnswer
)

GENERATE_FILL_IN_THE_BLANK_QUESTION_ANSWER_PROMPT = PromptTemplate(
    template="""Generate a fill in the blank question and its answer for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\nExample: The capital of France is __________.\n\n{format_instructions}""",
    input_variables=["passage", "difficulty"],
    partial_variables={
        "format_instructions": fill_in_the_blank_question_answer_parser.get_format_instructions()
    },
)

# Open-ended question generation


class OpenEndedQuestion(BaseModel):
    """
    An open-ended question.
    """

    question: str


open_ended_question_parser = PydanticOutputParser(pydantic_object=OpenEndedQuestion)

GENERATE_OPEN_ENDED_PROMPT = PromptTemplate(
    template="""Generate an open-ended question for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\n{format_instructions}""",
    input_variables=["passage", "difficulty"],
    partial_variables={"format_instructions": open_ended_question_parser.get_format_instructions()},
)

# Open-ended question and answer generation


class OpenEndedQuestionAnswer(BaseModel):
    """
    An open-ended question and its answer.
    """

    question: str
    answer: str


open_ended_question_answer_parser = PydanticOutputParser(pydantic_object=OpenEndedQuestionAnswer)

GENERATE_OPEN_ENDED_QUESTION_ANSWER_PROMPT = PromptTemplate(
    template="""Generate an open-ended question and its answer for the following passage: \n\n```{passage}```\n\nDifficulty Level: {difficulty}\n\n{format_instructions}""",
    input_variables=["passage", "difficulty"],
    partial_variables={
        "format_instructions": open_ended_question_answer_parser.get_format_instructions()
    },
)
