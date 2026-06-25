from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

# Import all views
from taxpayers.views import taxpayer_lookup, register_taxpayer
from ussd.views import ussd_handler
from payments.views import generate_control_number, initiate_stk_push
from integrations.views import brela_lookup, land_lookup, full_360_view
from core.views import signup_view, login_view, logout_view, home_view

urlpatterns = [
    path('', login_view, name='login'),           # First page is Login
    path('signup/', signup_view, name='signup'),
    path('dashboard/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/lookup/<str:nida_number>/', taxpayer_lookup),
    path('api/register/', register_taxpayer),
    path('ussd/', ussd_handler),
    path('api/payment/control-number/', generate_control_number),
    path('api/payment/stk-push/', initiate_stk_push),
    path('api/brela/lookup/<str:nida_number>/', brela_lookup),
    path('api/land/lookup/<str:nida_number>/', land_lookup),
    path('api/360-view/<str:nida_number>/', full_360_view),
]           