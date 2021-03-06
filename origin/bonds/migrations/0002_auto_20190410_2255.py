# Generated by Django 2.1.7 on 2019-04-10 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bonds', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bonds',
            options={'verbose_name': 'Bond', 'verbose_name_plural': 'Bonds'},
        ),
        migrations.AddField(
            model_name='bonds',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bonds',
            name='maturity',
            field=models.DateField(auto_now_add=True, verbose_name='Date Created'),
        ),
    ]
