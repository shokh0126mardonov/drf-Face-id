from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SUPERADMIN = 'SUPERADMIN', 'Superadmin'
    role = models.CharField(choices=Role.choices,default=Role.ADMIN, max_length=10)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN

class Student(models.Model):
    class Gender(models.TextChoices):
        ERKAK = 'ERKAK','Erkak'
        AYOL = 'AYOL','Ayol'

    gender = models.CharField(choices=Gender.choices,default=Gender.ERKAK, max_length=50)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    faculty = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    room = models.IntegerField()
    number = models.CharField(max_length=15)
    parent_number = models.CharField(max_length=15)
    home_number = models.CharField(max_length=15)
    location = models.CharField(max_length=128)
    token = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.room}"

class Payment(models.Model):
    class PaymentChoices(models.TextChoices):
        PAID = "paid", "To'langan"
        PARTIALLY = "partial", "Qisman to'langan"
        UNPAID = "unpaid", "To'lanmagan"

    student = models.ForeignKey("Student", verbose_name=("payment"), on_delete=models.SET_NULL,related_name='payment',null=True,blank=True,)
    amount = models.IntegerField(default=0)
    month = models.DateField()
    status = models.CharField(choices=PaymentChoices.choices,default=PaymentChoices.UNPAID,max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tracking(models.Model):
    class TrackingChoices(models.TextChoices):
        KIRDI = 'KIRDI','Kirdi'
        CHIQDI = 'CHIQDI','Chiqdi'
    student = models.ForeignKey("Student", on_delete=models.CASCADE,related_name='tracking')
    status = models.CharField(choices=TrackingChoices.choices, max_length=50)
    time = models.DateTimeField()


class Rules(models.Model):
    class Gender(models.TextChoices):
        ERKAK = 'ERKAK','Erkak'
        AYOL = 'AYOL','Ayol'
    admin = models.ForeignKey("CustomUser",on_delete=models.SET_NULL,null=True,blank=True,)
    time = models.TimeField()
    exit_time = models.TimeField()