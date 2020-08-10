from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Table
from reportlab.lib.units import cm

# https://www.python-izm.com/third_party/pdf/repotlab/


def open_pdf(output, author="", title="", subject=""):
    pdf_canvas = canvas.Canvas(output)
    pdf_canvas.saveState()

    pdf_canvas.setAuthor(author)
    pdf_canvas.setTitle(title)
    pdf_canvas.setSubject(subject)

    # A4
    pdf_canvas.setPageSize((21.0 * cm, 29.7 * cm))

    # B5
    # pdf_canvas.setPageSize((18.2*cm, 25.7*cm))

    return pdf_canvas


def set_font(pdf_canvas, font_name, font_size):
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    pdf_canvas.setFont(font_name, font_size)


def close_pdf(pdf_canvas):
    pdf_canvas.restoreState()
    pdf_canvas.save()


def build_cells(questions):
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


def output_pdf(
    output,
    questions=["0+0="],
    theme="なし",
    page_title="ぱぱのさんすうもんだい",
    font_name="HeiseiKakuGo-W5",
):

    cells = build_cells(questions)

    pdf_canvas = open_pdf(output)
    set_font(pdf_canvas, font_name, 30)
    pdf_canvas.drawString(2 * cm, 26 * cm, page_title)

    set_font(pdf_canvas, font_name, 20)
    pdf_canvas.drawString(3 * cm, 25 * cm, "「=」のみぎがわに、ただしいすうじをかいてね")

    set_font(pdf_canvas, font_name, 20)
    pdf_canvas.drawString(5 * cm, 2 * cm, "かかったじかん＿＿＿＿ふん＿＿＿＿びょう")

    set_font(pdf_canvas, font_name, 12)
    pdf_canvas.drawString(5 * cm, 1 * cm, "テーマ「{}」".format(theme))

    table = Table(cells, colWidths=7 * cm, rowHeights=2 * cm)
    table.setStyle([("FONT", (0, 0), (-1, -1), font_name, 28)])
    w, h = table.wrapOn(pdf_canvas, 0, 0)
    table.drawOn(pdf_canvas, 3 * cm, 24 * cm - h)

    close_pdf(pdf_canvas)
