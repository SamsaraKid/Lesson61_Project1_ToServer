# Generated by Django 4.2.5 on 2023-10-21 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата комментария'),
        ),
    ]