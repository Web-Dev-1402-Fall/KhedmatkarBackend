from django.db import models
from user.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    balance = models.BigIntegerField(default=0)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    amount = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
