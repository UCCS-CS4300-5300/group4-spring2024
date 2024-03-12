import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Laundromat(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    
   

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('laundromat_detail', args=[str(self.id)])
    

#redoing hopefully it will push ( justin).

class Laundromat(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
   

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
    Reserved = 'Resvered'

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


#if we deicide to move on to resrvation function
    
#class Reservation(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #machine = models.ForeignKey(Machines, on_delete=models.CASCADE)
   # start_time = models.DateTimeField()
    #end_time = models.DateTimeField()





from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Reservation(models.Model):
    machine = models.ForeignKey('Machines', on_delete=models.CASCADE, related_name='reservations')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_reservations')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def duration(self):
        """Calculate the duration of the reservation."""
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = datetime.combine(self.date, self.end_time)
        return (end_datetime - start_datetime).total_seconds() / 60.0  # Duration in minutes

    def __str__(self):
        return f'Reservation {self.id} for machine {self.machine.id} by {self.customer.username} on {self.date} from {self.start_time} to {self.end_time}'

    class Meta:
        # Ensuring that a machine cannot be double-booked for the same time slot
        unique_together = ('machine', 'date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']
