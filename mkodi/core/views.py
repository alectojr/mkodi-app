import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taxpayers.models import Taxpayer
from payments.models import Payment
from .models import UserProfile


def sync_taxpayer_from_signup(tin, full_name, phone, email):
    taxpayer, created = Taxpayer.objects.get_or_create(
        tin_number=tin,
        defaults={
            'nida_number': tin,
            'full_name': full_name,
            'phone_number': phone,
            'email': email or None,
        },
    )

    if not created:
        updated = False
        if taxpayer.full_name != full_name:
            taxpayer.full_name = full_name
            updated = True
        if taxpayer.phone_number != phone:
            taxpayer.phone_number = phone
            updated = True
        if (taxpayer.email or '') != (email or ''):
            taxpayer.email = email or None
            updated = True
        if not taxpayer.nida_number:
            taxpayer.nida_number = tin
            updated = True
        if updated:
            taxpayer.save()

    return taxpayer


def sync_user_from_taxpayer(user):
    try:
        taxpayer = Taxpayer.objects.get(tin_number=user.username)
    except Taxpayer.DoesNotExist:
        return user

    changed = False
    if taxpayer.full_name and user.first_name != taxpayer.full_name:
        user.first_name = taxpayer.full_name
        changed = True
    if taxpayer.email and user.email != taxpayer.email:
        user.email = taxpayer.email
        changed = True

    if changed:
        user.save()

    return user


# Signup View
def signup_view(request):
    if request.method == 'POST':
        tin = request.POST.get('tin_number', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validation
        if not tin or not password or not password_confirm:
            messages.error(request, "TIN, password, and password confirmation are required")
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('signup')

        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=tin).exists():
            messages.error(request, "This TIN is already registered")
            return redirect('signup')

        try:
            taxpayer = Taxpayer.objects.get(tin_number=tin, is_active=True)
            user = User.objects.create_user(
                username=tin,
                password=password,
                email=taxpayer.email or '',
                first_name=taxpayer.full_name,
            )
            sync_user_from_taxpayer(user)
            login(request, user)
            return redirect('home')
        except Taxpayer.DoesNotExist:
            messages.error(request, "This TIN is not available in the admin taxpayer records")
            return redirect('signup')
        except Exception as ex:
            messages.error(request, f"Error creating account: {str(ex)}")
            return redirect('signup')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        tin = request.POST.get('tin_number')
        password = request.POST.get('password')

        user = authenticate(request, username=tin, password=password)
        if user is not None:
            sync_user_from_taxpayer(user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid TIN or Password")

    return render(request, 'login.html')


def forgot_password_view(request):
    temp_password = None
    if request.method == 'POST':
        tin = request.POST.get('tin_number', '').strip()
        if not tin:
            messages.error(request, "Please enter your TIN number")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=tin)
        except User.DoesNotExist:
            messages.error(request, "No account found for that TIN")
            return redirect('forgot_password')

        fruits = [
            'mango', 'banana', 'papaya', 'kiwi', 'guava', 'lychee', 'orange',
            'pineapple', 'berry', 'apple', 'avocado', 'coconut', 'dragonfruit',
            'starfruit'
        ]
        temp_password = random.choice(fruits)
        user.set_password(temp_password)
        user.save()
        messages.success(request, f"Temporary password generated: {temp_password}")

    return render(request, 'forgot_password.html', {'temp_password': temp_password})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Protected Dashboard
@login_required(login_url='/')
def home_view(request):
    user = request.user
    taxpayer = Taxpayer.objects.filter(tin_number=user.username).first()
    context = {
        'user_tin': user.username,
        'user_name': taxpayer.full_name if taxpayer else user.first_name or user.username,
        'user_email': taxpayer.email if taxpayer else user.email,
        'taxpayer': taxpayer,
        'pending_payments': Payment.objects.filter(taxpayer=taxpayer, status='pending').count() if taxpayer else 0,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/')
def payment_receipt_view(request, payment_id):
    taxpayer = Taxpayer.objects.filter(tin_number=request.user.username).first()
    payment = Payment.objects.filter(id=payment_id, taxpayer=taxpayer).first()
    if payment is None:
        messages.error(request, 'Payment receipt not found.')
        return redirect('payments')
    return render(request, 'payment_receipt.html', {'payment': payment})


@login_required(login_url='/')
def intelligence_view(request):
    taxpayer = Taxpayer.objects.filter(tin_number=request.user.username).first()
    return render(request, 'intelligence.html', {'taxpayer': taxpayer, 'user_tin': request.user.username})


@login_required(login_url='/')
def payments_view(request):
    taxpayer = Taxpayer.objects.filter(tin_number=request.user.username).first()
    if request.method == 'POST' and taxpayer:
        amount = request.POST.get('amount', '').strip()
        method = request.POST.get('payment_method', 'mobile_money').strip()
        if method not in {'ussd', 'gepg', 'mobile_money'}:
            messages.error(request, 'Choose a valid payment method.')
        else:
            try:
                amount_value = float(amount)
                if amount_value <= 0:
                    raise ValueError
                control_number = '99' + ''.join(random.choices('0123456789', k=10))
                Payment.objects.create(
                    taxpayer=taxpayer,
                    control_number=control_number,
                    amount=amount_value,
                    payment_method=method,
                )
                messages.success(request, f'Payment request created. Control number: {control_number}')
                return redirect('payments')
            except ValueError:
                messages.error(request, 'Enter a valid payment amount.')
    payments = Payment.objects.filter(taxpayer=taxpayer).order_by('-created_at') if taxpayer else Payment.objects.none()
    return render(request, 'payments.html', {'payments': payments})


@login_required(login_url='/')
def profile_view(request):
    taxpayer = Taxpayer.objects.filter(tin_number=request.user.username).first()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        allowed_types = {'image/jpeg', 'image/png', 'image/webp'}
        if photo.content_type not in allowed_types or photo.size > 2 * 1024 * 1024:
            messages.error(request, 'Upload a JPG, PNG, or WebP image smaller than 2 MB.')
        else:
            profile.photo = photo
            profile.save()
            messages.success(request, 'Profile photo updated.')
        return redirect('profile')
    return render(request, 'profile.html', {'taxpayer': taxpayer, 'profile': profile})


@login_required(login_url='/')
def change_password_view(request):
    if request.method == 'POST':
        current = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirmation = request.POST.get('confirm_password', '')
        if not request.user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters.')
        elif new_password != confirmation:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save(update_fields=['password'])
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
    return render(request, 'change_password.html')