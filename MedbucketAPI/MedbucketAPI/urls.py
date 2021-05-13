from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login_user/', login_user),
    path('api/v1/check_mobile_uniqueness/', check_mobile_uniqueness),
    path('api/v1/check_email_uniqueness/', check_email_uniqueness),
    path('api/v1/save_user_details/', save_user_details),
    path('api/v1/get_user_details/', get_user_details),
    path('api/v1/update_store/', update_store),
    path('api/v1/save_store_payment_and_business_details/', save_store_payment_and_business_details),
    path('api/v1/add_medicine_basic_info/', add_medicine_basic_info),
    path('api/v1/add_medicine_stocks/', add_medicine_stocks),
    path('api/v1/add_medicine_price/', add_medicine_price),
    path('api/v1/add_medicine_distributer/', add_medicine_distributer),
    path('api/v1/get_medicine_data/', get_medicine_data),
    path('api/v1/get_medicine_suggestions/', get_medicine_suggestions),
    path('api/v1/get_medicines_details/', get_medicines_details),
    path('api/v1/save_purchse_review_details/', save_purchse_review_details),
    path('api/v1/get_customer_details/', get_customer_details),
    path('api/v1/save_customer_details_and_get_total_amount/', save_customer_details_and_get_total_amount),
    path('api/v1/record_payment_info/', record_payment_info),
    path('api/v1/get_inventory_listing/', get_inventory_listing),
    path('api/v1/get_selected_medicine_stock_data/', get_selected_medicine_stock_data),
    path('api/v1/update_medicine_stock_data/', update_medicine_stock_data),
    path('api/v1/get_medicine_basic_info_from_master/', get_medicine_basic_info_from_master),
    path('api/v1/get_dashboard_data/', get_dashboard_data),
    path('api/v1/get_medicine_batch/', get_medicine_batch),
    path('api/v1/add_medicine_batch/', add_medicine_batch),
    path('api/v1/delete_medicine_batch/', delete_medicine_batch),
    path('api/v1/update_medicine_batch/', update_medicine_batch),
    path('api/v1/update_store_and_bank_details/', update_store_and_bank_details),
    path('api/v1/get_store_profile/', get_store_profile),
    path('api/v1/update_stock/', update_stock),
    path('api/v1/save_unit/', save_unit),
    path('api/v1/list_unit/', list_unit),
    path('api/v1/get_transactions_data/', get_transactions_data),
    path('api/v1/trial/', trial),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)