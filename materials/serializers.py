from rest_framework import serializers
from django.core.exceptions import ValidationError

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_link
from users.models import Payment, User


class LessonSerializer(serializers.ModelSerializer):
    material = serializers.CharField(validators=[validate_youtube_link])

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['id', 'material']


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


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course']


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return obj.subscription_set.filter(user=user).exists()
