# Generated by Django 2.0.2 on 2018-12-20 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('correct', 'question'), ('title', 'question')},
        ),
    ]
