# Generated by Django 5.1.5 on 2025-01-23 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0008_comment_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='like_count',
        ),
    ]
