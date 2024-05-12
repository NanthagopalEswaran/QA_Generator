import os

import pytest
from delayed_assert import assert_expectations, expect

from qa_generator.constants import DifficultyLevel, QuestionType
from qa_generator.file_parser import File
from qa_generator.prompts import BaseQuestion, MultipleChoiceQuestion
from qa_generator.qa_generator import generate_questions

# Get all files under the sample_files directory
test_file_path = os.path.join(os.path.dirname(__file__), "sample_files", "python_syntax.pdf")


@pytest.mark.skip("Skip this test")
@pytest.mark.parametrize(
    "question_type",
    [QuestionType.OPEN_ENDED, QuestionType.TRUE_FALSE],
    ids=["open_ended", "true_false"],
)
@pytest.mark.parametrize("generate_answers", [True, False])
def test_qa_generation(generate_answers, question_type):
    """Test file parsing with all supported file formats."""

    try:
        test_file = File(test_file_path)
        results = generate_questions(
            file=test_file,
            num_questions=3,
            topics=None,
            question_type=question_type,
            num_options=0,
            difficulty=DifficultyLevel.EASY,
            generate_answers=generate_answers,
        )
        expect(len(results) != 0)
        expect(len(results) == 3, f"{len(results)} questions generated instead of 3")
        expect(
            isinstance(results[0], BaseQuestion.OutputWithAnswer)
            if generate_answers
            else isinstance(results[0], BaseQuestion.Output),
            "Answer Generation Check Failed",
        )
    except Exception as e:
        expect(False, f"Failed to generate questions: {e}")
    else:
        expect(True, "Successfully generated questions")

    assert_expectations()


@pytest.mark.skip("Skip this test")
@pytest.mark.parametrize("generate_answers", [True, False])
@pytest.mark.parametrize("num_options", [3, 4])
def test_qa_generation_multiple_choice(num_options, generate_answers):
    """Test file parsing with all supported file formats."""

    try:
        test_file = File(test_file_path)
        results = generate_questions(
            file=test_file,
            num_questions=3,
            topics=None,
            question_type=QuestionType.MULTIPLE_CHOICE,
            num_options=num_options,
            difficulty=DifficultyLevel.EASY,
            generate_answers=generate_answers,
        )
        expect(len(results) != 0, "No questions generated")
        expect(len(results) == 3, f"{len(results)} questions generated instead of 3")
        expect(
            isinstance(results[0], MultipleChoiceQuestion.OutputWithAnswer)
            if generate_answers
            else isinstance(results[0], MultipleChoiceQuestion.Output),
            "Answer Generation Check Failed",
        )
        expect(
            len(results[0].options) == num_options,
            f"{len(results[0].options)} options generated instead of {num_options}",
        )
    except Exception as e:
        expect(False, f"Failed to generate questions: {e}")
    else:
        expect(True, "Successfully generated questions")

    assert_expectations()


def test_about_content():
    """Test about content"""
    from qa_generator.about import about_content

    assert about_content


def test_invalid_question_type():
    """Test invalid question type"""
    with pytest.raises(ValueError):
        test_file = File(test_file_path)
        generate_questions(
            file=test_file,
            num_questions=3,
            topics=None,
            question_type="invalid",
            num_options=4,
            difficulty=DifficultyLevel.EASY,
            generate_answers=True,
        )
