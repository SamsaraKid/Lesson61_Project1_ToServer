from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.views import generic


def index(req):
    numkino = Kino.objects.all().count()
    numactor = Actor.objects.all().count()
    numfree = Kino.objects.filter(status__kino=1).count()
    # username = req.user.first_name if hasattr(req.user, 'first_name') else 'Guest'
    try:
        username = req.user.first_name
    except:
        username = 'Guest'
    data = {'k1': numkino, 'k2': numactor, 'k3': numfree, 'username': username}
    # user = User.objects.create_user('user2', 'user2@mail.ru', 'useruser')
    # user.first_name = 'Vlad'
    # user.last_name = 'Petrov'
    # user.save()
    return render(req, 'index.html', context=data)


# def allkino(req):
#     return render(req, 'index.html')


class Kinolist(generic.ListView):
    model = Kino
    paginate_by = 2

# from django.http import HttpResponse
# def info(req, id):
#     film = Kino.objects.get(id=id)
#     return HttpResponse(film.title)

class KinoDetail(generic.DetailView):
    model = Kino


class Actorlist(generic.ListView):
    model = Actor


class DirectorDetail(generic.DetailView):
    model = Director


class Directorlist(generic.ListView):
    model = Director


class ActorDetail(generic.DetailView):
    model = Actor


def status(req):
    k1 = Status.objects.all()
    data = {'podpiska': k1}
    return render(req, 'podpiska.html', data)


def prosmotr(req, id1, id2, id3):
    print(id1, id2, id3)
    mas = ['бесплатно', 'базовая', 'супер']  # kino id2
    mas2 = ['Free', 'Based', 'Super']  # user id3
    podp = User.objects.get(id=id3).groups.all()[0].id
    print(podp)
    if id3 == 0:
        podp = 1
    if podp >= id2:
        print('can watch')
    else:
        print('can\'t watch')
    return render(req, 'index.html')