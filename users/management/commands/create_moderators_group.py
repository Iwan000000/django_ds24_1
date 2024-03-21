from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from materials.models import Lesson, Course


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Получаем контент-типы для моделей Lesson и Course
        lesson_content_type = ContentType.objects.get_for_model(Lesson)
        course_content_type = ContentType.objects.get_for_model(Course)

        # Получаем все права доступа для моделей Lesson и Course
        lesson_permissions = Permission.objects.filter(content_type=lesson_content_type)
        course_permissions = Permission.objects.filter(content_type=course_content_type)

        # Добавляем права доступа к группе модераторов
        for permission in lesson_permissions | course_permissions:
            moderators_group.permissions.add(permission)

        # Исключаем права на удаление и создание новых экземпляров
        delete_permissions = Permission.objects.filter(
            content_type=lesson_content_type,
            codename__in=['delete_lesson', 'add_lesson']
        ) | Permission.objects.filter(
            content_type=course_content_type,
            codename__in=['delete_course', 'add_course']
        )

        for permission in delete_permissions:
            moderators_group.permissions.remove(permission)

        self.stdout.write(self.style.SUCCESS('Группа модераторов создана и разрешения успешно назначены.'))
