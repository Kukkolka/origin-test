# Generated by Django 2.1.7 on 2019-04-10 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0002_auto_20190410_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bonds',
            name='user',
        ),
    ]
