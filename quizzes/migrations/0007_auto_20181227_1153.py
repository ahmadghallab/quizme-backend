# Generated by Django 2.0.2 on 2018-12-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_remove_question_model_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='fill_answer',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='question',
            name='true_or_false',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
