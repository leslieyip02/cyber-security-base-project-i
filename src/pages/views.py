from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from sqlite3 import connect
from .models import Account

# FIX 2: Use django models
# from .models import Record

# FIX 4: Use password encryption
# from django.contrib.auth.hashers import check_password


def home(request):
    """
    Home view for the root of the application.
    """
    # FIX 1: Keep track of user
    # if request.session.get('username'):
    #     username = request.session['username']
    #     return redirect(f'./users/{username}/')

    return render(request, 'pages/index.html')


# FIX 5: enforce CSRF check
@csrf_exempt
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

            # FIX 4: Check encrypted password
            # if check_password(password, account.password):
            #     authenticated = True

        except:
            error_message = 'Account does not exists'

        if authenticated:
            request.session['username'] = account.username
            request.session['authenticated'] = True
            return redirect(f'../users/{username}/')

        elif not error_message:
            error_message = 'Wrong password'

    return render(request, 'pages/login.html', {'error_message': error_message})


# FIX 5: enforce CSRF check
@csrf_exempt
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

            # FIX 1: Keep track of user
            # request.session['username'] = username

            request.session['authenticated'] = True
            return redirect(f'../users/{username}/')

        else:
            error_message = 'Account already exists'

    return render(request, 'pages/signup.html', {'error_message': error_message})


# FIX 3: Implement a proper logout
# def logout(request):
#     """
#     Handles logouts.
#     """
#     # request.session['username'] = None
#     request.session['authenticated'] = False
#     return redirect('/')


def user(request, username=""):
    """
    Returns a unique page for each authenticated user.
    """

    # FIX 1: Deny access to other users
    # if not request.session.get('username') == username:
    #     return redirect('../../')

    con = connect('src/db.sqlite3')
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE if not exists
        records (username TEXT, account TEXT, password TEXT)
    """)

    res = cur.execute("""
                SELECT * FROM records WHERE username=?
            """, (username,))

    records = []
    for record in res.fetchall():
        _, account, password = record
        records.append({'account': account, 'password': password})

    # FIX 2: Use django models
    # records = Record.objects.filter(username=username).values()

    return render(request, 'pages/user.html',
                  {'username': username, 'records': records, })


# FIX 5: enforce CSRF check
@csrf_exempt
def add(request, username=""):
    """
    Handles adding and updating password records.
    """

    # FIX 1: Deny access to other users
    # if not request.session.get('username') == username:
    #     return redirect('../')

    if request.method == 'POST':
        account = request.POST.get('account').strip()
        password = request.POST.get('password').strip()

        con = connect('src/db.sqlite3')
        cur = con.cursor()
        res = cur.execute("""
            SELECT * FROM records
            WHERE username=? AND account=?
        """, (username, account))

        if res.fetchone() is None:
            query = f"""
                INSERT INTO records (username, account, password)
                VALUES ('{username}', '{account}', '{password}')
            """
            cur.executescript(query)

        else:
            cur.execute("""
                UPDATE records
                SET password=?
                WHERE username=? AND account=?
            """, (password, username, account))

        con.commit()

        # FIX 2: Use django models to prevent injection
        # try:
        #     record = Record.objects.get(username=username,
        #                                 account=account)

        #     # update record if it exists
        #     record.password = password
        #     record.save()

        # except:
        #     Record.objects.create(username=username,
        #                           account=account,
        #                           password=password)

        return redirect('../')

    return render(request, 'pages/add.html')
