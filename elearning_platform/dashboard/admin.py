from django.contrib import admin

from django.contrib import admin
from courses.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'price', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['category', 'level']

