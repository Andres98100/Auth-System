# ಠ╭╮ಠ   ⚆_⚆   (●'◡'●)   ✪ω✪   (╯▔皿▔)╯   (►__◄)
from django.shortcuts import render, redirect # ✍️(◔◡◔)
from django.contrib.auth.models import User # ⚆_⚆
from django.contrib.auth import authenticate, login # ✪ω✪
# (❁´◡`❁)

# (👉ﾟヮﾟ)👉
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Username or password is incorrect.'})
    else:
        return render(request, 'login.html')

# (👉ﾟヮﾟ)👉
def register(request):
    """( ͡• ͜ʖ ͡•)✌ ✔"""
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                    )
                return redirect('login')
            except User.DoesNotExist:
                User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                return redirect('login')

# # (👉ﾟヮﾟ)👉      
def home(request):
    """( ͡• ͜ʖ ͡•)✌ ✔"""
    usernames = [user.username for user in User.objects.all()]
    return render(request, 'home.html', {
        'usernames': usernames
        })

