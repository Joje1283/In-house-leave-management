# Generated by Django 4.0.4 on 2022-06-04 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0001_initial'),
        ('grants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrantLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grants.grant')),
                ('leave', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='leaves.leave')),
            ],
        ),
    ]
