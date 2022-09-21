# Generated by Django 4.1 on 2022-09-12 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personal_financer', '0006_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashentry',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashentry', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stocktrxn',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocktrxn', to=settings.AUTH_USER_MODEL),
        ),
    ]