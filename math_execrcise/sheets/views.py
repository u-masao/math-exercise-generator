import random

from django.utils import timezone
from django.http import HttpResponse
from django.views import generic


from .models import Question  # noqa: F401
from .util import QuestionSheet


class QuestionInterface:
    def __init__(
        self,
        ans_min=0,
        ans_max=10,
        ab_min=0,
        ab_max=10,
        a=None,
        b=None,
        substruction=False,
        num_of_questions=20,
    ):

        self.ans_min = ans_min
        self.ans_max = ans_max
        self.ab_min = ab_min
        self.ab_max = ab_max
        self.a = a
        self.b = b
        self.substruction = substruction
        self.num_of_questions = num_of_questions

    def generate(self):
        pass


class IndexView(generic.ListView):
    model = Question
    template_name = "sheets/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["created"] = timezone.now()
        return context


def detail(request, action, pages):
    pass


def addition_specific_ab(request, pages, ab_min, ab_max, a, b):
    return generate_sheet(
        QuestionAdditionSpecificAb,
        pages=pages,
        **dict(a=a, b=b, ab_min=ab_min, ab_max=ab_max)
    )


def addition_specific_ans(
    request, pages, ab_min, ab_max, ans_min, ans_max, subtraction
):
    return generate_sheet(
        QuestionAdditionSpecificAns,
        pages=pages,
        **dict(
            ans_min=ans_min,
            ans_max=ans_max,
            ab_min=ab_min,
            ab_max=ab_max,
            subtraction=subtraction,
        )
    )


def substraction_specific_ab(request, pages, ab_min, ab_max, a, b):
    return generate_sheet(
        QuestionSubstractionSpecificAb,
        pages=pages,
        **dict(a=a, b=b, ab_min=ab_min, ab_max=ab_max)
    )


def generate_sheet(func, pages=10, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=sheet.pdf"

    sheets = QuestionSheet(response)
    for _ in range(pages):
        questions, theme = func(**kwargs).generate()
        sheets.draw(
            questions=questions, theme=theme,
        )
    sheets.close()

    return response


class QuestionSubstractionSpecificAb(QuestionInterface):
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
            if self.a:
                question_a = self.a
            else:
                question_a = random.randint(0, self.ab_max)

            if self.b:
                question_b = -self.b
            else:
                question_b = -random.randint(0, question_a)
            question = "{}{:+}=".format(question_a, question_b)
            questions.append(question)
        return questions, theme


class QuestionAdditionSpecificAns(QuestionInterface):
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
            questions.append(question)
        return questions, theme


class QuestionAdditionSpecificAb(QuestionInterface):
    def generate(self):
        if not self.a and not self.b:
            theme = "たしざん（{}までのかず）".format(self.ab_max)
        elif self.a and self.b:
            theme = "たしざん（{}たす{}）".format(self.a, self.b)
        else:
            if self.a:
                theme = "たしざん（{}たす{}までのかず）".format(self.a, self.ab_max)
            else:
                theme = "たしざん（{}までのかずたす{}）".format(self.ab_max, self.b)

        questions = []
        for _ in range(self.num_of_questions):
            if self.a:
                question_a = self.a
            else:
                question_a = random.randint(0, self.ab_max)

            if self.b:
                question_b = self.b
            else:
                question_b = random.randint(0, self.ab_max)

            question = "{}+{}=".format(question_a, question_b)
            questions.append(question)
        return questions, theme
