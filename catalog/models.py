from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=20, verbose_name='Жанр')

    def __str__(self):
        return self.name


class Director(models.Model):
    fname = models.CharField(max_length=20, verbose_name='Имя')
    lname = models.CharField(max_length=20, verbose_name='Фамилия')

    def __str__(self):
        return f'{self.fname} {self.lname}'

    def get_absolute_url(self):
        return reverse('infodirector', args=[self.id, self.lname])


class Actor(models.Model):
    fname = models.CharField(max_length=20, verbose_name='Имя')
    lname = models.CharField(max_length=20, verbose_name='Фамилия')
    born = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    country = models.CharField(max_length=20, blank=True, null=True, verbose_name='Страна')

    def __str__(self):
        return f'{self.fname} {self.lname}'

    def get_absolute_url(self):
        return reverse('infoactor', args=[self.id, f'{self.fname} {self.lname}'])


class Status(models.Model):
    choise = (('бесплатно', 'бесплатно'), ('базовая', 'базовая'), ('супер', 'супер'))
    name = models.CharField(max_length=20, choices=choise, verbose_name='Статус')

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=20, verbose_name='Страна')

    def __str__(self):
        return self.name


class AgeRate(models.Model):
    choise = (('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17'))
    rate = models.CharField(max_length=20, choices=choise, verbose_name='Возрастной рейтинг')

    def __str__(self):
        return self.rate


class Kino(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    genre = models.ForeignKey(Genre, on_delete=models.SET_DEFAULT, default=1, verbose_name='Жанр')
    rating = models.FloatField(verbose_name='Рейтинг')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Страна')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Режиссёр')
    summary = models.TextField(max_length=5000, verbose_name='Краткое описание')
    year = models.IntegerField(verbose_name='Год')
    ager = models.ForeignKey(AgeRate, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Возрастной рейтинг')
    actor = models.ManyToManyField(Actor, verbose_name='Актёры', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=1, verbose_name='Статус подписки')
    poster = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Ссылка на постер')

    def __str__(self):
        return self.title

    def display_actors(self):
        res = []
        for a in self.actor.all():
            res.append(a.lname)
        return ', '.join(res)
    display_actors.short_description = 'Актёры'


    def get_absolute_url(self):
        return reverse('info', args=[self.id])  #, self.title
        # return f'kino/{self.id}/{self.title}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата комментария')
    movie = models.ForeignKey(Kino, on_delete=models.CASCADE, verbose_name='Фильм')
