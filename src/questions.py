import click
from src.util import output_pdf
import random


def question_diff(max_number=10):
    name = "diff_under_10"
    theme = "0から{}のひきざん".format(max_number)
    questions = []
    while len(questions) < 20:
        a = random.randint(0, max_number)
        b = random.randint(0, a)
        op = "-"
        question = "{}{}{}=".format(a, op, b)
        questions.append(question)
    return questions, theme, name


def question_ans(max_number=10, width=0):
    name = "ans_{}".format(max_number)
    theme = "だいたい{}になるけいさん".format(max_number)
    questions = []
    while len(questions) < 20:
        ans = random.randint(max_number - width, max_number + width)
        b = random.randint(-ans, ans)
        a = ans - b
        question = "{}{:+}=".format(a, b)
        questions.append(question)
    return questions, theme, name


def question_add_one():
    name = "add_1_to_0-9"
    theme = "いちたすなにか"
    questions = []
    op = "+"
    for _ in range(20):
        question = "{}{}{}=".format(1, op, random.randint(0, 9))
        questions.append(question)
    return questions, theme, name


@click.command()
@click.argument("output_dir", type=click.Path(exists=True), default="reports")
def main(output_dir):

    for count in range(1, 11):
        questions, theme, name = question_add_one()
        output_pdf(
            "{}/{}_{:02d}.pdf".format(output_dir, name, count),
            questions,
            theme,
        )

    max_number = 10
    for count in range(1, 11):
        questions, theme, name = question_diff(max_number=max_number)
        output_pdf(
            "{}/{}_{:02d}.pdf".format(output_dir, name, count),
            questions,
            theme,
        )

    max_number = 5
    for count in range(1, 11):
        questions, theme, name = question_ans(max_number=max_number, width=1)
        output_pdf(
            "{}/{}_{:02d}.pdf".format(output_dir, name, count),
            questions,
            theme,
        )


if __name__ == "__main__":
    main()
