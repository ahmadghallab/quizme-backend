# Generated by Django 2.0.2 on 2018-12-25 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_auto_20181224_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='model_answer',
        ),
    ]
