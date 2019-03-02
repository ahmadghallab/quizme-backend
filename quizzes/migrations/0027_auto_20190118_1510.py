# Generated by Django 2.0.2 on 2019-01-18 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0026_auto_20190117_1008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='answer_ids',
            new_name='student_answer',
        ),
        migrations.AlterField(
            model_name='file',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='quizzes.Question'),
        ),
        migrations.AlterField(
            model_name='result',
            name='correct',
            field=models.NullBooleanField(),
        ),
    ]