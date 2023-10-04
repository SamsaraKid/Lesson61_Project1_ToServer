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


class ActorDetail(generic.DetailView):
    model = Actor