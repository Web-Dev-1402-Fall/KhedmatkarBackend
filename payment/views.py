import time

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Wallet, Transaction
from user.models import User
from .serializers import WalletSerializer, TransactionSerializer


class WalletListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        if not Wallet.objects.filter(user=request.user).exists():
            Wallet(user=request.user, balance=1000).save()
            wallet = Wallet.objects.get(user=request.user)
            return Response({"wallet_id": wallet.id, "balance": wallet.balance}, status=status.HTTP_201_CREATED)
        return Response({"error": "Wallet is already exist!"}, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        if not request.META.get('HTTP_X_INTERNAL_SECRET') == 'your_internal_secret':
            self.check_permissions(request)
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['balance']
            if amount < 0 and wallet.balance < abs(amount):
                return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)
            wallet.balance += amount
            wallet.save()
            Transaction(wallet=wallet, amount=amount, timestamp=time.time()).save()
            return Response(WalletSerializer(wallet).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class AdminWalletDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk):
        wallet = Wallet.objects.filter(user=User.objects.get(pk=pk)).first()
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            wallet.balance += serializer.validated_data['balance']
            wallet.save()
            Transaction(wallet=wallet, amount=serializer.validated_data['balance'], timestamp=time.time()).save()
            return Response(WalletSerializer(wallet).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        transactions = Transaction.objects.filter(wallet__user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
