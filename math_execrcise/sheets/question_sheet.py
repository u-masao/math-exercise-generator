from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  # noqa: F401
from reportlab.platypus import Table
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont

GEN_SHIN_GOTHIC_MEDIUM_TTF = "./sheets/fonts/GenShinGothic-P-Medium.ttf"
GEN_SHIN_GOTHIC_FONT_NAME = "GenShinGothic"


class QuestionSheet:
    def __init__(
        self,
        output,
        author="author",
        title="title",
        subject="subject",
        page_width_cm=21.0,
        page_height_cm=29.7,
    ):
        self.pdf_canvas = canvas.Canvas(output)
        self.pdf_canvas.setAuthor(author)
        self.pdf_canvas.setTitle(title)
        self.pdf_canvas.setSubject(subject)
        self.pdf_canvas.setPageSize((page_width_cm * cm, page_height_cm * cm))

    def set_fontsize(self, font_size):
        pdfmetrics.registerFont(
            TTFont(GEN_SHIN_GOTHIC_FONT_NAME, GEN_SHIN_GOTHIC_MEDIUM_TTF)
        )
        self.pdf_canvas.setFont(GEN_SHIN_GOTHIC_FONT_NAME, font_size)

    def close(self):
        self.pdf_canvas.save()

    def _build_cells(self, questions, rows=10, cols=2):
        cells = []
        index = 0
        for a in range(1, rows + 1):
            row = []
            for b in range(1, cols + 1):
                cell = questions[index]
                index = (1 + index) % len(questions)
                row.append(cell)
            cells.append(row)
        return cells

    def _draw_string(
        self, text, x, y, size,
    ):
        self.set_fontsize(size)
        self.pdf_canvas.drawString(x * cm, y * cm, text)

    def draw(
        self,
        questions=["0+0="],
        rows=10,
        cols=2,
        theme="なし",
        page_title="さんすうもんだいをやろう！",
        page_subtitle="「=」のみぎがわに、ただしいすうじをかいてね",
    ):

        cells = self._build_cells(questions, rows=rows, cols=cols)

        self.pdf_canvas.setTitle(page_title)
        self._draw_string(page_title, x=2, y=26, size=30)
        self._draw_string(page_subtitle, x=3, y=25, size=20)
        self._draw_string(f"テーマ「{theme}」", x=3, y=2, size=12)

        table = Table(cells, colWidths=8 * cm, rowHeights=2 * cm)
        table.setStyle(
            [("FONT", (0, 0), (-1, -1), GEN_SHIN_GOTHIC_FONT_NAME, 28)]
        )
        w, h = table.wrapOn(self.pdf_canvas, 0, 0)
        table.drawOn(self.pdf_canvas, 3 * cm, 24 * cm - h)

        self.pdf_canvas.showPage()
