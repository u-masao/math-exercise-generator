import random

from django.utils import timezone
from django.http import HttpResponse, Http404
from django.views import generic

from .models import Question  # noqa: F401
from .question_sheet import QuestionSheet

import logging


class QuestionInterface:
    def __init__(
        self,
        ans_min=0,
        ans_max=10,
        ab_min=0,
        ab_max=10,
        a=None,
        b=None,
        subtraction=False,
        num_of_questions=20,
        a_min=None,
        a_max=None,
        b_min=None,
        b_max=None,
    ):

        self.ans_min = ans_min
        self.ans_max = ans_max
        self.ab_min = ab_min
        self.ab_max = ab_max
        self.a = a
        self.b = b
        self.subtraction = subtraction
        self.num_of_questions = num_of_questions
        self.a_min = a_min
        self.a_max = a_max
        self.b_min = b_min
        self.b_max = b_max

    def generate(self):
        pass


class IndexView(generic.ListView):
    model = Question
    template_name = "sheets/index.html"

    def get_queryset(self):
        return Question.objects.order_by(*["level_text", "level_number"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["created"] = timezone.now()
        return context


def pdf(
    request,
    action,
    pages,
    ab_min,
    ab_max,
    ans_min,
    ans_max,
    a,
    b,
    a_min,
    a_max,
    b_min,
    b_max,
):

    if action == "addition_specific_ab":
        return generate_sheet(
            QuestionAdditionSpecificAb,
            pages=pages,
            **dict(
                a=a,
                b=b,
                ab_min=ab_min,
                ab_max=ab_max,
                ans_min=ans_min,
                ans_max=ans_max,
                a_min=a_min,
                a_max=a_max,
                b_min=b_min,
                b_max=b_max,
            ),
        )
    elif action == "specific_ans":
        return generate_sheet(
            QuestionSpecificAns,
            pages=pages,
            **dict(
                a=a,
                b=b,
                ab_min=ab_min,
                ab_max=ab_max,
                ans_min=ans_min,
                ans_max=ans_max,
                subtraction=False,
            ),
        )
    elif action == "subtraction_specific_ab":
        return generate_sheet(
            QuestionSubtractionSpecificAb,
            pages=pages,
            **dict(a=a, b=b, ab_min=ab_min, ab_max=ab_max),
        )
    elif action == "subtraction_specific_ab_range":
        return generate_sheet(
            QuestionSubtractionSpecificAbRange,
            pages=pages,
            **dict(a_min=a_min, a_max=a_max, b_min=b_min, b_max=b_max),
        )
    elif action == "subtraction_borrow":
        return generate_sheet(
            QuestionSubtractionBorrow,
            pages=pages,
            **dict(a_min=a_min, a_max=a_max),
        )
    else:
        raise Http404("No such action")


def generate_sheet(func, pages=10, **kwargs):
    logger = logging.getLogger(__name__)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=sheet.pdf"

    sheets = QuestionSheet(response)
    for _ in range(pages):
        questions, theme = func(**kwargs).generate()
        sheets.draw(
            questions=questions, theme=theme,
        )
        logger.debug(f"draw sheet: {questions} {theme}")
    sheets.close()

    return response


class QuestionSubtractionBorrow(QuestionInterface):
    def generate(self):
        logger = logging.getLogger(__name__)
        theme = f"ひきざん（くりさがりあり {self.a_max} までのかず ）"

        questions = []
        while len(questions) < self.num_of_questions:
            if self.a_min and self.a_max:
                question_a = random.randint(self.a_min, self.a_max)
            if question_a % 10 > 8:
                continue
            question_b = -random.randint(question_a % 10 + 1, 9)
            question = "{}{:+}=".format(question_a, question_b)

            if len(questions) < 2:
                questions.append(question)
            elif questions[-1] != question and questions[-2] != question:
                questions.append(question)
        logger.debug(f"questions: {questions}")
        return questions, theme


class QuestionSubtractionSpecificAbRange(QuestionInterface):
    def generate(self):
        theme = f"ひきざん（くりさがりなし {self.a_max} までのかず ）"

        questions = []
        while len(questions) < self.num_of_questions:
            if self.a_min and self.a_max:
                question_a = random.randint(self.a_min, self.a_max)
            if question_a % 10 < 3:
                continue
            question_b = -random.randint(1, question_a % 10)
            question = "{}{:+}=".format(question_a, question_b)
            if not questions:
                questions.append(question)
            elif questions[-1] != question:
                questions.append(question)
        return questions, theme


class QuestionSubtractionSpecificAb(QuestionInterface):
    def generate(self):
        if not self.a and not self.b:
            theme = "ひきざん（{}までのかず）".format(self.ab_max)
        elif self.a and self.b:
            theme = "ひきざん（{}ひく{}）".format(self.a, self.b)
        else:
            if self.a:
                theme = "ひきざん（{}ひく{}までのかず）".format(self.a, self.ab_max)
            else:
                theme = "ひきざん（{}までのかずひく{}）".format(self.ab_max, self.b)

        questions = []
        while len(questions) < self.num_of_questions:
            if self.a_min and self.a_max:
                question_a = random.randint(self.a_min, self.a_max)
            if self.b_min and self.b_max:
                question_b = random.randint(self.a_min, self.a_max)

            if self.a:
                question_a = self.a
            else:
                question_a = random.randint(self.ab_min, self.ab_max)

            if self.b:
                question_b = -self.b
            else:
                question_b = -random.randint(1, question_a)
            question = "{}{:+}=".format(question_a, question_b)
            if not questions:
                questions.append(question)
            elif questions[-1] != question:
                questions.append(question)
        return questions, theme


class QuestionSpecificAns(QuestionInterface):
    def generate(self):
        # todo: 入力エラー処理

        if not self.subtraction:
            theme = "たしざん（こたえが{}から{}になるけいさん）".format(
                self.ans_min, self.ans_max
            )
        else:
            theme = "たしざんとひきざん（こたえが{}から{}になるけいさん）".format(
                self.ans_min, self.ans_max
            )

        questions = []
        for _ in range(self.num_of_questions):
            question_ans = random.randint(self.ans_min, self.ans_max)
            if not self.subtraction:
                question_a = random.randint(0, question_ans)
                question_b = question_ans - question_a
            else:
                question_a = random.randint(question_ans, self.ab_max)
                question_b = question_ans - question_a

            question = "{}{:+}=".format(question_a, question_b)
            if not questions:
                questions.append(question)
            elif questions[-1] != question:
                questions.append(question)
        return questions, theme


class QuestionAdditionSpecificAb(QuestionInterface):
    def generate(self):
        if not self.a and not self.b:
            theme = "たしざん（{}から{}までのかず）".format(self.ab_min, self.ab_max)
        elif self.a and self.b:
            theme = "たしざん（{}たす{}）".format(self.a, self.b)
        else:
            if self.a:
                theme = "たしざん（{}たす{}から{}までのかず）".format(
                    self.a, self.ab_min, self.ab_max
                )
            else:
                theme = "たしざん（{}から{}までのかずたす{}）".format(
                    self.ab_min, self.ab_max, self.b
                )

        questions = []
        for _ in range(self.num_of_questions):
            if self.a:
                question_a = self.a
            else:
                question_a = random.randint(self.ab_min, self.ab_max)

            if self.b:
                question_b = self.b
            else:
                question_b = random.randint(self.ab_min, self.ab_max)

            question = "{}+{}=".format(question_a, question_b)
            if not questions:
                questions.append(question)
            elif questions[-1] != question:
                questions.append(question)
        return questions, theme