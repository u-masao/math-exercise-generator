from django.test import TestCase
from sheets.views import (
    QuestionAdditionSpecificAb,
    QuestionSubtractionSpecificAb,
    QuestionSpecificAns,
)


class QuestionAdditionSpecificAbTests(TestCase):
    def test_default_constructor(self):
        num_of_questions = 40
        question_generators = [
            QuestionAdditionSpecificAb,
            QuestionSubtractionSpecificAb,
            QuestionSpecificAns,
        ]
        for question_generator in question_generators:
            questions = question_generator(num_of_questions=num_of_questions)
            question_list, theme = questions.generate()
            self.assertTrue(isinstance(theme, str))
            self.assertTrue(isinstance(question_list, list))
            for question_str in question_list:
                self.assertTrue(isinstance(question_str, str))
                self.assertTrue("=" in question_str)

            self.assertEqual(len(question_list), num_of_questions)
