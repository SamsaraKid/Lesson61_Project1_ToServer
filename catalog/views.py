from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User, Group
from django.views import generic
import datetime
from .seleniumkp import getmovies

def index(req):
    numkino = Kino.objects.all().count()
    numactor = Actor.objects.all().count()
    numfree = Kino.objects.filter(status_id=1).count()
    usid = req.user.id  # находим номер текущего пользователя
    user = User.objects.get(id=usid)  # находим его номер в таблице user
    statusnow = user.groups.all()[0]  # находим номер его подписки (группы)
    # username = req.user.first_name if hasattr(req.user, 'first_name') else 'Guest'
    try:
        username = req.user.first_name
    except:
        username = 'Guest'
    data = {'k1': numkino, 'k2': numactor, 'k3': numfree, 'username': username, 'k4': statusnow}
    # user = User.objects.create_user('user2', 'user2@mail.ru', 'useruser')
    # user.first_name = 'Vlad'
    # user.last_name = 'Petrov'
    # user.save()
    # try:
    #     a = Actor.objects.get(fname='Гоша', lname='Куценко').id
    #     print(a)
    # except:
    #     print(False)
    # getmovies()

    return render(req, 'index.html', context=data)


# def allkino(req):
#     return render(req, 'index.html')


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
    mas = ['бесплатно', 'базовая', 'супер']  # kino id2
    mas2 = ['Free', 'Based', 'Super']  # user id3
    status = 0
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


def buy(req, type):
    usid = req.user.id  # находим номер текущего пользователя
    user = User.objects.get(id=usid)  # находим его номер в таблице user
    statusnow = user.groups.all()[0].id  # находим номер его подписки (группы)
    groupold = Group.objects.get(id=statusnow)  # находим эту подписку в таблице group
    groupold.user_set.remove(user)  # удаляем старую подписку
    groupnew = Group.objects.get(id=type)  # находим новую подписку в таблице group
    groupnew.user_set.add(user)  # добавляем новую подписку
    k1 = groupnew.name  # узанём название подписки для вывода
    data = {'podpiska': k1}
    return render(req, 'buy.html', context=data)