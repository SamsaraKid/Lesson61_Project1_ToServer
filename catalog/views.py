from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User


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

from django.views import generic
class Kinolist(generic.ListView):
    model = Kino
    paginate_by = 2

# from django.http import HttpResponse
# def info(req, id):
#     film = Kino.objects.get(id=id)
#     return HttpResponse(film.title)

class KinoDetail(generic.DetailView):
    model = Kino