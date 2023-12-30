# expense/models.py
from django.db import models
from django.contrib.auth.models import User


class WExpense(models.Model):
    date = models.DateField()
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255)
    
   

    def __str__(self):
        return f"{self.date} - {self.item}: ${self.price}"
