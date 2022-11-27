from django.db import models

# Create your models here.

class UserRegister(models.Model):
    email=models.CharField(max_length=255)
    uname=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    securityQuestion=models.CharField(max_length=255)
    
