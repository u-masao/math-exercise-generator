from django.http import HttpResponse

import random
from .util import QuestionSheet


def index(request):
    # 一覧表示
    return generate_sheet(
        question_add_specific_ab, pages=5, **dict(max_number=20)
    )


def add_specific_ab(request, pages, ab_max, a, b):
    return generate_sheet(
        question_add_specific_ab,
        pages=pages,
        **dict(a=a, b=b, max_number=ab_max)
    )


def add_specific_ans(request, pages, ab_max, ans, width, subtraction):
    return generate_sheet(
        question_add_specific_ans,
        pages=pages,
        **dict(
            ans=ans, width=width, max_number=ab_max, subtraction=subtraction
        )
    )


def diff_specific_ab(request, pages, ab_max, a, b):
    return generate_sheet(
        question_diff_specific_ab,
        pages=pages,
        **dict(a=a, b=b, max_number=ab_max)
    )


def generate_sheet(func, pages=10, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=sheet.pdf"

    sheets = QuestionSheet(response)
    for _ in range(pages):
        questions, theme = func(**kwargs)
        sheets.draw(
            questions=questions, theme=theme,
        )
    sheets.close()

    return response


def question_diff_specific_ab(max_number=10, a=None, b=None):
    if not a and not b:
        theme = "ひきざん（{}までのかず）".format(max_number)
    elif a and b:
        theme = "ひきざん（{}ひく{}）".format(a, b)
    else:
        if a:
            theme = "ひきざん（{}ひく{}までのかず）".format(a, max_number)
        else:
            theme = "ひきざん（{}までのかずひく{}）".format(max_number, b)

    questions = []
    while len(questions) < 20:
        if a:
            question_a = a
        else:
            question_a = random.randint(0, max_number)

        if b:
            question_b = -b
        else:
            question_b = -random.randint(0, question_a)
        question = "{}{:+}=".format(question_a, question_b)
        questions.append(question)
    return questions, theme


def question_add_specific_ans(ans=10, width=0, max_number=20, subtraction=0):
    # todo: 入力エラー処理

    if not subtraction:
        theme = "たしざん（だいたい{}になるけいさん、はば{}）".format(ans, width)
    else:
        theme = "たしざんとひきざん（だいたい{}になるけいさん、はば{}）".format(ans, width)

    questions = []
    for _ in range(20):
        question_ans = random.randint(ans - width, ans + width)
        if not subtraction:
            question_a = random.randint(0, question_ans)
            question_b = question_ans - question_a
        else:
            question_a = random.randint(question_ans, max_number)
            question_b = question_ans - question_a

        question = "{}{:+}=".format(question_a, question_b)
        questions.append(question)
    return questions, theme


def question_add_specific_ab(a=None, b=None, max_number=10):
    if not a and not b:
        theme = "たしざん（{}までのかず）".format(max_number)
    elif a and b:
        theme = "たしざん（{}たす{}）".format(a, b)
    else:
        if a:
            theme = "たしざん（{}たす{}までのかず）".format(a, max_number)
        else:
            theme = "たしざん（{}までのかずたす{}）".format(max_number, b)

    questions = []
    for _ in range(20):
        if a:
            question_a = a
        else:
            question_a = random.randint(0, max_number)

        if b:
            question_b = b
        else:
            question_b = random.randint(0, max_number)

        question = "{}+{}=".format(question_a, question_b)
        questions.append(question)
    return questions, theme
