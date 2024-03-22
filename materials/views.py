from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import Payment
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Вью-сет для модели Курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(generics.ListCreateAPIView):
    """создание записи"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    """просмотр записи"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """просмотр конкретной записи"""
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsOwner]

    # def get_object(self):
    #     obj = get_object_or_404(Lesson, pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)
    #     return obj


class LessonUpdateAPIView(generics.UpdateAPIView):
    """изменение записи"""
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsOwner]

    # def get_object(self):
    #     obj = get_object_or_404(Lesson, pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)
    #     return obj


class LessonDestroyAPIView(generics.DestroyAPIView):
    """создание записи"""
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser, IsOwner]

    # def get_object(self):
    #     obj = get_object_or_404(Lesson, pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)
    #     return obj


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_date', 'paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = [IsModerator]

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name='moderators').exists():
    #         return Payment.objects.all()
    #     return Payment.objects.filter(owner=self.request.user)
