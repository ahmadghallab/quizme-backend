# Generated by Django 2.0.2 on 2018-12-21 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20181220_1951'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('title', 'question')},
        ),
    ]