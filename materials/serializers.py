from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import Payment, User


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description']



class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'lessons']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'user', 'payments']