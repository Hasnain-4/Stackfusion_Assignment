from django.db import models

# Create your models here.


class Formsdata(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.name} Form Data'