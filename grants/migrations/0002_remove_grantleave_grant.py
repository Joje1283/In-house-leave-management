# Generated by Django 4.0.4 on 2022-06-05 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grantleave',
            name='grant',
        ),
    ]
