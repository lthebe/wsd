# Generated by Django 2.0 on 2018-01-03 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_merge_20180103_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='viewcount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]