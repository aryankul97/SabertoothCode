from django.urls import path
from .import views

urlpatterns = [
    path('api/v1/login/',views.login,name='login'),
    path('api/v1/register/',views.register_user,name='register_user'),
    path('api/v1/vehicles/',views.vehicles,name='vehicles'),
    path('api/v1/staff/',views.staff,name='staff'),
]
