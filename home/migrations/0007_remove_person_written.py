# Generated by Django 3.0.2 on 2020-06-10 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200611_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='written',
        ),
    ]
