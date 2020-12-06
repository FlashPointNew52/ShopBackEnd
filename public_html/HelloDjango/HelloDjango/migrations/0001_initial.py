# Generated by Django 3.1.2 on 2020-12-01 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Код')),
                ('section', models.CharField(blank=True, max_length=40, verbose_name='Секция')),
                ('subsection', models.CharField(blank=True, max_length=40, verbose_name='Подгруппа')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('producer', models.CharField(max_length=100, null=True, verbose_name='Производитель')),
                ('flavor', models.CharField(max_length=100, null=True, verbose_name='Вкус')),
                ('age', models.CharField(max_length=100, null=True, verbose_name='Возраст')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Скидка')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='static/images/categoryImage', verbose_name='Изображение')),
            ],
        ),
        migrations.CreateModel(
            name='Pricelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('option', models.CharField(blank=True, max_length=200, null=True, verbose_name='Опция')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('count', models.IntegerField(verbose_name='Кол-во')),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Скидка')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pricelists', to='HelloDjango.category', verbose_name='Группа')),
            ],
        ),
    ]