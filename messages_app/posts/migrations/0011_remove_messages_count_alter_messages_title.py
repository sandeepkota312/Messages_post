# Generated by Django 4.1.5 on 2023-03-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_messages_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='count',
        ),
        migrations.AlterField(
            model_name='messages',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]