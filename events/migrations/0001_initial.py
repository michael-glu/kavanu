# Generated by Django 3.1.3 on 2020-12-03 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('image', models.ImageField(upload_to=events.models.upload_location)),
                ('min_attendees', models.IntegerField()),
                ('max_attendees', models.IntegerField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
