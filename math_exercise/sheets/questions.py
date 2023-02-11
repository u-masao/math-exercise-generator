import logging
import random

from .models import Question  # noqa: F401


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
        arg1=1,
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
        self.arg1 = arg1
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


class QuestionSubtractionDecimalBorrow(QuestionInterface):
    def generate(self):
        theme = f"ひきざん（くりさがりあり {self.a_max:0.1f} までのかず ）"

        formula_format = "{:0.1f}-{:0.1f}＝"
        questions = []
        answer_list = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(max(self.a_min, 0), self.a_max)
            question_b = random.randint(max(self.a_min, 0), self.a_max)

            if question_a == question_b:
                continue

            if abs(question_b) > abs(question_a):
                temp_value = question_a
                question_a = question_b
                question_b = temp_value

            question = self._format_question(
                question_a / 10.0,
                question_b / 10.0,
                question_format=formula_format,
            )
            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{(question_a - question_b)/10.0:0.1f}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionSubtractionBorrow(QuestionInterface):
    def generate(self):
        logger = logging.getLogger(__name__)
        theme = f"ひきざん（くりさがりあり {self.a_max} までのかず ）"

        questions = []
        answer_list = []

        while len(questions) < self.num_of_questions:
            if self.a_min and self.a_max:
                question_a = random.randint(self.a_min, self.a_max)
            if question_a % 10 > 8:
                continue
            question_b = -random.randint(question_a % 10 + 1, 9)
            question = self._format_question(question_a, question_b)

            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{question_a + question_b}")
        logger.debug(f"questions: {questions}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionSubtractionSpecificAbRange(QuestionInterface):
    def generate(self):
        theme = f"ひきざん（くりさがりなし {self.a_max} までのかず ）"

        questions = []
        answer_list = []
        while len(questions) < self.num_of_questions:
            if self.a_min and self.a_max:
                question_a = random.randint(self.a_min, self.a_max)
            if question_a % 10 < 3:
                continue
            question_b = -random.randint(1, question_a % 10)
            question = self._format_question(question_a, question_b)
            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{question_a + question_b}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


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
        answer_list = []
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
            answer_list.append(f"{question}{question_a + question_b}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionSpecificAns(QuestionInterface):
    def generate(self):
        # todo: 入力エラー処理

        if not self.subtraction:
            theme = "たしざん（こたえが{}から{}になるけいさん）".format(self.ans_min, self.ans_max)
        else:
            theme = "たしざんとひきざん（こたえが{}から{}になるけいさん）".format(self.ans_min, self.ans_max)

        questions = []
        answer_list = []
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
            answer_list.append(f"{question}{question_a + question_b}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionAdditionDecimalSpecificAb(QuestionInterface):
    def generate(self):
        if not self.a and not self.b:
            theme = "たしざん（{:0.1f}から{:0.1f}までのかず）".format(
                self.ab_min / 10, self.ab_max / 10
            )
        elif self.a and self.b:
            theme = "たしざん（{:0.1f}たす{:0.1f}）".format(self.a / 10, self.b / 10)
        else:
            if self.a:
                theme = "たしざん（{:0.1f}たす{:0.1f}から{:0.1f}までのかず）".format(
                    self.a / 10, self.ab_min / 10, self.ab_max / 10
                )
            else:
                theme = "たしざん（{:0.1f}から{:0.1f}までのかずたす{:0.1f}）".format(
                    self.ab_min / 10, self.ab_max / 10, self.b / 10
                )

        formula_format = "{:0.1f}+{:0.1f}＝"
        questions = []
        answer_list = []
        for _ in range(self.num_of_questions):
            if self.a:
                question_a = self.a
            else:
                question_a = random.randint(self.ab_min, self.ab_max)

            if self.b:
                question_b = self.b
            else:
                question_b = random.randint(self.ab_min, self.ab_max)

            question = self._format_question(
                question_a / 10.0,
                question_b / 10.0,
                question_format=formula_format,
            )
            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{(question_a + question_b) / 10.0:0.1f}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


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
        answer_list = []
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
            answer_list.append(f"{question}{question_a + question_b}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionAdditionIngenious(QuestionInterface):
    def generate(self):
        logger = logging.getLogger(__name__)
        self.fontsize_question = 22
        theme = "たしざん（くふうした計算、{}から{}）".format(self.a_min * 200, self.a_max * 200)
        formula_format = "{}+{}＝"

        questions = []
        answer_list = []
        while len(questions) < self.num_of_questions:
            digit_100 = random.randint(self.a_min, self.a_max)
            digit_1 = random.randint(self.b_min, self.b_max)

            question_a, question_b = random.sample(
                [100 * digit_100 + digit_1, 100 * digit_100 - digit_1], 2
            )

            question = self._format_question(
                question_a, question_b, question_format=formula_format
            )
            logger.info(f"question: {question}")
            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{question_a + question_b}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


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
        answer_list = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(self.a_min, self.a_max)
            question_b = random.randint(self.b_min, self.b_max)

            question = self._format_question(
                question_a, question_b, question_format=formula_format
            )
            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{question_a * question_b}")

        logger.debug(f"questions: {len(questions)}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


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
        answers = None
        return questions, theme, answers


class QuestionDivisionSpecificAbRange(QuestionInterface):
    def generate(self):
        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}÷{}＝"
        theme = "わりざん（{}と{}までのかず）".format(self.a_max, self.b_max)

        questions = []
        answer_list = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(self.a_min, self.a_max)
            question_b = random.randint(self.b_min, self.b_max)

            question = self._format_question(
                question_a, question_b, question_format=formula_format
            )
            questions = self._append_question(questions, question)

            answer_list.append(
                f"{question}{question_a // question_b}" f"・・・{question_a%question_b}"
            )
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionDivisionUnDivisible(QuestionInterface):
    def generate(self):
        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}÷{}＝"
        theme = "わりざん（割り切れない{}までのかず）".format(self.ans_max)

        questions = []
        answer_list = []
        while len(questions) < self.num_of_questions:
            mod_number = random.randint(self.b_min, self.b_max)
            ans_b = random.randint(0, mod_number)
            if ans_b == 0:
                continue
            ans_a = random.randint(self.ans_min, self.ans_max)

            question = self._format_question(
                ans_a * mod_number + ans_b, mod_number, question_format=formula_format
            )
            questions = self._append_question(questions, question)

            answer_list.append(f"{question}{ans_a}・・・{ans_b}")
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionDivisionSpecificAbRangeDivisible(QuestionInterface):
    def generate(self):
        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}÷{}＝"
        theme = "わりざん（{}と{}までのかず）".format(self.a_max, self.b_max)

        questions = []
        answer_list = []
        while len(questions) < self.num_of_questions:
            question_a = random.randint(self.a_min, self.a_max)
            question_b = random.randint(self.b_min, self.b_max)
            question_a, question_b = random.sample([question_a, question_b], 2)

            question = self._format_question(
                question_a * question_b, question_a, question_format=formula_format
            )
            questions = self._append_question(questions, question)

            answer_list.append(
                f"{question}{question_a // question_b}" f"・・・{question_a%question_b}"
            )
        answers = " \n".join(answer_list)
        return questions, theme, answers


class QuestionMultiplicationSequential(QuestionInterface):
    def generate(self):

        self.num_of_questions = 24
        self.rows = 12
        self.cols = 2
        self.fontsize_question = 24
        formula_format = "{}×{}＝"
        theme = "かけざん（{}の段を順番に）".format(self.a)

        questions = []
        answer_list = []
        question_a = self.a
        while len(questions) < self.num_of_questions:
            i = len(questions)
            question_b = i % 9 + 1
            question = self._format_question(
                question_a, question_b, question_format=formula_format
            )
            questions = self._append_question(questions, question)
            answer_list.append(f"{question}{question_a * question_b}")
        answers = " \n".join(answer_list)

        return questions, theme, answers


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
        if self.step_width <= 0:
            raise ValueError("次の条件でパラメーターを設定してください: step_width > 0")

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

        answers = None
        return questions, theme, answers


class QuestionDatetimeForward(QuestionInterface):
    def generate(self):
        """
        params
        ======
        a_min, a_max,
        ans_min, ans_max,
        step_width

        """

        def am_or_pm(hour):
            return "午前" if (hour // 12) % 2 == 0 else "午後"

        self.num_of_questions = 10
        self.cols = 1
        self.rows = 10
        self.fontsize_question = 18
        theme = f"時刻と時間から時刻を求める（{self.step_width} 分毎）"

        a_min = self.a_min if self.a_min is not None else 0
        a_max = self.a_max if self.a_max is not None else 24

        if a_min > a_max:
            raise ValueError("次の条件でパラメーターを設定してください: a_min <= a_max")
        if self.step_width <= 0:
            raise ValueError("次の条件でパラメーターを設定してください: step_width > 0")

        questions = []
        while len(questions) < self.num_of_questions:

            from_hour = random.randrange(a_min, a_max, 1)
            from_min = random.randrange(0, 60, self.step_width)
            to_hour = random.randrange(self.ans_min, self.ans_max, 1)
            to_min = random.randrange(0, 60, self.step_width)
            from_sign = am_or_pm(from_hour)

            question = (
                f"{from_sign} {from_hour%12} 時 {from_min:02} 分から "
                f"{to_hour%12} 時間 {to_min:02} 分後の時刻は"
            )
            question += "\n" + " " * 65 + "答え" + "_" * 18
            questions = self._append_question(questions, question)

        answers = None
        return questions, theme, answers
