import logging
import random

from django.http import Http404, HttpResponse, HttpResponseServerError
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token

from .models import Question  # noqa: F401
from .question_sheet import QuestionSheet


@requires_csrf_token
def my_customized_server_error(request, template_name="500.html"):
    import sys

    from django.views import debug

    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)


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
        step_width=1,
        style="formula",  # formura or sentence
        rows=10,
        cols=2,
        fontsize_question=28,
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
        self.step_width = step_width
        self.style = style
        self.rows = rows
        self.cols = cols
        self.fontsize_question = fontsize_question
        if self.style == "sentence":
            self.num_of_questions = 10
            self.rows = 10
            self.cols = 1
            self.fontsize_question = 18

    def generate(self):
        pass

    def _format_question(self, a, b, question_format="{}{:+}="):
        question_string = question_format.format(a, b)

        if self.style == "sentence":
            question_string = "つみきが "
            if b >= 0:
                question_string += f"{a} こ あります。{b} こ もらいました。"
            else:
                question_string += f"{a} こ あります。{abs(b)} こ あげました。"

            question_string += "いま なんこですか。"

        return question_string

    def _append_question(self, questions, question):
        if len(questions) < 2:
            questions.append(question)
        elif questions[-1] != question and questions[-2] != question:
            questions.append(question)
        return questions


class IndexView(generic.ListView):
    model = Question
    template_name = "sheets/index.html"

    def get_queryset(self):
        return Question.objects.order_by(
            *["-level_text", "-level_number", "-theme_text"]
        )

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
    style,
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
    elif action == "multiplication_specific_ab_range":
        return generate_sheet(
            QuestionMultiplicationSpecificAbRange,
            pages=pages,
            **dict(
                a_min=a_min,
                a_max=a_max,
                b_min=b_min,
                b_max=b_max,
            ),
        )
    elif action == "multiplication_blank_b":
        return generate_sheet(
            QuestionMultiplicationBlankB,
            pages=pages,
            page_subtitle="「=」のひだりがわに、ただしいすうじをかいてね",
            **dict(
                a_min=a_min,
                a_max=a_max,
                b_min=b_min,
                b_max=b_max,
            ),
        )
    elif action == "division_specific_ab_range":
        return generate_sheet(
            QuestionDivisionSpecificAbRange,
            pages=pages,
            **dict(
                a_min=a_min,
                a_max=a_max,
                b_min=b_min,
                b_max=b_max,
            ),
        )
    elif action == "multiplication_sequential":
        return generate_sheet(
            QuestionMultiplicationSequential,
            pages=pages,
            **dict(a=a),
        )
    elif action == "subtraction_borrow":
        return generate_sheet(
            QuestionSubtractionBorrow,
            pages=pages,
            **dict(a_min=a_min, a_max=a_max, style=style),
        )
    elif action == "datetime_interval":
        return generate_sheet(
            QuestionDatetimeInterval,
            pages=pages,
            page_subtitle="「答え」に、正しい時間を書いてね",
            **dict(a_min=a_min, a_max=a_max, step_width=10),
        )
    else:
        raise Http404("No such action")


