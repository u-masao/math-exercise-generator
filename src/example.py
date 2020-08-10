import click
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm

# https://www.python-izm.com/third_party/pdf/repotlab/


@click.command()
@click.argument("output", type=click.File("wb"))
def main(output):
    pdfFile = canvas.Canvas(output)
    pdfFile.saveState()

    pdfFile.setAuthor("トッケイラボ")
    pdfFile.setTitle("タイトル")
    pdfFile.setSubject("サンプル")

    # A4
    pdfFile.setPageSize((21.0 * cm, 29.7 * cm))
    # B5
    # pdfFile.setPageSize((18.2*cm, 25.7*cm))

    pdfFile.setFillColorRGB(0, 0, 100)
    pdfFile.rect(2 * cm, 2 * cm, 6 * cm, 6 * cm, stroke=1, fill=1)
    pdfFile.setFillColorRGB(0, 0, 0)

    pdfFile.setLineWidth(1)
    pdfFile.line(10 * cm, 20 * cm, 10 * cm, 10 * cm)

    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfFile.setFont("HeiseiKakuGo-W5", 12)
    pdfFile.drawString(5 * cm, 25 * cm, "はーひふーへほー")

    pdfFile.restoreState()
    pdfFile.save()


if __name__ == "__main__":
    main()
