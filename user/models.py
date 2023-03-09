import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


def imgFolder(instance, filename):
    return f"img/{instance.username.username}/{filename}"


class ExtendUser(models.Model):
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    profile = models.ImageField(upload_to=imgFolder , default="img/hacker.png")
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

    def save(self, *args, **kwargs):
        # if not self.id:
        self.uploadedImage = self.compressImage(self.profile)
        super(ExtendUser, self).save(*args, **kwargs)

    def compressImage(self, profile):
        imageTemproary = Image.open(profile)
        if imageTemproary.mode in ("RGBA","P"):
            imageTemproary = imageTemproary.convert("RGB")
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % profile.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage
