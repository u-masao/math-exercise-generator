from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table


class QuestionSheet:
    def __init__(
        self, output, author="author", title="title", subject="subject"
    ):
        self.pdf_canvas = canvas.Canvas(output)
        self.pdf_canvas.setAuthor(author)
        self.pdf_canvas.setTitle(title)
        self.pdf_canvas.setSubject(subject)
        self.pdf_canvas.setPageSize((21.0 * cm, 29.7 * cm))

    def set_font(self, font_name, font_size):
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))
        self.pdf_canvas.setFont(font_name, font_size)

    def close(self):
        self.pdf_canvas.save()

    def build_cells(self, questions):
        cells = []
        index = 0
        for a in range(1, 11):
            row = []
            for b in range(1, 3):
                cell = questions[index]
                index = (1 + index) % len(questions)
                row.append(cell)
            cells.append(row)
        return cells

    def draw(
        self,
        questions=["0+0="],
        theme="なし",
        page_title="ぱぱのさんすうもんだい",
        font_name="HeiseiKakuGo-W5",
    ):

        cells = self.build_cells(questions)

        self.set_font(font_name, 30)
        self.pdf_canvas.drawString(2 * cm, 26 * cm, page_title)

        self.set_font(font_name, 20)
        self.pdf_canvas.drawString(3 * cm, 25 * cm, "「=」のみぎがわに、ただしいすうじをかいてね")

        self.set_font(font_name, 12)
        self.pdf_canvas.drawString(5 * cm, 1 * cm, "テーマ「{}」".format(theme))

        table = Table(cells, colWidths=7 * cm, rowHeights=2 * cm)
        table.setStyle([("FONT", (0, 0), (-1, -1), font_name, 28)])
        w, h = table.wrapOn(self.pdf_canvas, 0, 0)
        table.drawOn(self.pdf_canvas, 3 * cm, 24 * cm - h)

        self.pdf_canvas.showPage()
