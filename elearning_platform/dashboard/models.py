from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser

User = get_user_model()

class TotalUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        students = User.objects.filter(role='student').count()
        instructors = User.objects.filter(role='instructor').count()
        return Response({
            "total_students": students,
            "total_instructors": instructors,
            "total_users": students + instructors
        })
