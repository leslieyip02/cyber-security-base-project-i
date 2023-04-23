from django.shortcuts import render, redirect
from .models import Account, Record


def home(request):
    """
    Home view for the root of the application.
    """
    if request.session['authenticated']:
        username = request.session['username']
        return redirect(f'./users/{username}/')

    return render(request, 'pages/index.html')


def login(request):
    """
    Handles logins and authentication.

    GET request -> a login form is returned.

    POST request -> the login information will used to authenticate the user.
    """
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
            return redirect(f'../users/{username}/')

        elif not error_message:
            error_message = 'Wrong password'

    return render(request, 'pages/login.html', {'error_message': error_message})


def signup(request):
    """
    Handles account creation.

    GET request -> a signup form is returned.

    POST request -> creates an account with the given information.
    """
    error_message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not Account.objects.filter(username=username).exists():
            Account.objects.create(username=username,
                                   password=password)

            request.session['username'] = username
            request.session['authenticated'] = True
            return redirect(f'../users/{username}/')

        else:
            error_message = 'Account already exists'

    return render(request, 'pages/signup.html', {'error_message': error_message})


def logout(request):
    """
    Handles logouts.
    """
    request.session['username'] = None
    request.session['authenticated'] = False
    return redirect('/')


def user(request, username=""):
    """
    Returns a unique page for each authenticated user.
    """
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        record = Record.objects.get(username=username,
                                    account=account)

        # update record if it exists
        if record:
            record.password = password
            Record.save()

        else:
            Record.objects.create(username=username,
                                  account=account,
                                  password=password)

    records = Record.objects.filter(username=username).values()
    return render(request, 'pages/user.html',
                  {'username': username, 'records': records})
