# Generated by Django 2.0.2 on 2019-01-23 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0032_auto_20190123_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='mark_divided',
            field=models.FloatField(null=True),
        ),
    ]
