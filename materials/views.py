from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import StandardResultsSetPagination
from materials.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import Payment
from users.permissions import IsModerator, IsOwner
from rest_framework import filters
from django.shortcuts import get_object_or_404

class CourseViewSet(viewsets.ModelViewSet):
    """Вью-сет для модели Курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)


class LessonCreateAPIView(generics.CreateAPIView):
    """создание записи"""

    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """просмотр записи"""
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name='moderators').exists():
    #         return Lesson.objects.all()
    #     return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """просмотр конкретной записи"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsModerator, IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """изменение записи"""
    serializer_class = LessonSerializer
    # permission_classes = [IsModerator, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """создание записи"""
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser, IsOwner]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_date', 'paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    # permission_classes = [IsModerator]

class SubscriptionView(APIView):
    """Управление подпиской"""
    # permission_classes = [IsAuthenticated]  # Убедитесь, что только авторизованные пользователи могут подписаться

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        # Проверка, существует ли курс, если нет, верните ответ 404.
        try:
            course_item = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Проверка, подписан ли пользователь уже на курс
        if Subscription.objects.filter(user=user, course=course_item).exists():
            Subscription.objects.filter(user=user, course=course_item).delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
