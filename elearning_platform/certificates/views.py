from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from courses.models import Course
from .models import Certificate
from .tasks import generate_certificate

class CertificateGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=404)

        total_lectures = course.lecture_set.count()
        completed = request.user.completed_lectures.filter(course=course).count()

        if total_lectures == 0 or completed < total_lectures:
            return Response({"detail": "Complete all lectures to get certificate."}, status=400)

        cert, created = Certificate.objects.get_or_create(user=request.user, course=course)

        if created or not cert.pdf:
            generate_certificate.delay(
                user_id=request.user.id,
                course_id=course.id,
                username=request.user.get_full_name() or request.user.username,
                course_name=course.title
            )
            return Response({"message": "Certificate generation in progress. Check back soon."})

        return Response({"download_url": cert.pdf.url})
