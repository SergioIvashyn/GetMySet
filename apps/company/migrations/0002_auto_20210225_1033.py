# Generated by Django 3.0.7 on 2021-02-25 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='logos'),
        ),
    ]