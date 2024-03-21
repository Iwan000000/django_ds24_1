from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import Payment, User




class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'user', 'payments']

class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'num_lessons', 'lessons']
