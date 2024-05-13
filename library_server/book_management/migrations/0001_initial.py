# Generated by Django 5.0.4 on 2024-05-13 09:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISBN', models.CharField(max_length=255, unique=True)),
                ('availability', models.BooleanField(default=True)),
                ('bookCover', models.TextField()),
                ('bookGenres', models.TextField()),
                ('bookPlot', models.TextField()),
                ('bookTitle', models.CharField(max_length=255)),
                ('bookAuthor', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=30)),
                ('numOfPages', models.PositiveIntegerField()),
                ('publishDate', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowDate', models.DateField()),
                ('returnDate', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_management.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]