# Generated by Django 4.2.5 on 2023-10-07 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_kino_posterstatic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kino',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='kino',
            name='posterstatic',
        ),
        migrations.AddField(
            model_name='kino',
            name='posterlink',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на постер'),
        ),
        migrations.AlterField(
            model_name='kino',
            name='actor',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.actor', verbose_name='Актёры'),
        ),
        migrations.AlterField(
            model_name='kino',
            name='ager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.agerate', verbose_name='Возрастной рейтинг'),
        ),
    ]
