from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Laundromat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='laundromats', null=True)
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    hours = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
   

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('laundromat_detail', args=[str(self.id)])
       

class Machines(models.Model):
    Dryer = 'Dryer'
    Washer = 'Washer'

    
    Machine_Choice = [
        (Dryer, 'Dryer'),
        (Washer, 'Washer'),
    ]

    Open = 'Open'
    Reserved = 'Reserved'

    Machine_Status =[
        (Open, 'Open'),
        (Reserved, 'Reserved'),
    ]

    laundromat = models.ForeignKey(Laundromat, on_delete=models.CASCADE)
    #unique id for every machine.
    machine_ID = models.CharField(max_length=100, unique=True)
    #allowing choice for which machine
    machine_choice =models.CharField(max_length =6, choices=Machine_Choice)
    #showing the correct status of that machine
    status =models.CharField(max_length=8, choices=Machine_Status, default = Open)

# simplifies the process of identifying machines by choice and ID.
    def __str__(self):
        return f"{self.machine_choice} - {self.machine_ID}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machines, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

