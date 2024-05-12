"""
This module provides functionality for generating questions from extracted text.
"""

from langchain_openai import ChatOpenAI

from .constants import DifficultyLevel, QuestionType
from .file_parser import File
from .prompts import get_question_class


def generate_questions(
    file: File,
    num_questions: int,
    topics: list[str],
    question_type: QuestionType,
    num_options: int,
    difficulty: DifficultyLevel,
    generate_answers: bool,
):
    """
    Generate questions from the extracted text.

    Args:
        file (File): The file containing the extracted text.
        num_questions (int): The number of questions to generate.
        topics (list[str]): The topics to focus on when generating questions.
        question_type (str): The type of questions to generate.
        num_options (int): The number of options for multiple choice questions.
        difficulty (str): The difficulty level of the questions.
        generate_answers (bool): Whether to generate answers along with the questions.

    Returns:
        tuple: A tuple containing two lists - the generated questions and the generated answers (if generate_answers is True).
    """
    from random import choice

    results = []
    for _ in range(num_questions):
        passage = choice(file.documents).text
        result = generate_a_question_for_given_passage(
            passage, question_type, num_options, generate_answers, difficulty
        )
        results.append(result)

    return results


def generate_a_question_for_given_passage(
    passage, question_type, num_options, generate_answers, difficulty
):
    """
    Generate a question for the given passage.

    Args:
        passage (str): The passage for which to generate a question.
        question_type (str): The type of question to generate.
        num_options (int): The number of options for multiple choice questions.
        generate_answers (bool): Whether to generate answers along with the question.
        difficulty (str): The difficulty level of the question.

    Returns:
        str: The generated question.
    """

    model = ChatOpenAI(
        model_name="gpt-3.5-turbo-1106",
        temperature=0.4,
        response_format={"type": "json_object"},
    )

    # Get the prompt and parser for the given question type and whether to generate answers
    prompt, parser = generate_question_prompt_and_parser(question_type, generate_answers)

    # Generate the question using the prompt and parser (using openai)
    qa_chain = prompt | model | parser

    return None
    output = qa_chain.invoke(
        {"passage": passage, "no_choices": num_options, "difficulty": difficulty.value}
    )
    return output


def generate_question_prompt_and_parser(question_type: QuestionType, generate_answers: bool):
    """
    Get the prompt and parser for the given question type and whether to generate answers.

    Args:
        question_type (str): The type of questions to generate.
        generate_answers (bool): Whether to generate answers along with the questions.

    Returns:
        tuple: A tuple containing the prompt and parser for the given question type and whether to generate answers.
    """

    return get_question_class(question_type).get_qa_prompt_and_parser(with_answer=generate_answers)
