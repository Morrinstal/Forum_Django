# Generated by Django 5.1.4 on 2025-01-22 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0003_category_post_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author_avatar',
        ),
    ]
