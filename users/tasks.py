from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def block_inactive_users():
    """
        Блокирует пользователей, которые не заходили в течение 30 дней.
    """
    User = get_user_model()
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - timedelta(days=30))
    for user in inactive_users:
        user.is_active = False
        user.save()
