from django.urls import path
from .views import CertificateGenerateView

urlpatterns = [
    path('certificate/<int:course_id>/', CertificateGenerateView.as_view(), name='generate-certificate'),
]
