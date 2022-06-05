# Generated by Django 4.0.4 on 2022-06-05 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='consume',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='is_all_day',
            field=models.BooleanField(default=True, verbose_name='연차 여부'),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_date',
            field=models.DateField(null=True, verbose_name='휴가 종료일'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_date',
            field=models.DateField(null=True, verbose_name='휴가 시작일'),
        ),
    ]