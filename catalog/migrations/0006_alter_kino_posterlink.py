# Generated by Django 4.2.5 on 2023-10-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_remove_kino_poster_remove_kino_posterstatic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kino',
            name='posterlink',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Ссылка на постер'),
        ),
    ]