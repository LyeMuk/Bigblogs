from django.db import models

# Create your models here.

class UserRegister(models.Model):
    email=models.CharField(max_length=255)
    uname=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    securityQuestion=models.CharField(max_length=255)


    
class blogg(models.Model):
    bid = models.AutoField(primary_key=True)
    bdate=models.CharField(max_length=25)
    authorname=models.CharField(max_length=255)
    title=models.CharField(max_length=300)
    content=models.CharField(max_length=1500)