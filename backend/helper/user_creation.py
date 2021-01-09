from django.contrib.auth.models import User
from .email import send_external_registration_mail, send_auth_mail


def RegisterUser(email, password, first_name, last_name):
    user = User.objects.create_user(email,
                                    email=email,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name)
    return user


def login_or_create_user(data):
    user = User.objects.filter(email=data['email']).first()
    if user is None:
        user = RegisterUser(data['email'], data['password'], data['first_name'], data['last_name'])
        data['newly_registered'] = True
        data['username'] = data['email'].split('@', 1)[0]
        data['user'] = user.email
    else:
        user.set_password(data['password'])
        data['username'] = user.userextended.scout_name
        data['user'] = user.email
        data['newly_registered'] = False
        user.save()

    send_auth_mail(data)
    return data


def CreateUserExternally(email):
    password = User.objects.make_random_password()
    RegisterUser(email, password, '', '')
    data = {'username': email.split('@', 1)[0],
            'user': email,
            'email': email,
            'password': password}
    send_external_registration_mail(data)

