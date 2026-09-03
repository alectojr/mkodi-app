from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Import all views
from taxpayers.views import taxpayer_lookup, register_taxpayer, account_lookup
from ussd.views import ussd_handler
from payments.views import generate_control_number, initiate_stk_push
from integrations.views import brela_lookup, land_lookup, full_360_view
from core.views import signup_view, login_view, logout_view, home_view, forgot_password_view, intelligence_view, payments_view, profile_view, change_password_view, payment_receipt_view

urlpatterns = [
    path('', login_view, name='login'),           # First page is Login
    path('signup/', signup_view, name='signup'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('dashboard/', home_view, name='home'),
    path('360-view/', intelligence_view, name='intelligence'),
    path('payments/', payments_view, name='payments'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view, name='change_password'),
    path('payments/<int:payment_id>/receipt/', payment_receipt_view, name='payment_receipt'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/lookup/<str:nida_number>/', taxpayer_lookup),
    path('api/register/', register_taxpayer),
    path('api/account-lookup/<str:tin_number>/', account_lookup, name='account_lookup'),
    path('ussd/', ussd_handler),
    path('api/payment/control-number/', generate_control_number),
    path('api/payment/stk-push/', initiate_stk_push),
    path('api/brela/lookup/<str:nida_number>/', brela_lookup),
    path('api/land/lookup/<str:nida_number>/', land_lookup),
    path('api/360-view/<str:nida_number>/', full_360_view, name='full_360_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)