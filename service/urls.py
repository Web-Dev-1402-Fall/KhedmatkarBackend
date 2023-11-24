from django.urls import path, include
from .views import *

urlpatterns = [
    path('spec/add/', NewSpecialityView.as_view()),
    path('service-types/search/', ServiceTypeSearchView.as_view()),
    path('service-requests/create/', ServiceRequestCreateView.as_view()),
    path('service-requests/<int:pk>/update-by-customer/', ServiceRequestUpdateByCustomerView.as_view()),
    path('service-requests/<int:pk>/update-by-specialist/', ServiceRequestUpdateBySpecialistView.as_view()),
    path('service-requests/', ServiceRequestListView.as_view()),
    path('service-types/create/', ServiceTypeCreateView.as_view()),
    path('service-types/<int:pk>/delete/', ServiceTypeDeleteView.as_view()),
    path('all-service-requests/', AllServiceRequestListView.as_view()),
    path('service-requests/<int:pk>/update-address/', ServiceRequestUpdateAddressView.as_view()),
    path('service-requests/<int:pk>/complete/', ServiceRequestCompleteView.as_view()),
    path('specialties/<int:id>/', SpecialtyDeleteView.as_view(), name='specialty-delete'),
    path('specialties/', SpecialtyListView.as_view(), name='specialty-list'),
]
