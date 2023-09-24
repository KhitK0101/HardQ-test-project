from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.PositiveIntegerField()  # длительность в секундах
    products = models.ManyToManyField(Product, related_name='lessons')


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    duration_watched = models.PositiveIntegerField(
        default=0
    )  # время просмотра в секундах
    is_watched = models.BooleanField(
        default=False
    )  # статус просмотра
    last_viewed = models.DateTimeField(
        null=True, blank=True
    )  # дата последнего просмотра

    def save(self, *args, **kwargs):
        if self.duration_watched >= self.lesson.duration * 0.8:
            self.is_watched = True
        super(UserLesson, self).save(*args, **kwargs)
