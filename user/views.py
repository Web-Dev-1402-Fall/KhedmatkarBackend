from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Value
from django.db.models.functions import Concat
from .models import Customer, Specialist, Admin, User
from .serializers import UserSerializer, InfoSerializer, LoginSerializer, ChangePasswordSerializer, CustomerSerializer
from payment.views import WalletListAPIView


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if request.data['type'] == "customer":
            user.is_customer = True
            user.save()
            c = Customer(user=user)
            c.save()
        else:
            user.is_specialist = True
            user.save()
            s = Specialist(user=user)
            s.save()
        request.user = user
        response = WalletListAPIView().post(request)
        return Response(serializer.data | response.data)


class AdminRegisterView(APIView):
    # Todo change AllowAny
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_admin = True
        user.save()
        a = Admin(user=user)
        a.save()

        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password"]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # send_email()
        user = request.user
        serializer = InfoSerializer(user)
        return Response(serializer.data)


class SpecialistInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        users = User.objects.filter(pk=pk, is_specialist=True)
        if len(users) > 0:
            return Response(UserSerializer(users[0]).data, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class SpecialistSearchView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        query = request.query_params.get('query', '')
        user_specialists = User.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')). \
            filter(full_name__icontains=query, is_specialist=True)
        serializer = UserSerializer(user_specialists, many=True)
        return Response(serializer.data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        customers = Customer.objects.filter(user=user)
        if len(customers) > 0:
            serializer = CustomerSerializer(customers[0])
        return Response(serializer.data)


class UserInfoModificationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status.HTTP_200_OK)
