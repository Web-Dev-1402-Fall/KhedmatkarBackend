import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import Wallet
from service.entities.serializers.SpecialtySerializer import SpecialtySerializer
from user.decorators import admin_required

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Customer
from .models import ServiceType, ServiceRequest
from .serializers import ServiceTypeSerializer, ServiceRequestSerializer
from user.decorators import customer_required, specialist_required


# Create your views here.
class NewSpecialityView(APIView):
    permission_classes = [IsAuthenticated, ]

    @admin_required
    def post(self, request):
        specialty = SpecialtySerializer(data=request.data)
        if specialty.is_valid():
            specialty.save()
            return Response(specialty.data, status=status.HTTP_201_CREATED)
        return Response(specialty.errors, status=status.HTTP_400_BAD_REQUEST)


# 1. Search for service types
class ServiceTypeSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        service_types = ServiceType.objects.filter(name__icontains=query)
        print(service_types)
        serializer = ServiceTypeSerializer(service_types, many=True)
        return Response(serializer.data)


# 2. Register a service request
class ServiceRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @customer_required
    def post(self, request):
        serializer = ServiceRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_user = Customer.objects.get(user=request.user)
        serializer.save(customer=customer_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 3. Accept or reject initial request by specialist
from .entities import ServiceRequestStatus
from user.models import Specialist

from django.utils import timezone


class ServiceRequestUpdateBySpecialistView(APIView):
    permission_classes = [IsAuthenticated]

    @specialist_required
    def patch(self, request, pk):
        service_request = ServiceRequest.objects.get(pk=pk)
        data = request.data.copy()  # Make a mutable copy of the data
        data['price'] = request.data.get('price')  # Get the price from the request data
        serializer = ServiceRequestSerializer(service_request, data=data, partial=True)  # Pass the data to the serializer
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('status') == ServiceRequestStatus.ServiceRequestStatus.SPECIALIST_ACCEPTED:
            specialist_user = Specialist.objects.get(user=request.user)
            service_request.accepted_specialist = specialist_user
            service_request.reception_date = timezone.now().date()  # set reception_date to current date
            service_request.save()
        serializer.save()
        return Response(serializer.data)


class ServiceRequestUpdateByCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    @customer_required
    def patch(self, request, pk):
        service_request = ServiceRequest.objects.get(pk=pk)
        if request.user != service_request.customer.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ServiceRequestSerializer(service_request, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ServiceRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service_requests = ServiceRequest.objects.all()
        serializer = ServiceRequestSerializer(service_requests, many=True)
        return Response(serializer.data)


class ServiceTypeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @admin_required
    def post(self, request):
        serializer = ServiceTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ServiceTypeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @admin_required
    def delete(self, request, pk):
        service_type = ServiceType.objects.get(pk=pk)
        service_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(staff_member_required, name='dispatch')
class AllServiceRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    @admin_required
    def get(self, request):
        service_requests = ServiceRequest.objects.all()
        serializer = ServiceRequestSerializer(service_requests, many=True)
        return Response(serializer.data)


class ServiceRequestUpdateAddressView(APIView):
    permission_classes = [IsAuthenticated]

    @customer_required
    def patch(self, request, pk):
        service_request = ServiceRequest.objects.get(pk=pk)
        if request.user != service_request.customer.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ServiceRequestSerializer(service_request, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ServiceRequestCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    @customer_required
    def patch(self, request, pk):
        service_request = ServiceRequest.objects.get(pk=pk)
        if request.user != service_request.customer.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        service_request.status = 'completed'
        service_request.save()
        return Response(ServiceRequestSerializer(service_request).data)


from rest_framework.generics import DestroyAPIView
from .models import Specialty


class SpecialtyDeleteView(DestroyAPIView):
    queryset = Specialty.objects.all()
    lookup_field = 'id'


from rest_framework.generics import ListAPIView
from .models import Specialty


class SpecialtyListView(ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ServiceRequest
from user.models import Customer
from .serializers import ServiceRequestSerializer


from rest_framework.authtoken.models import Token as AuthToken

from rest_framework.authtoken.models import Token as AuthToken

class ServiceRequestFinalDecisionByCustomerView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    @customer_required
    @transaction.atomic
    def patch(self, request, pk):
        service_request = ServiceRequest.objects.get(pk=pk)
        if request.user != service_request.customer.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        decision = request.data.get('decision')
        if decision.lower() == 'accept':
            customer = Customer.objects.get(user=request.user)
            wallet = Wallet.objects.get(user=customer.user)
            if customer.wallet.balance < service_request.price:
                return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
            # Get or create the token for the current user
            token, created = AuthToken.objects.get_or_create(user=request.user)
            # Call the API in the payment module to withdraw the service price from the wallet
            response = requests.put(f'http://localhost:8000/payment/wallets/{wallet.id}/',
                                    data={'balance': -service_request.price},
                                    headers={
                                        'Authorization': f'Token {token.key}',
                                        # Include the authentication token in the headers
                                        'X-Internal-Secret': 'your_internal_secret'  # Include the special header
                                    })
            if response.status_code != 200:
                return Response({'error': 'Failed to withdraw the service price from the wallet.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            service_request.status = 'accepted'
        elif decision.lower() == 'reject':
            service_request.status = 'rejected'
        else:
            return Response({'error': 'Invalid decision. Please enter "accept" or "reject".'},
                            status=status.HTTP_400_BAD_REQUEST)
        service_request.save()
        return Response(ServiceRequestSerializer(service_request).data)