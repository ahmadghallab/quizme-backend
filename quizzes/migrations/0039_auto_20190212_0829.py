# Generated by Django 2.0.2 on 2019-02-12 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0038_auto_20190211_0713'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'classes',
            },
        ),
        migrations.CreateModel(
            name='StudentClassGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('class_group', models.ForeignKey(on_delete='models.CASCADE', related_name='class_students', to='quizzes.ClassGroup')),
                ('student', models.ForeignKey(on_delete='models.CASCADE', related_name='student_classes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='level',
        ),
        migrations.AlterUniqueTogether(
            name='studentcourse',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='studentcourse',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentcourse',
            name='student',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='name',
            new_name='title',
        ),
        migrations.DeleteModel(
            name='Level',
        ),
        migrations.DeleteModel(
            name='StudentCourse',
        ),
        migrations.AddField(
            model_name='quiz',
            name='class_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='quizzes.ClassGroup'),
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.AlterUniqueTogether(
            name='quiz',
            unique_together={('title', 'class_group')},
        ),
        migrations.AlterUniqueTogether(
            name='studentclassgroup',
            unique_together={('student', 'class_group')},
        ),
        migrations.AlterUniqueTogether(
            name='classgroup',
            unique_together={('title', 'user')},
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]