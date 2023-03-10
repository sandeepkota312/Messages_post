# Generated by Django 4.1.5 on 2023-01-20 11:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_remove_messages_likes_messages_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'ordering': ('-posted_date',)},
        ),
        migrations.AlterField(
            model_name='messages',
            name='likes',
            field=models.ManyToManyField(default=None, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
