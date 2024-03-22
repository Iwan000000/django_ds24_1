from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import CoursesConfig
from materials.views import CourseViewSet, SubscriptionView, LessonCreateAPIView, LessonListAPIView, \
    LessonRetrieveAPIView, LessonDestroyAPIView, LessonUpdateAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

urlpatterns = [
    path("create_lesson/", LessonCreateAPIView.as_view(), name="create_lesson"),
    path("list_lesson/", LessonListAPIView.as_view(), name="list_lesson"),
    path("retrieve_lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="retrieve_lesson"),
    path("delete_lesson/<int:pk>/", LessonDestroyAPIView.as_view(), name="delete_lesson"),
    path("update_lesson/<int:pk>/", LessonUpdateAPIView.as_view(), name="update_lesson"),
    path("subscription/", SubscriptionView.as_view(), name="subscription")
] + router.urls
