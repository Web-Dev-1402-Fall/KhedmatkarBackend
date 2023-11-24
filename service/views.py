from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ServiceRequestUpdateBySpecialistView(APIView):
    permission_classes = [IsAuthenticated]

    @specialist_required
    def patch(self, request, pk):
        service_request = ServiceRequest.objects.get(pk=pk)
        serializer = ServiceRequestSerializer(service_request, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('status') == ServiceRequestStatus.ServiceRequestStatus.SPECIALIST_ACCEPTED:
            specialist_user = Specialist.objects.get(user=request.user)
            service_request.accepted_specialist = specialist_user
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
