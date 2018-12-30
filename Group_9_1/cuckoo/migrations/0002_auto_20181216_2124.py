# Generated by Django 2.1.4 on 2018-12-16 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cuckoo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make_in', models.CharField(max_length=200)),
                ('movie_boxOffice', models.CharField(max_length=200)),
                ('movie_directors', models.CharField(max_length=200)),
                ('movie_name_chi', models.CharField(max_length=200)),
                ('movie_name_eng', models.CharField(max_length=200)),
                ('movie_releaseDate', models.CharField(max_length=200)),
                ('movie_score', models.CharField(max_length=20)),
                ('movie_stars_all', models.CharField(max_length=200)),
                ('movie_timeLength', models.CharField(max_length=200)),
                ('movie_type', models.CharField(max_length=200)),
                ('movie_url_index', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SearchInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_input', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=200)),
                ('movie_score', models.CharField(max_length=20)),
                ('search_input', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuckoo.SearchInput')),
            ],
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='searchinput',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]