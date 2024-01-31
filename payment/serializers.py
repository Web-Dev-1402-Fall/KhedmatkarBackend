from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'balance',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'timestamp')
