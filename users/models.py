from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


NULLABLE = {"null": True, "blank": True}

class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to="avatar/", **NULLABLE, verbose_name='аватар')
    phone_number = models.CharField(max_length=35, **NULLABLE, verbose_name='номер телефона')
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, verbose_name='платный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, verbose_name='платный урок')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='к оплате')
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')], verbose_name='способ оплаты')

    def __str__(self):
        return f"Платеж за {self.user.username} на {self.payment_date}"
