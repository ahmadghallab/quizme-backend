from django.db import models
from accounts import models as accounts_models

class ClassGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    color = models.CharField(max_length=10)
    user = models.ForeignKey(accounts_models.User, related_name='classes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['title', 'user']
        verbose_name_plural = "classes"

class Quiz(models.Model):
    title = models.CharField(max_length=255, unique=True)
    class_group = models.ForeignKey(ClassGroup, related_name="quizzes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateField(null=True)
    question_order = models.CharField(max_length=25, default='order')
    default_mark = models.FloatField(default=1)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['title', 'class_group']
        verbose_name_plural = "quizzes"

class Question(models.Model):
    title = models.TextField(null=True)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    type = models.CharField(max_length=3)
    mark = models.FloatField(null=True)
    mark_divided = models.FloatField(null=True)
    file = models.FileField(null=True, blank=True)

    class Meta:
        unique_together = ['title', 'quiz']

    def __str__(self):
        return self.title

class Answer(models.Model):
    title = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    correct = models.NullBooleanField()

    class Meta:
        unique_together = ['title', 'question']

    def __str__(self):
        return self.title

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_results', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='results', on_delete=models.CASCADE)
    student = models.ForeignKey(accounts_models.User, related_name='user_results', on_delete=models.CASCADE)
    correct = models.NullBooleanField()
    do_not_know = models.NullBooleanField()
    answer = models.ForeignKey(Answer, related_name='answer_results', on_delete=models.CASCADE, null=True)
    answer_text = models.CharField(max_length=255, null=True)


class StudentClassGroup(models.Model):
    student = models.ForeignKey(accounts_models.User, related_name='student_classes', on_delete='models.CASCADE')
    class_group = models.ForeignKey(ClassGroup, related_name='class_students', on_delete='models.CASCADE')
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'class_group']
