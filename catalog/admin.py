from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Genre)
# admin.site.register(Director)
# admin.site.register(Actor)
admin.site.register(AgeRate)
# admin.site.register(Status)
# admin.site.register(Kino)
admin.site.register(Country)

class Actoradmin(admin.ModelAdmin):
    list_display = ('lname', 'fname', 'born')
    list_display_links = ('lname', 'fname')
admin.site.register(Actor, Actoradmin)


class Diradmin(admin.ModelAdmin):
    list_display = ('lname', 'fname')
    list_display_links = ('lname', 'fname')
admin.site.register(Director, Diradmin)


class Kinoadmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'display_actors')
    list_filter = ('genre', 'status', 'rating')
    fieldsets = (('О фильме', {'fields': ('title', 'summary', 'actor')}),
                 ('Рейтинг', {'fields': ('rating', 'ager', 'status')}),
                 ('Остальное', {'fields': ('genre', 'year', 'country', 'director', 'poster')}))
admin.site.register(Kino, Kinoadmin)


class Stinline(admin.TabularInline):
    model = Kino


class Statusadmin(admin.ModelAdmin):
    inlines = [Stinline]
admin.site.register(Status, Statusadmin)