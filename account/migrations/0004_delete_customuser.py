# Generated by Django 4.2.3 on 2023-07-20 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]