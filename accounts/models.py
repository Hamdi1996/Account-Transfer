from django.db import models

class Account(models.Model):
    id = models.CharField(max_length=36, primary_key=True)  # UUID or string ID
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.balance}"
