from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from materials.models import Course, Lesson

User = get_user_model()

class LessonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="testcase_user@thisistest.test", password="simple_password!"
        )
        self.course = Course.objects.create(name='Test Course', description='Test Description', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Test Description', course=self.course,
                                            owner=self.user, video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    def test_lesson_create(self):
        """Тест создания урока с валидными данными"""
        data = {
            "title": "Test lesson case",
            "description": "This is test video or lesson creating =)",
            "video_url": "https://www.youtube.com/watch?v=EXHxkwDm7c0&list=&index=2234532",
            "course": "2",
        }

        self.client.force_authenticate(self.user)
        response = self.client.post(path="/create_lesson/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_lesson(self):
        """Тест удаления урока с недостаточными правами"""
        self.client.force_authenticate(self.user)
        response = self.client.post(path="/delete_lesson/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course(self):
        """Тест создания курса"""
        data = {
            "name": "CourseTest 2",
            "description": "CourseDescroption 2",
            "user": self.user
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/course/', data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_list_course(self):
        """Тест получения списка курсов"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/course/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_subscription(self):
        """Тест подписки/отписки на курс"""
        # Тестовая подписка на курс
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)

        # Тестовая отписка от курса
        response = self.client.post('/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
