import random
import click
from src.util import QuestionSheet


def question_diff_fix_a(a=10):
    theme = "ひきざん（{}からのひきざん）".format(a)
    questions = []
    while len(questions) < 20:
        b = random.randint(0, a)
        op = "-"
        question = "{}{}{}=".format(a, op, b)
        questions.append(question)
    return questions, theme


def question_diff(max_number=10):
    theme = "ひきざん（0から{}のかず）".format(max_number)
    questions = []
    while len(questions) < 20:
        a = random.randint(0, max_number)
        b = random.randint(0, a)
        op = "-"
        question = "{}{}{}=".format(a, op, b)
        questions.append(question)
    return questions, theme


def question_ans(max_number=10, width=0):
    theme = "だいたい{}になるけいさん（はば{}）".format(max_number, width)
    questions = []
    while len(questions) < 20:
        ans = random.randint(max_number - width, max_number + width)
        b = random.randint(-ans, ans)
        a = ans - b
        question = "{}{:+}=".format(a, b)
        questions.append(question)
    return questions, theme


def question_add(max_number=10):
    theme = "たしざん（{}までのかず）".format(max_number)
    questions = []
    op = "+"
    for _ in range(20):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)
        question = "{}{}{}=".format(a, op, b)
        questions.append(question)
    return questions, theme


def question_add_a(a=1, max_number=10):
    theme = "たしざん（{}たすなにか）".format(a)
    questions = []
    op = "+"
    for _ in range(20):
        question = "{}{}{}=".format(a, op, random.randint(0, max_number))
        questions.append(question)
    return questions, theme


@click.command()
@click.argument("output_dir", type=click.Path(exists=True), default="reports")
@click.option("--pages", default=30, help="PDFのページ数")
def main(output_dir, pages=30):

    generators = []

    # ひきざん
    for max_number in range(5, 20):
        generators.append(
            {"func": question_diff, "kwargs": dict(max_number=max_number)}
        )

    # ひきざん
    for a in range(5, 21):
        generators.append({"func": question_diff_fix_a, "kwargs": dict(a=a)})

    # たしざん
    for max_number in range(5, 21):
        generators.append(
            {"func": question_add, "kwargs": dict(max_number=max_number)},
        )

    # 決まった数を中心にしたたしざん
    for a in range(1, 11):
        generators.append({"func": question_add_a, "kwargs": dict(a=a)},)

    # 加算減算のミックス：だいたい決まった答えになる計算
    for max_number in range(5, 21, 5):  # こたえのかず
        for width in range(1, 6):  # ぶれはば
            generators.append(
                {
                    "func": question_ans,
                    "kwargs": dict(max_number=max_number, width=width),
                },
            )

    # PDF 出力
    for generator in generators:
        sheets = None
        for _ in range(pages):
            questions, theme = generator["func"](**generator["kwargs"])
            if sheets is None:
                sheets = QuestionSheet("{}/{}.pdf".format(output_dir, theme))
            sheets.draw(
                questions=questions, theme=theme,
            )
        sheets.close()


if __name__ == "__main__":
    main()
