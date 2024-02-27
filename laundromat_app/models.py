from django.db import models
from django.urls import reverse

# Create your models here.

class Laundromat(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    phone = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    