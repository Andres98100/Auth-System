from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Access_Code
import string
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not None and password is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('signin')

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('signin')
            except User.DoesNotExist:
                User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                return redirect('signin')

@login_required
def home(request):
    if request.user.is_authenticated:
        print("Usuario autenticado:", request.user.username)
    else:
        print("Usuario no autenticado")
    usernames = [user.username for user in User.objects.all()]
    return render(request, 'home.html', {
        'usernames': usernames
        })

def code_generator():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(5))

def send_mail(email, code):
    try:
        msg = MIMEMultipart()
        system_email = "felipevillamizarc@gmail.com"
        subject = "Access code validation"
        message = f"This is your access code: {code}"

        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        smtp_username = "tu_correo@gmail.com"
        smtp_password = "tu_contraseña_de_app"


        # Adjuntar el cuerpo del mensaje al objeto MIMEMultipart
        msg.attach(MIMEText(message, 'plain'))

        # Iniciar una conexión segura con el servidor SMTP
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        # Iniciar sesión en el servidor SMTP
        server.login(smtp_username, smtp_password)

        # Enviar el correo electrónico
        server.sendmail(system_email, email, msg.as_string())

        # Cerrar la conexión con el servidor SMTP
        server.quit()

        return True
    except BaseException:
        return False

def forgot(request):
    if request.method == "GET":
        return render(request, 'forgot.html')
    else:
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            ACCESS_CODE = code_generator()
            new_code = Access_Code(code=ACCESS_CODE, user=user)
            new_code.save()

            mail = send_mail(email, ACCESS_CODE)
            if not mail:
                print("Error al enviar el correo electrónico")

            return JsonResponse({'username': user.username})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Email does not exist.'})
