# Generated by Django 3.1.2 on 2020-12-01 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HelloDjango', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='photo',
            new_name='picture',
        ),
    ]
