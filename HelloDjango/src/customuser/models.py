from django.db import models

# Create your models here.
class CustomUser(models.Model):
    id = models.CharField('ID',max_length=100,primary_key=True)
    password = models.CharField('PASSWORD',max_length=100)
    
