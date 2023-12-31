# Generated by Django 4.2.5 on 2023-10-21 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_kino_country_alter_kino_director'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=20, verbose_name='Автор')),
                ('text', models.TextField(max_length=500, verbose_name='Текст комментария')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.kino', verbose_name='Фильм')),
            ],
        ),
    ]
