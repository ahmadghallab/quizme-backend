# Generated by Django 2.0.2 on 2018-12-24 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_auto_20181222_1827'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('title', 'question')},
        ),
    ]
