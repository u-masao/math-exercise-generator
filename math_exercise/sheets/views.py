import logging

from django.http import Http404, HttpResponse, HttpResponseServerError
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token

from .models import Question  # noqa: F401
from .question_sheet import QuestionSheet
from .questions import (
    QuestionAdditionIngenious,
    QuestionAdditionSpecificAb,
    QuestionDatetimeForward,
    QuestionDatetimeInterval,
    QuestionDivisionSpecificAbRange,
    QuestionDivisionSpecificAbRangeDivisible,
    QuestionMultiplicationBlankB,
    QuestionMultiplicationSequential,
    QuestionMultiplicationSpecificAbRange,
    QuestionSpecificAns,
    QuestionSubtractionBorrow,
    QuestionSubtractionSpecificAb,
    QuestionSubtractionSpecificAbRange,
)


@requires_csrf_token
def my_customized_server_error(request, template_name="500.html"):
    import sys

    from django.views import debug

    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)


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
    arg1,
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
    elif action == "addition_ingenious":
        return generate_sheet(
            QuestionAdditionIngenious,
            pages=pages,
            **dict(
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
    elif action == "division_specific_ab_range_divisible":
        return generate_sheet(
            QuestionDivisionSpecificAbRangeDivisible,
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
        arg1 = arg1 if arg1 is not None else 1
        return generate_sheet(
            QuestionDatetimeInterval,
            pages=pages,
            page_subtitle="「答え」に、正しい時間を書いてね",
            **dict(a_min=a_min, a_max=a_max, step_width=arg1),
        )
    elif action == "datetime_forward":
        arg1 = arg1 if arg1 is not None else 1
        return generate_sheet(
            QuestionDatetimeForward,
            pages=pages,
            page_subtitle="「答え」に、正しい時こくを書いてね",
            **dict(
                a_min=a_min,
                a_max=a_max,
                ans_min=ans_min,
                ans_max=ans_max,
                step_width=arg1,
            ),
        )
    else:
        raise Http404("No such action")
