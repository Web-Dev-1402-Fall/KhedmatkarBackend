from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    is_customer = models.BooleanField(default=False)
    is_specialist = models.BooleanField(default=False)


class Specialist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def wallet(self):
        Wallet = apps.get_model('payment', 'Wallet')  # Get the Wallet model
        wallet = Wallet.objects.get(user=self.user)
        return wallet



