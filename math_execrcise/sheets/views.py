from django.http import HttpResponse
from reportlab.pdfgen import canvas

def index(request):
    response = HttpResponse(content_type='application/pdf')
    response["Content-Disposition"] = 'inline; filename=sheet.pdf'

    pdf = canvas.Canvas(response)
    pdf.drawString(100,100,"Hello world")
    pdf.showPage()
    pdf.save()
    return response

