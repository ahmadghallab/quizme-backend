# Generated by Django 2.0.2 on 2019-02-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0040_auto_20190212_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(null=True),
        ),
    ]
