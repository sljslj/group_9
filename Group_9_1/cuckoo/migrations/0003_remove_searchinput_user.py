# Generated by Django 2.1.4 on 2018-12-16 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuckoo', '0002_auto_20181216_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchinput',
            name='user',
        ),
    ]