import tempfile

import numpy as np
import qrcode
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  # noqa: F401
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

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
        cells = np.array(questions).reshape((-1, cols), order="F").tolist()
        return cells

    def _draw_string(
        self,
        text,
        x,
        y,
        size,
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
        page_subtitle="「=」のみぎがわにただしいこたえをかいてね",
        fontsize_question=28,
        answers=None,
    ):

        cells = self._build_cells(questions, rows=rows, cols=cols)

        self.pdf_canvas.setTitle(page_title)
        self._draw_string(page_title, x=2, y=26, size=30)
        self._draw_string(page_subtitle, x=3, y=25, size=18)
        self._draw_string(f"テーマ「{theme}」", x=8, y=3, size=12)
        self._draw_string("かかったじかん_______ふん______びょう", x=8, y=1.5, size=14)
        if answers is not None:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
            )
            qr.add_data(answers)
            qr.make(fit=True)
            qr_pillow = qr.make_image(fill_color="gray", back_color="white")

            qr_image = self._convert_to_image_reader(qr_pillow)

            self.pdf_canvas.drawImage(
                qr_image, x=2.5 * cm, y=0.5 * cm, width=3 * cm, height=3 * cm
            )

        table = Table(cells, colWidths=8 * cm, rowHeights=20.0 * cm / rows)
        table.setStyle(
            [
                (
                    "FONT",
                    (0, 0),
                    (-1, -1),
                    GEN_SHIN_GOTHIC_FONT_NAME,
                    fontsize_question,
                )
            ]
        )
        w, h = table.wrapOn(self.pdf_canvas, 0, 0)
        table.drawOn(self.pdf_canvas, 2 * cm, 24 * cm - h)

        self.pdf_canvas.showPage()

    def _convert_to_image_reader(self, qr_pillow):

        fo = tempfile.NamedTemporaryFile()
        qr_pillow.save(fo)
        fo.seek(0)
        qr_image = ImageReader(fo.name)
        fo.close()
        return qr_image
