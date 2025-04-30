from celery import shared_task
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO
from .models import Certificate
from django.core.mail import EmailMessage
from datetime import datetime

@shared_task
def generate_certificate(user_id, course_id, username, course_name):
    from courses.models import Course
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 🎨 STYLED Certificate Design
    p.setStrokeColorRGB(0.2, 0.2, 0.2)
    p.setLineWidth(4)
    p.rect(50, 50, width - 100, height - 100)  # border

    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(width / 2, height - 2.2 * inch, "Certificate of Completion")

    p.setFont("Helvetica", 20)
    p.drawCentredString(width / 2, height - 3.2 * inch, "This is to certify that")

    p.setFont("Helvetica-Bold", 24)
    p.setFillColorRGB(0.1, 0.3, 0.5)
    p.drawCentredString(width / 2, height - 4.2 * inch, username)
    p.setFillColorRGB(0, 0, 0)

    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2, height - 5.2 * inch, "has successfully completed the course")

    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2, height - 6.2 * inch, course_name)

    # Date and Signature
    p.setFont("Helvetica", 14)
    p.drawString(80, 100, f"Date: {datetime.now().date()}")
    p.drawRightString(width - 80, 100, "Signature")

    # Finalize
    p.showPage()
    p.save()
    buffer.seek(0)

    # Save Certificate
    cert = Certificate(user=user, course=course)
    pdf_filename = f"{user.username}-{course.slug}-certificate.pdf"
    cert.pdf.save(pdf_filename, ContentFile(buffer.read()))
    cert.save()

    # 📧 Email the PDF certificate
    email = EmailMessage(
        subject="Your Course Completion Certificate",
        body=f"Hi {username},\n\nCongratulations on completing {course_name}!\nYour certificate is attached.",
        to=[user.email]
    )
    email.attach(pdf_filename, cert.pdf.read(), 'application/pdf')
    email.send()
