# Generated by Django 2.2.16 on 2022-09-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_user_extended'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=None, null=True, verbose_name='Rating'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=10, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Id_Category'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Id_Genre'),
        ),
    ]
