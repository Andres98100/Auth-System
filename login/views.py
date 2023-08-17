from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()

                return render(request, 'login.html', {
                    'form': UserCreationForm(),
                    'success': 'User created successfully'
                })
            except:
                return render(request, 'login.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already exists'
                })
        return render(request, 'login.html', {
            'form': UserCreationForm(),
            'error': 'Passwords do not match'
        })
        
def register(request):
    return render(request, 'register.html')
