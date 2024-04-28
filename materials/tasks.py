from celery import shared_task
from django.core.mail import send_mail

from django_ds24_1 import settings
from materials.models import Course, Subscription


@shared_task
def send_update_email(course_id):
    """
    Отложенная задача для отправки электронной почты пользователям при обновлении курса.
    """
    try:
        course = Course.objects.get(pk=course_id)
        course_sub = Subscription.objects.filter(course=course_id)
        for sub in course_sub:
            send_mail(
                subject=f"Обновление курса: {course.name}",
                message=f"Доступны обновления для курса {course.name}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.user.email],
                fail_silently=False  # False, чтобы получать исключения при ошибках отправки
            )
    except Course.DoesNotExist:
        # Обработка случая, когда курс не найден
        print(f"Курс с идентификатором {course_id} не найден.")
    except Exception as e:
        # Обработка любых других исключений
        print(f"Произошла ошибка при отправке уведомлений: {e}")
