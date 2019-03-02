from django.db.models import Count

from rest_framework import serializers

from . import models

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'question', 'correct')
        model = models.Answer

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('uploaded_at', 'question', 'datafile')
        model = models.File

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'quiz', 'order', 'type', 'mark', 'mark_divided', 'file')
        model = models.Question

class QuestionAndAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'title', 'quiz', 'order', 'type', 'mark', 'mark_divided', 'answers', 'file')
        model = models.Question

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    total_questions = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'title', 'created_at',
            'questions', 'total_questions',
            'class_group', 'due_date', 'default_mark', 'question_order'
        )
        model = models.Quiz

    def get_total_questions(self, obj):
        total = obj.questions.aggregate(Count('id')).get('id__count')
        if total is None:
            return 0
        return total

class MultipleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','quiz','question','student','correct', 'answer')
        model = models.Result

class MultipleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','quiz','question','student','correct', 'answer_text')
        model = models.Result

class DoNotKnowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','quiz','question','student','do_not_know')
        model = models.Result


class FilteredResultSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(student=self.context['request'].query_params.get('student'))
        return super(FilteredResultSerializer, self).to_representation(data)

class QuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredResultSerializer
        fields = ('answer', 'correct', 'answer_text', 'do_not_know')
        model = models.Result

class QuestionAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    question_results = QuestionResultSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'title', 'quiz', 'order', 'type', 'mark', 'file', 'answers', 'question_results')
        model = models.Question

class ClassGroupSerializer(serializers.ModelSerializer):
    total_quizzes = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'title', 'description', 'user', 'total_quizzes')
        model = models.ClassGroup

    def get_total_quizzes(self, obj):
        total = obj.quizzes.aggregate(Count('id')).get('id__count')
        if total is None:
            return 0
        return total


class StudentClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'student', 'class_group')
        model = models.StudentClassGroup
