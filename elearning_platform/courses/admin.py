from django.contrib import admin

# courses/admin.py


from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'price', 'level', 'created_at')
    list_filter = ('level', 'category', 'created_at')
    search_fields = ('title', 'tags', 'category')
    prepopulated_fields = {'slug': ('title',)}
