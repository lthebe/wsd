# Generated by Django 2.0 on 2018-01-04 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20180104_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameplayed',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Game'),
        ),
        migrations.AlterField(
            model_name='gameplayed',
            name='gameState',
            field=models.TextField(default="{''}"),
        ),
    ]