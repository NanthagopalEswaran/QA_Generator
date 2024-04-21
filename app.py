"""
This module contains the Question and Answer Generation App.

The app allows users to upload a PDF file, specify the number of questions to generate,
choose whether to generate answers as well, and provide focus keywords for question generation.
The app processes the PDF file, generates questions based on the text content, and displays
the generated questions along with their corresponding answers (if generated).

Example:
    $ streamlit run app.py

"""

import os

import streamlit as st
from openai import AuthenticationError
from pydantic.v1.error_wrappers import ValidationError

from qa_generator.about import about_content
from qa_generator.constants import DifficultyLevel, QuestionType
from qa_generator.file_parser import File
from qa_generator.qa_generator import generate_questions

curent_file_path = os.path.dirname(os.path.abspath(__file__))
os.environ["DATA_DIR"] = os.path.join(curent_file_path, ".data")
os.makedirs(os.environ["DATA_DIR"], exist_ok=True)

st.set_page_config(
    page_title="QA Generator",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/NanthagopalEswaran/QA_Generator/issues",
        "Get help": "https://huggingface.co/spaces/NandyG/QA_Generator/discussions",
        "About": about_content,
    },
)


def main():  # noqa: C901
    """
    Main function that runs the Question and Answer Generation App.
    """
    st.title("Question and Answer Generation App")

    uploaded_file = st.file_uploader(
        "Upload a File",
        accept_multiple_files=False,
        type=["pdf", "docx", "md", "txt", "rst"],
    )

    openai_api_key = st.text_input("OpenAI API Key", type="password")

    st.write("---")  # Add a separator

    num_questions = st.number_input("Number of questions to generate", min_value=1, value=10)

    question_type = QuestionType(
        st.selectbox(
            "Question type",
            [value.value for value in QuestionType if value != QuestionType.FILL_IN_THE_BLANK],
        )
    )

    num_options = 0

    if question_type:
        # Get no. of options for multiple choice questions
        if question_type == QuestionType.MULTIPLE_CHOICE:
            num_options = st.number_input(
                "Number of options for multiple choice questions",
                min_value=2,
                value=4,
            )

    # topics = st.text_input("Topics (comma-separated)").split(",")
    topics = []

    # Difficulty level
    difficulty = DifficultyLevel(
        st.selectbox(
            "Difficulty level",
            [value.value for value in DifficultyLevel],
        )
    )

    generate_answers = st.checkbox("Generate answers as well?")

    st.write("---")  # Add a separator

    if st.button("Generate", use_container_width=True):
        if uploaded_file is not None:
            with st.spinner("Processing the uploaded file..."):
                try:
                    file = File(uploaded_file)
                except Exception as e:
                    print(e)
                    st.error("Could not process the uploaded file. Try again or different file")
                    return
            with st.spinner("Generating questions..."):
                os.environ["OPENAI_API_KEY"] = openai_api_key
                try:
                    results = generate_questions(
                        file,
                        num_questions,
                        topics,
                        question_type,
                        num_options,
                        difficulty,
                        generate_answers,
                    )
                except ValidationError as err:
                    if "openai_api_key" in err.json():
                        st.error("Please provide an OpenAI API key.")
                        return
                    raise
                except AuthenticationError:
                    st.error("Invalid OpenAI API key.")
                    return
                except Exception as err:
                    st.error(
                        f"Unexpected error occured while generating questions. please try again. {err}"
                    )
                    return
            st.write("---")  # Add a separator
            st.header("Generated Questions")
            for i, result in enumerate(results):
                st.text(f"Q{i+1}")
                st.json(result.json(), expanded=True)
        else:
            st.error("Please upload a file.")


if __name__ == "__main__":
    main()
