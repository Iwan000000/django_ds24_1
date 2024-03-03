from rest_framework.routers import DefaultRouter

from materials.apps import CoursesConfig
from materials.views import CourseViewSet

app_name = CoursesConfig.name

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

urlpatterns = [

] + router.urls
