# Generated by Django 2.1.7 on 2019-03-03 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0041_auto_20190216_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='classgroup',
            name='color',
            field=models.CharField(default='blue', max_length=10),
            preserve_default=False,
        ),
    ]
