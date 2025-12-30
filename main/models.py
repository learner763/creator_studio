# main/models.py
from django.db import models

class app_users(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=15)
    subscription = models.CharField(max_length=12)
    fullname = models.CharField(max_length=15)
    residence = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    parent = models.EmailField()
    displayname = models.CharField(max_length=15)
    account = models.CharField(max_length=12)
    last_login=models.CharField(max_length=50,null=True)
