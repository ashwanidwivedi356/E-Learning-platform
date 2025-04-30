from celery import shared_task
from .models import PaymentHistory
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas

@shared_task
def generate_invoice_pdf(payment_id):
    payment = PaymentHistory.objects.get(id=payment_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Invoice for {payment.course.title}")
    p.drawString(100, 780, f"User: {payment.user.email}")
    p.drawString(100, 760, f"Amount: ${payment.amount}")
    p.drawString(100, 740, f"Status: {payment.status}")
    p.drawString(100, 720, f"Date: {payment.created_at}")
    p.showPage()
    p.save()

    pdf_file = ContentFile(buffer.getvalue())
    payment.invoice_pdf.save(f"invoice_{payment.id}.pdf", pdf_file)
    payment.save()
