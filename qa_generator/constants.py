from enum import Enum


class QuestionType(Enum):
    MULTIPLE_CHOICE = "Multiple choice"
    TRUE_FALSE = "True/false"
    FILL_IN_THE_BLANK = "Fill in the blank"
    OPEN_ENDED = "Open-ended"


class DifficultyLevel(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
