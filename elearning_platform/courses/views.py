from django.shortcuts import render

# Create your views here.
# courses/views.py

from rest_framework import generics, permissions, filters
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsInstructorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]

    def perform_create(self, serializer):
        # print("USER:", self.request.user)
        # print("ROLE:", self.request.user.role)
        serializer.save(instructor=self.request.user)

class CourseUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]
    lookup_field = 'slug'

class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]
    lookup_field = 'slug'

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'tags', 'category']
    filterset_fields = ['category', 'level']
    pagination_class = None  # Or use PageNumberPagination if needed

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'


from rest_framework import generics, permissions
from .models import Section, Lecture, LectureCompletion
from .serializers import SectionSerializer, LectureSerializer, LectureCompletionSerializer

class CreateSectionView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add instructor permission check

class CreateLectureView(generics.CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add instructor permission check

class CourseSectionListView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Section.objects.filter(course__slug=self.kwargs['slug'])

class LectureCompleteView(generics.CreateAPIView):
    serializer_class = LectureCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Course, Enrollment, PaymentHistory

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateRazorpayOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)

        if course.price == 0:
            Enrollment.objects.create(user=request.user, course=course, is_paid=False)
            return Response({"message": "Enrolled in free course."})

        amount_in_paise = int(course.price * 100)

        razorpay_order = razorpay_client.order.create(dict(
            amount=amount_in_paise,
            currency='INR',
            payment_capture='1'
        ))

        PaymentHistory.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            razorpay_order_id=razorpay_order['id']
        )

        return Response({
            "order_id": razorpay_order['id'],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount_in_paise,
            "currency": "INR",
        })


class VerifyRazorpayPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            payment = PaymentHistory.objects.get(razorpay_order_id=data['razorpay_order_id'])
            payment.razorpay_payment_id = data['razorpay_payment_id']
            payment.razorpay_signature = data['razorpay_signature']
            payment.status = 'paid'
            payment.save()

            Enrollment.objects.create(user=request.user, course=payment.course, is_paid=True)
            return Response({"message": "Payment verified and enrolled successfully."})
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Payment verification failed."}, status=400)



from rest_framework import generics, permissions
from .models import Course, Review
from .serializers import CourseSerializer, ReviewSerializer
from .permissions import IsEnrolledOrReadOnly
from rest_framework.exceptions import PermissionDenied

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledOrReadOnly]
    lookup_field = 'slug'


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course = generics.get_object_or_404(Course, slug=self.kwargs['slug'])
        if self.request.user not in course.students.all():
            raise PermissionDenied("You must be enrolled to review this course.")
        serializer.save(user=self.request.user, course=course)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum

class InstructorAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        courses = Course.objects.filter(instructor=user)
        total_enrollments = sum(course.students.count() for course in courses)
        total_revenue = sum(course.price * course.students.count() for course in courses)

        return Response({
            "total_courses": courses.count(),
            "total_enrollments": total_enrollments,
            "total_revenue": total_revenue
        })
