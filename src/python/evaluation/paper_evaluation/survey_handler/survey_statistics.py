from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Dict, List


@dataclass
class Question:
    with_formatting_count: int = 0
    without_formatting_count: int = 0
    any_formatting_count: int = 0

    def get_total(self):
        return self.with_formatting_count + self.without_formatting_count + self.any_formatting_count


@unique
class SurveyJsonField(Enum):
    NUMBER = 'number'
    LEFT_FRAGMENT = 'left_fragment'
    RIGHT_FRAGMENT = 'right_fragment'

    BEFORE_FORMATTING = 'before_formatting'
    BOTH = 'both'

    QUESTIONS = 'questions'


@dataclass
class SurveyStatistics:
    questions: List[Question]

    def __init__(self, questions_json: List[Dict[str, Any]], results_json: List[Dict[str, int]]):
        self.questions = []
        for result_json in results_json:
            question_number = result_json[SurveyJsonField.NUMBER.value]
            question = self.__find_json_question(questions_json, question_number)
            if question[SurveyJsonField.LEFT_FRAGMENT.value] == SurveyJsonField.BEFORE_FORMATTING.value:
                without_formatting_count = result_json[SurveyJsonField.LEFT_FRAGMENT.value]
                with_formatting_count = result_json[SurveyJsonField.RIGHT_FRAGMENT.value]
            else:
                without_formatting_count = result_json[SurveyJsonField.RIGHT_FRAGMENT.value]
                with_formatting_count = result_json[SurveyJsonField.LEFT_FRAGMENT.value]
            any_formatting_count = result_json[SurveyJsonField.BOTH.value]
            self.questions.append(Question(with_formatting_count, without_formatting_count, any_formatting_count))

    @staticmethod
    def __find_json_question(questions_json: List[Dict[str, Any]], question_number: int) -> Dict[str, Any]:
        for question in questions_json:
            if question[SurveyJsonField.NUMBER.value] == question_number:
                return question
        raise ValueError(f'Did not find question {question_number}')

    def print_stat(self):
        if len(self.questions) == 0:
            print('No questions found')
            return
        print(f'total participants={self.questions[0].get_total()}')
        print('------before----after----any----')
        for index, question in enumerate(self.questions):
            print(f'{index + 1}.\t\t{question.without_formatting_count}\t\t{question.with_formatting_count}\t\t  '
                  f'{question.any_formatting_count}')
