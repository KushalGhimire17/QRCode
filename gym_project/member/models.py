from django.db import models
from django.core.validators import RegexValidator
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    MORNING = 'M'
    DAY = 'D'
    EVENING = 'E'
    SHIFT_CHOICES = [
        (MORNING, 'Morning'),
        (DAY, 'Day'),
        (EVENING, 'Evening')
    ]
    shift = models.CharField(
        max_length=1,
        choices=SHIFT_CHOICES
    )
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.phone_number)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class Profile(models.Model):
    name = models.OneToOneField(
        Member, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='profile/images')
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2)
    height = models.DecimalField(
        max_digits=5, decimal_places=2)
    amount = models.FloatField(default=0.0)
    activity_levels = models.FloatField(default=1.2)
    medical_condiions = models.CharField(max_length=500)
    attendance = models.BooleanField(default=False)
