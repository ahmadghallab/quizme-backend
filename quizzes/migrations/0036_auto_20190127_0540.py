# Generated by Django 2.0.2 on 2019-01-27 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0035_auto_20190123_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(),
        ),
    ]