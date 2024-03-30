from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        default_related_name = 'custom_user_related'

class Laundromat(models.Model):
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


#if we deicide to move on to resrvation function
    
#class Reservation(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #machine = models.ForeignKey(Machines, on_delete=models.CASCADE)
   # start_time = models.DateTimeField()
    #end_time = models.DateTimeField()
