# Generated by Django 2.0.2 on 2018-12-31 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0011_auto_20181230_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answer_results', to='quizzes.Answer'),
            preserve_default=False,
        ),
    ]
