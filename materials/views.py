from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Subscription
from materials.models import Lesson
from materials.paginators import StandardResultsSetPagination
from materials.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from materials.services import create_stripe_price, create_stripe_session
from users.models import Payment
from users.permissions import IsModerator, IsOwner

from datetime import timedelta
from django.utils import timezone


class CourseViewSet(viewsets.ModelViewSet):
    """Вью-сет для модели Курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        subscribed_users = instance.get_subscribed_users()
        # Отправляем уведомление каждому подписанному пользователю

        course = Course.objects.get(id=course_id)

        # проверка, обновлялся ли курс более 4 часов назад
        if course.updated_at < timezone.now() - timedelta(hours=4):
            for user in subscribed_users:
                if user.email:
                    send_update_email.delay(instance.name, user.email)

        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    """создание записи"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'description')

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """просмотр конкретной записи"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator, IsOwner]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'description')


class LessonUpdateAPIView(generics.UpdateAPIView):
    """изменение записи"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """создание записи"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser, IsOwner]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['payment_date', 'paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = [IsModerator]


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if not course:
            raise serializers.ValidationError('Укажите курс')

        payment = serializer.save()
        price_id = create_stripe_price(payment)
        payment.payment_link, payment.payment_id = create_stripe_session(price_id)
        payment.save()


class SubscriptionView(APIView):
    """Управление подпиской"""

    permission_classes = [IsAuthenticated]  # только авторизованные пользователи могут подписаться

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
