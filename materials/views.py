from django.shortcuts import render
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import Payment


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_date', 'paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']