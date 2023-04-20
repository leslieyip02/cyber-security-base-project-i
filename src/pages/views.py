from django.shortcuts import render, redirect
from .models import Account


def homePageView(request):
    username = request.session.get('username')
    return render(request, 'pages/index.html', {'username': username})


def loginView(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        authenticated = False

        try:
            account = Account.objects.get(username=username)
            if password == account.password:
                authenticated = True

        except:
            error_message = 'Account does not exists'

        if authenticated:
            request.session['username'] = account.username
            request.session['authenticated'] = True
            return redirect('/')

        elif not error_message:
            error_message = 'Wrong password'

    return render(request, 'pages/login.html', {'error_message': error_message})


def signupView(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not Account.objects.filter(username=username).exists():
            Account.objects.create(username=username, password=password)

            request.session['username'] = username
            request.session['authenticated'] = True
            return redirect('/')

        else:
            error_message = 'Account already exists'

    return render(request, 'pages/signup.html', {'error_message': error_message})


def logoutView(request):
    request.session['username'] = None
    request.session['authenticated'] = False
    return redirect('/')
