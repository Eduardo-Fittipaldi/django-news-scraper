# Generated by Django 3.1.3 on 2020-11-06 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newspaper_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=50)),
                ('pub_day', models.DateField()),
                ('link', models.URLField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news_scraper.author')),
                ('newspaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_scraper.newspaper')),
            ],
        ),
    ]
