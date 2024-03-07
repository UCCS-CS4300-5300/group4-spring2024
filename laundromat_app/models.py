from django.db import models
from django.urls import reverse

# Create your models here.

class Laundromat(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    hours = models.IntegerField()
    description = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('laundromat_detail', args=[str(self.id)])
    