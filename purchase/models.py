from django.db import models
from courses.models import Course
from django.contrib.auth.models import User


def upiFolder(instance, filename):
    return f"payment/{instance.user.username}/{filename}"


class PaymentInfo(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    method=models.CharField(max_length=40, default=" ")
    payment_id = models.TextField()
    upi_img = models.ImageField(upload_to=upiFolder)
    price = models.FloatField()
    payment_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.course.title} payment:{'done' if self.payment_completed else 'not'}"


class FailedPayment(models.Model):
    course = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    payment_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


