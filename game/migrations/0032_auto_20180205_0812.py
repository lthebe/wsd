# Generated by Django 2.0 on 2018-02-05 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0031_game_popularity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameplayed',
            name='users',
        ),
        migrations.AddField(
            model_name='gameplayed',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='game_played',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.GamePlayed'),
        ),
    ]