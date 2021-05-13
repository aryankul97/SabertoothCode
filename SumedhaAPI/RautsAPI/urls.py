from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/',login),
    path('api/v1/admin/',administrator),
    path('api/v1/admin_list/',administrator_list),
    path('api/v1/staff_type/',staff_type),
    path('api/v1/staff_type_list/',staff_type_list),
    path('api/v1/vehicles/',vehicles),
    path('api/v1/vehicles_list/',vehicles_list),
    path('api/v1/vehicle_delete/',vehicle_delete),
    path('api/v1/vehicle_update/',vehicle_update),
    path('api/v1/vehicle_show/',vehicle_show),
    path('api/v1/staff/',staff),
    path('api/v1/staff_list/',staff_list),
    path('api/v1/staff_delete/',staff_delete),
    path('api/v1/staff_update/',staff_update),
    path('api/v1/staff_show/',staff_show),
    path('api/v1/assign_driver_to_vehicle/',assign_driver_to_vehicle),
    path('api/v1/cylinder_bills/',cylinder_bills),
    path('api/v1/cylinder_bills_list/',cylinder_bills_list),
    path('api/v1/get_cylinder_sales/',get_cylinder_sales),
    path('api/v1/business/',business),
    path('api/v1/business_list/',business_list),
    path('api/v1/assign_cylinder/',assign_cylinder),
    path('api/v1/get_assignments_list/',get_assignments_list),
    path('api/v1/forgotpassword/',forgot_password),
    path('api/v1/changepassword/',change_password),
    path('api/v1/petrol/',petrol),
    path('api/v1/petrol_bills/',petrol_bills),
    path('api/v1/diesel/',diesel),
    path('api/v1/diesel_bills/',diesel_bills),
    path('api/v1/fuel_dashboard/',fuel_dashboard),
    path('api/v1/cylinder_history/',cylinder_history),
    path('api/v1/cylinder_dashboard/',cylinder_dashboard),
    path('api/v1/get_assigned_vehicles_list_by_date/',get_assigned_vehicles_list_by_date),
    path('api/v1/deassign_vehicle/',deassign_vehicle),
    path('api/v1/generate_report/',generate_report),
    path('api/v1/check_vehicle_assignment/',check_vehicle_assignment),
    path('api/v1/get_assigned_data_by_date_and_vehicle_id/',get_assigned_data_by_date_and_vehicle_id),
    path('api/v1/calculate_fuel_profit_of_day/',calculate_fuel_profit_of_day),
    path('api/v1/fuel_purchase_entry/', fuel_purchase_entry),
    path('api/v1/get_cylinder_count/', get_cylinder_count),
    path('api/v1/get_current_petrol_quantity/', get_current_petrol_quantity),
    path('api/v1/get_current_diesel_quantity/', get_current_diesel_quantity),
    path('api/v1/savemeterreadings/', savemeterreadings),
    path('api/v1/listmeterreadings/', listmeterreadings),
    path('api/v1/cylinder_purchase_report/', cylinder_purchase_report),
    path('api/v1/cylinder_sales_report/', cylinder_sales_report),
    path('api/v1/fuel_sales_report/', fuel_sales_report),
    path('api/v1/fuel_purchase_report/', fuel_purchase_report),

    #path('addbasic/',addbasic),
    path('cleardb/',cleardb),
    path('trial/',trial),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)