# Generated by Django 2.0 on 2018-01-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20180107_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='upload_date',
            field=models.DateTimeField(),
        ),
    ]