from django.urls import path
from . import views

urlpatterns = [
    path('control-number/', views.generate_control_number, name='generate_control_number'),
    path('stk-push/', views.initiate_stk_push, name='initiate_stk_push'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'), # <--- Add this line
]
