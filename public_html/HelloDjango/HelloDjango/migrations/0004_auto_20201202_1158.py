# Generated by Django 3.1.2 on 2020-12-02 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HelloDjango', '0003_auto_20201202_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricelist',
            old_name='сategory',
            new_name='category',
        ),
    ]
