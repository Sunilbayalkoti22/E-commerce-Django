# Generated by Django 4.0.4 on 2022-04-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='grand_total',
            field=models.IntegerField(default=0),
        ),
    ]
