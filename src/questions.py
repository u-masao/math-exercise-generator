import random
import click
from src.util import QuestionSheet


def question_diff(max_number=9):
    theme = "0から{}のひきざん".format(max_number)
    questions = []
    while len(questions) < 20:
        a = random.randint(0, max_number)
        b = random.randint(0, a)
        op = "-"
        question = "{}{}{}=".format(a, op, b)
        questions.append(question)
    return questions, theme


def question_ans(max_number=10, width=0):
    theme = "だいたい{}になるけいさん".format(max_number)
    questions = []
    while len(questions) < 20:
        ans = random.randint(max_number - width, max_number + width)
        b = random.randint(-ans, ans)
        a = ans - b
        question = "{}{:+}=".format(a, b)
        questions.append(question)
    return questions, theme


def question_add_a(a = 1, max_number=10):
    theme = "{}たすなにか".format(a)
    questions = []
    op = "+"
    for _ in range(20):
        question = "{}{}{}=".format(1, op, random.randint(0, max_number))
        questions.append(question)
    return questions, theme


@click.command()
@click.argument("output_dir", type=click.Path(exists=True), default="reports")
def main(output_dir):

    generators = [
        {"func": question_add_a, "kwargs": {a=1}},
        {"func": question_add_a, "kwargs": {a=5}},
        {"func": question_add_a, "kwargs": {a=3}},
        {"func": question_diff, "kwargs": {}},
        {"func": question_ans, "kwargs": {"max_number": 5, "width": 1}},
        {"func": question_ans, "kwargs": {"max_number": 10, "width": 1}},
    ]

    for generator in generators:
        sheets = None
        for _ in range(1, 31):
            questions, theme = generator["func"](**generator["kwargs"])
            if sheets is None:
                sheets = QuestionSheet("{}/{}.pdf".format(output_dir, theme))
            sheets.draw(
                questions=questions, theme=theme,
            )
        sheets.close()


if __name__ == "__main__":
    main()
