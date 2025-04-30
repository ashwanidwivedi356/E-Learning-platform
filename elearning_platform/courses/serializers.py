# courses/serializers.py

from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'instructor', 'instructor_name', 'title', 'slug', 
            'description', 'price', 'category', 'tags', 'level', 
            'thumbnail', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'instructor', 'created_at']


from rest_framework import serializers
from .models import Section, Lecture, LectureCompletion

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'course', 'lectures']

class LectureCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureCompletion
        fields = ['lecture']

from rest_framework import serializers
from .models import Course, Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'price', 'average_rating', 'reviews']

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
