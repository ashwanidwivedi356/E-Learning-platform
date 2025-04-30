# courses/urls.py

from django.urls import path
from .views import (
    CourseCreateView, CourseUpdateView, CourseDeleteView, 
    CourseListView, CourseDetailView
)
from .views import (
    CreateSectionView,
    CreateLectureView,
    CourseSectionListView,
    LectureCompleteView
)

from .views import CreateRazorpayOrder, VerifyRazorpayPayment
from .views import CourseDetailView, CreateReviewView, InstructorAnalyticsView
urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<slug:slug>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<slug:slug>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('sections/create/', CreateSectionView.as_view(), name='section-create'),
    path('lectures/create/', CreateLectureView.as_view(), name='lecture-create'),
    path('courses/<slug:slug>/sections/', CourseSectionListView.as_view(), name='section-list'),
    path('lectures/complete/<int:lecture_id>/', LectureCompleteView.as_view(), name='lecture-complete'),
    path('enroll/<int:course_id>/', CreateRazorpayOrder.as_view()),
    path('payment/verify/', VerifyRazorpayPayment.as_view()),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<slug:slug>/review/', CreateReviewView.as_view(), name='course-review'),
    path('instructor/analytics/', InstructorAnalyticsView.as_view(), name='instructor-analytics'),
]

