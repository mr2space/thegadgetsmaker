from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class ExtendUser(models.Model):
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    profile = models.ImageField(upload_to='img/',default="defualt.jpeg")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list
    full_name = models.CharField(max_length=15,null=False)
    otp = models.IntegerField()
    address = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return  self.full_name