def generate_sheet(func, pages=10, page_subtitle="「=」のみぎがわに、ただしいすうじをかいてね", **kwargs):
    logger = logging.getLogger(__name__)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=sheet.pdf"

    sheets = QuestionSheet(response)
    for _ in range(pages):
        generator = func(**kwargs)
        questions, theme = generator.generate()
        sheets.draw(
            questions=questions,
            theme=theme,
            rows=generator.rows,
            cols=generator.cols,
            fontsize_question=generator.fontsize_question,
            page_subtitle=page_subtitle,
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
            question = self._format_question(question_a, question_b)

            questions = self._append_question(questions, question)
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
            question = self._format_question(question_a, question_b)
            questions = self._append_question(questions, question)
        return questions, theme


class QuestionSubtractionSpecificAb(QuestionInterface):
    def generate(self):
        logging.basicConfig(level=logging.WARNING)
        logger = logging.getLogger(__name__)
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

            logger.debug(f"self.a: {self.a}")
            logger.debug(f"self.b: {self.b}")

            if self.a:
                question_a = self.a
            else:
                question_a = random.randint(self.ab_min, self.ab_max)

            logger.debug(f"question_a: {question_a}")

            if self.b:
                question_b = -self.b
            else:
                if question_a == 0:
                    continue
                question_b = -random.randint(1, question_a)
            question = self._format_question(question_a, question_b)
            questions = self._append_question(questions, question)
        return questions, theme


class QuestionSpecificAns(QuestionInterface):
    def generate(self):
        # todo: 入力エラー処理

        if not self.subtraction:
            theme = "たしざん（こたえが{}から{}になるけいさん）".format(self.ans_min, self.ans_max)
        else:
            theme = "たしざんとひきざん（こたえが{}から{}になるけいさん）".format(self.ans_min, self.ans_max)

        questions = []
        for _ in range(self.num_of_questions):
            question_ans = random.randint(self.ans_min, self.ans_max)
            if not self.subtraction:
                question_a = random.randint(0, question_ans)
                question_b = question_ans - question_a
            else:
                question_a = random.randint(question_ans, self.ab_max)
                question_b = question_ans - question_a

            question = self._format_question(question_a, question_b)
            questions = self._append_question(questions, question)
        return questions, theme


class QuestionAdditionSpecificAb(QuestionInterface):
    def generate(self):
        if not self.a and not self.b:
            theme = "たしざん（{}から{}までのかず）".format(self.ab_min, self.ab_max)
        elif self.a and self.b:
            theme = "たしざん（{}たす{}）".format(self.a, self.b)
        else:
            if self.a:
                theme = "たしざん（{}たす{}から{}までのかず）".format(self.a, self.ab_min, self.ab_max)
            else:
                theme = "たしざん（{}から{}までのかずたす{}）".format(self.ab_min, self.ab_max, self.b)

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

            question = self._format_question(question_a, question_b)
            questions = self._append_question(questions, question)
        return questions, theme


class QuestionMultiplicationSpecificAbRange(QuestionInterface):
    def generate(self):
        logger = logging.getLogger(__name__)

        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}×{}＝"
        theme = "かけざん（{}と{}までのかず）".format(self.a_max, self.b_max)

        questions = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(self.a_min, self.a_max)
            question_b = random.randint(self.b_min, self.b_max)
            question_a, question_b = random.sample([question_a, question_b], 2)

            question = self._format_question(
                question_a, question_b, question_format=formula_format
            )
            questions = self._append_question(questions, question)

        logger.debug(f"questions: {len(questions)}")
        return questions, theme


class QuestionMultiplicationBlankB(QuestionInterface):
    def generate(self):
        logger = logging.getLogger(__name__)

        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}×    ＝ {}"
        theme = "あなうめかけざん（{}と{}までのかず）".format(self.a_max, self.b_max)

        questions = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(self.a_min, self.a_max)
            question_b = random.randint(self.b_min, self.b_max)
            question_a, question_b = random.sample([question_a, question_b], 2)

            question = self._format_question(
                question_a, question_a * question_b, question_format=formula_format
            )
            questions = self._append_question(questions, question)

        logger.debug(f"questions: {len(questions)}")
        return questions, theme


class QuestionDivisionSpecificAbRange(QuestionInterface):
    def generate(self):
        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}÷{}＝"
        theme = "わりざん（{}と{}までのかず）".format(self.a_max, self.b_max)

        questions = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(self.a_min, self.a_max)
            question_b = random.randint(self.b_min, self.b_max)
            question_a, question_b = random.sample([question_a, question_b], 2)

            question = self._format_question(
                question_a * question_b, question_a, question_format=formula_format
            )
            questions = self._append_question(questions, question)

        return questions, theme


class QuestionMultiplicationSequential(QuestionInterface):
    def generate(self):

        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}×{}＝"
        theme = "かけざん（{}の段を順番に）".format(self.a)

        questions = []
        question_a = self.a
        while len(questions) < self.num_of_questions:
            i = len(questions)
            question_b = i % 9 + 1
            question = self._format_question(
                question_a, question_b, question_format=formula_format
            )
            questions = self._append_question(questions, question)

        return questions, theme


class QuestionDatetimeInterval(QuestionInterface):
    def generate(self):
        def am_or_pm(hour):
            return "午前" if (hour // 12) % 2 == 0 else "午後"

        self.num_of_questions = 10
        self.cols = 1
        self.rows = 10
        self.fontsize_question = 18
        theme = f"時刻と時刻から時間間隔を求める（{self.step_width} 分毎）"

        a_min = self.a_min if self.a_min is not None else 0
        a_max = self.a_max if self.a_max is not None else 24
        if a_min > a_max:
            raise ValueError("次の条件でパラメーターを設定してください: a_min <= a_max")

        questions = []
        while len(questions) < self.num_of_questions:

            from_hour = random.randrange(a_min, a_max, 1)
            from_min = random.randrange(0, 60, self.step_width)
            to_hour = random.randrange(from_hour, a_max, 1)
            to_min = random.randrange(0, 60, self.step_width)
            from_sign = am_or_pm(from_hour)
            to_sign = am_or_pm(to_hour)

            if from_hour * 60 + from_min >= to_hour * 60 + to_min:
                continue

            question = (
                f"{from_sign} {from_hour%12} 時 {from_min:02} 分から "
                f"{to_sign} {to_hour%12} 時 {to_min:02} 分まで"
            )
            question += "\n" + " " * 80 + "答え______________"
            questions = self._append_question(questions, question)

        return questions, theme
