from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.views import generic
from .form import SignUp
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import datetime
from .seleniumkp import getmovies

def index(req):
    numkino = Kino.objects.all().count()
    numactor = Actor.objects.all().count()
    numfree = Kino.objects.filter(status_id=1).count()
    # username = req.user.first_name if hasattr(req.user, 'first_name') else 'Guest'
    data = {'k1': numkino, 'k2': numactor, 'k3': numfree}
    # user = User.objects.create_user('user2', 'user2@mail.ru', 'useruser')
    # user.first_name = 'Vlad'
    # user.last_name = 'Petrov'
    # user.save()
    # getmovies()
    return render(req, 'index.html', context=data)


class Kinolist(generic.ListView):
    model = Kino
    paginate_by = 30

# from django.http import HttpResponse
# def info(req, id):
#     film = Kino.objects.get(id=id)
#     return HttpResponse(film.title)

class KinoDetail(generic.DetailView):
    model = Kino


class Actorlist(generic.ListView):
    model = Actor
    paginate_by = 30


class ActorDetail(generic.DetailView):
    model = Actor


class Directorlist(generic.ListView):
    model = Director
    paginate_by = 30


class DirectorDetail(generic.DetailView):
    model = Director


def status(req):
    k1 = Status.objects.all()
    data = {'podpiska': k1}
    return render(req, 'podpiska.html', data)


def prosmotr(req, id1, id2, id3):
    print(id1, id2, id3)
    if id3 != 0:
        status = User.objects.get(id=id3)  # нашли юзера
        status = status.groups.all()  # нашли его подписки
        status = status[0].id  #  нашли id его подписки
    else:
        status = 1  # выдаём гостю подписку free
    if status >= id2:  # сравниваем статус пользователя и подписку фильма
        print('can watch')
        permission = True
    else:
        print('can\'t watch')
        permission = False
    k1 = Kino.objects.get(id=id1).title
    k2 = Group.objects.get(id=status).name
    k3 = Status.objects.get(id=id2).name
    data = {'kino': k1, 'status': k2, 'statuskino': k3, 'prava': permission}
    return render(req, 'prosmotr.html', context=data)


def changestatus(req, type):
    usid = req.user.id  # находим номер текущего пользователя
    user = User.objects.get(id=usid)  # находим его номер в таблице user
    statusnow = user.groups.all()[0].id  # находим номер его подписки (группы)
    groupold = Group.objects.get(id=statusnow)  # находим эту подписку в таблице group
    groupold.user_set.remove(user)  # удаляем старую подписку
    groupnew = Group.objects.get(id=type)  # находим новую подписку в таблице group
    groupnew.user_set.add(user)  # добавляем новую подписку
    k1 = groupnew.name  # узанём название подписки для вывода
    return redirect('lk')


def registr(req):
    if req.POST:
        anketa = SignUp(req.POST)
        if anketa.is_valid():
            anketa.save()
            name = anketa.cleaned_data.get('username')
            password = anketa.cleaned_data.get('password1')
            fname = anketa.cleaned_data.get('first_name')
            lname = anketa.cleaned_data.get('last_name')
            email = anketa.cleaned_data.get('email')
            user = authenticate(username=name, password=password)
            man = User.objects.get(username=name)
            man.first_name = fname
            man.last_name = lname
            man.email = email
            man.save()
            login(req, user)
            group = Group.objects.get(id=1)
            group.user_set.add(man)
            return redirect('home')
    else:
        anketa = SignUp()
    data = {'regform': anketa}
    return render(req, 'registration/registration.html', context=data)


def lk(req):
    try:
        username = req.user.first_name
        usid = req.user.id  # находим номер текущего пользователя
        user = User.objects.get(id=usid)  # находим его номер в таблице user
        statusnow = str(user.groups.all()[0])  # находим номер его подписки (группы)
    except:
        username = 'Guest'
        statusnow = Group.objects.get(id=1).name
    data = {'username': username, 'statusnow': statusnow}
    return render(req, 'registration/lk.html', context=data)
