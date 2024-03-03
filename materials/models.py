from django.db import models

from users.models import NULLABLE


class Course(models.Model):

    name = models.CharField(max_length=100,verbose_name='название')
    preview = models.ImageField(upload_to='previews_course/', **NULLABLE, verbose_name='превью')
    description = models.TextField(max_length=10000, verbose_name='описание')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"



class Lesson(models.Model):

    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(max_length=10000, verbose_name='описание')
    preview = models.ImageField(upload_to='previews_lesson/', **NULLABLE, verbose_name='превью')
    video_link = models.URLField(verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='уроки', **NULLABLE)

    def __str__(self):
        return f"{self.name}({self.course}) {self.description} {self.video_link}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
