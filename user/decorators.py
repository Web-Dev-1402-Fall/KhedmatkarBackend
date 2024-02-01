from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext_lazy as _


def customer_required(func):
    @wraps(func)
    def _wrapped_view(instance, request, *args, **kwargs):
        print(request.user.id)
        if not request.user.is_authenticated:
            return Response({'error': _('Please login to continue.')}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_customer:
            return Response({'error': _('You are not authorized to access this resource.')},
                            status=status.HTTP_403_FORBIDDEN)
        return func(instance,request, *args, **kwargs)

    return _wrapped_view


def specialist_required(func):
    @wraps(func)
    def _wrapped_view(instance, request, *args, **kwargs):
        print(request.user.id)
        if not request.user.is_authenticated:
            return Response({'error': _('Please login to continue.')}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_specialist:
            return Response({'error': _('You are not authorized to access this resource.')},
                            status=status.HTTP_403_FORBIDDEN)
        return func(instance,request, *args, **kwargs)

    return _wrapped_view


def admin_required(func):
    @wraps(func)
    def _wrapped_view(instance, request, *args, **kwargs):
        print(request.user.id)
        if not request.user.is_authenticated:
            return Response({'error': _('Please login to continue.')}, status=status.HTTP_401_UNAUTHORIZED)
        return func(instance,request, *args, **kwargs)

    return _wrapped_view
