# Generated by Django 3.1.7 on 2021-02-26 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0002_auto_20210225_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='notes',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='project',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('name', 'user_id')},
        ),
    ]
