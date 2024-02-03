from django.urls import path
from .views import WalletListAPIView, WalletDetailAPIView, AdminWalletDetailAPIView, TransactionListAPIView, TransactionDetailAPIView

urlpatterns = [
    path('wallets/create/', WalletListAPIView.as_view()),
    path('wallets/', WalletDetailAPIView.as_view()),
    path('wallets/admin/<int:pk>/', AdminWalletDetailAPIView.as_view()),
    path('transactions/', TransactionListAPIView.as_view()),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view()),
]
