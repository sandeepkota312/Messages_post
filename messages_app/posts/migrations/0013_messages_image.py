# Generated by Django 4.2.2 on 2023-06-29 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='images/'),
        ),
    ]
