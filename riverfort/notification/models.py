from django.db import models

# Create your models here.

class Company(models.Model):
  company = models.CharField(max_length=200)
  time    = models.CharField(max_length=200)

  def __str__(self):
    return self.company
    