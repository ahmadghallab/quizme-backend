# Generated by Django 2.0.2 on 2019-01-16 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0020_result_answer_ids'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to='')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_files', to='quizzes.Question')),
            ],
        ),
    ]
