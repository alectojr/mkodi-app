import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Signup View
def signup_view(request):
    if request.method == 'POST':
        tin = request.POST.get('tin_number', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Validation
        if not tin or not full_name or not phone or not password:
            messages.error(request, "All fields are required")
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('signup')

        if User.objects.filter(username=tin).exists():
            messages.error(request, "This TIN is already registered")
            return redirect('signup')

        try:
            user = User.objects.create_user(
                username=tin,
                password=password,
                email=email if email else None,
                first_name=full_name
            )
            login(request, user)
            return redirect('home')
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
    context = {
        'user_tin': user.username,
        'user_name': user.first_name or user.username,
        'user_email': user.email,
    }
    return render(request, 'index.html', context)