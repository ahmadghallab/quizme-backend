import datetime
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import ValidationError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from . import models
from . import serializers

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 1

# Custom Permissions
class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            if request.method == 'DELETE':
                return False

# ClassGroupes View
class ListCreateClassGroup(generics.ListCreateAPIView):
    queryset = models.ClassGroup.objects.all()
    serializer_class = serializers.ClassGroupSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.kwargs.get('user_pk'))


class ListClassGroup(APIView):
    def get(self, request, level_pk, format=None):
        classes = models.ClassGroup.objects.values(
            'id', 'title'
        ).annotate(
            joined=Count(
            'class_students__pk',
            filter=Q(class_students__student=request.query_params.get('student')))
        ).annotate(
            total_quizzes=Count('quizzes__pk', distinct=True)
        ).filter(level=level_pk)
        return Response(classes)

class DestroyStudentClassGroup(APIView):
    def delete(self, request, class_pk, student_pk, format=None):
        student_class = models.StudentClassGroup.objects.filter(class_group=class_pk, student=student_pk)
        student_class.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveUpdateDestroyClassGroup(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClassGroup.objects.all()
    serializer_class = serializers.ClassGroupSerializer

# Quizzes View
class ListTodayQuiz(APIView):
    def get(self, request, user_pk, format=None):
        student_classes = [e.class_group for e in models.StudentClassGroup.objects.filter(student=user_pk)]

        quizzes = models.Quiz.objects.values(
            'pk','name','class__title'
        ).filter(
            due_date=datetime.date.today(),
            class__pk__in=student_classes
        ).annotate(
            total_questions=Count('questions__pk', distinct=True),
        ).annotate(
            total_questions_answered=Count(
                'quiz_results__question',
                distinct=True,
                filter=Q(quiz_results__student=user_pk))
        )
        return Response(quizzes)

class CreateStudentClassGroup(generics.CreateAPIView):
    serializer_class = serializers.StudentClassGroupSerializer


class ListStudentClassGroup(APIView):
    def get(self, request, format=None):
        if self.request.query_params.get('student'):
            results = models.StudentClassGroup.objects.values(
                'pk', 'class__title'
            ).filter(student=request.query_params.get('student'))

        if self.request.query_params.get('class'):
            results = models.StudentClassGroup.objects.values(
                'pk', 'student__email'
            ).filter(class_group=request.query_params.get('class'))

        return Response(results)

class ListCreateQuiz(generics.ListCreateAPIView):
    permission_classes = (
        # IsSuperUser,
        permissions.DjangoModelPermissions,
    )
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer

    def get_queryset(self):
        return self.queryset.filter(class_group=self.kwargs.get('class_pk'))

class RetrieveUpdateDestroyQuiz(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.DjangoModelPermissions,)
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer

# Questions View
class ListCreateQuestion(generics.ListCreateAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        return self.queryset.filter(quiz_id=self.kwargs.get('quiz_pk'))

    def perform_create(self, serializer):
        quiz = get_object_or_404(models.Quiz, pk=self.kwargs.get('quiz_pk'))
        serializer.save(quiz=quiz, mark_divided=self.request.data.get('mark'))


class RetrieveUpdateDestroyQuestion(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionsAnswersSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs.get('pk')
        )

class UpdateQuestionFile(generics.UpdateAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_update(self, serializer):
        if self.request.data['file'] == '':
            file = models.Question.objects.values('file').filter(pk=self.kwargs.get('pk'))[0]
            os.remove(os.path.join(settings.MEDIA_ROOT, file['file']))
        serializer.save()

# Answers View
class ListCreateAnswer(generics.ListCreateAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        return self.queryset.filter(question_id=self.kwargs.get('question_pk'))

    def perform_create(self, serializer):
        question = get_object_or_404(
            models.Question,
            pk=self.kwargs.get('question_pk'))

        serializer.save(question=question)


class RetrieveUpdateDestroyAnswer(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


    def perform_update(self, serializer):
        if self.request.data['question_type']:
            if self.request.data['question_type'] == 'ma':
                self.queryset.filter(
                    pk=self.kwargs.get('pk')
                ).update(correct=self.request.data['correct'])
            else:
                self.queryset.filter(
                    question=self.request.data['question'],
                ).exclude(
                    pk=self.kwargs.get('pk')
                ).update(correct=False)

        serializer.save()

# Assessment View
class ListQuestionsAnswersResults(generics.ListAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionsAnswersResultsSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        quiz_question_order = models.Quiz.objects.values('question_order').get(id=self.kwargs.get('quiz_pk'))
        return self.queryset.filter(
                quiz_id=self.kwargs.get('quiz_pk')
            ).order_by(quiz_question_order['question_order'])


class DoNotKnowResult(generics.CreateAPIView):
    serializer_class = serializers.DoNotKnowSerializer

class MultipleChoiceResult(generics.CreateAPIView):
    serializer_class = serializers.MultipleChoiceSerializer
    def perform_create(self, serializer):
        answer_result = get_object_or_404(
            models.Answer,
            question_id=self.request.data['question'],
            pk=self.request.data['answer']
        )
        serializer.save(correct=answer_result.correct)

class MultipleAnswerResult(generics.CreateAPIView):
    serializer_class = serializers.MultipleAnswerSerializer

    def perform_create(self, serializer):
        student_answers = self.request.data['answers']
        student_answers_str = ','.join(str(e) for e in student_answers)
        correct_answers = [answer['id'] for answer in models.Answer.objects.values('id').filter(question_id=self.request.data['question'], correct=True)]

        if set(student_answers) == set(correct_answers):
            serializer.save(correct=True, answer_text=student_answers_str)
        else:
            serializer.save(correct=False, answer_text=student_answers_str)

class EnumerateResult(APIView):
    def post(self, request, format=None):
        student_answer = self.request.data.get('answers')
        correct_answer = [
            answer['title'].replace(', ', ',').split(',') for answer in models.Answer.objects.values('title').filter(
            question_id=self.request.data.get('question'))
        ]
        response = []
        for answer in student_answer:
            obj = models.Result()
            obj.quiz_id=self.request.data.get('quiz')
            obj.question_id=self.request.data.get('question')
            obj.student_id=self.request.data.get('student')
            if answer in [elem for sublist in correct_answer for elem in sublist]:
                obj.correct=True
                response.append(True)
                correct_answer = [item for item in correct_answer if answer not in item]
            else:
                obj.correct=False
                response.append(False)
            obj.answer_text=answer
            obj.save()
        return Response(response, status=status.HTTP_201_CREATED)

class FillBlankResult(APIView):
    def post(self, request, format=None):
        student_answer = self.request.data.get('answers')
        correct_answer = [
            answer['title'].replace(', ', ',').split(',') for answer in models.Answer.objects.values('title').filter(
            question_id=self.request.data.get('question'))
        ]
        response = []
        for s, c in zip(student_answer, correct_answer):
            obj = models.Result()
            obj.quiz_id=self.request.data.get('quiz')
            obj.question_id=self.request.data.get('question')
            obj.student_id=self.request.data.get('student')
            if s in c:
                obj.correct=True
                response.append(True)
            else:
                obj.correct=False
                response.append(False)
            obj.answer_text=s
            obj.save()
        return Response(response, status=status.HTTP_201_CREATED)


class ListResult(APIView):
    def get(self, request, quiz_pk, format=None):
        quiz = models.Quiz.objects.values(
            'name', 'class__title'
        ).annotate(
            total_mark=Sum('questions__mark')
        ).get(pk=quiz_pk)

        result = models.Result.objects.values(
            'student','student__first_name','student__last_name'
        ).filter(quiz=quiz_pk).distinct().annotate(
            mark=Sum('question__mark_divided', filter=Q(correct=True))
        )
        return Response({
            'result': result,
            'quiz': quiz
        })

class ListAssessmentResult(APIView):
    def get(self, request, quiz_pk, student_pk, format=None):
        quiz = models.Quiz.objects.values(
            'name', 'class__title', total_mark=Sum('questions__mark')
        ).get(pk=quiz_pk)

        result = models.Result.objects.filter(
            quiz=quiz_pk,
            student=student_pk
        ).aggregate(
            student_mark=Sum('question__mark_divided', filter=Q(correct=True)),
            correct_answers=Count('pk', filter=Q(correct=True)),
            incorrect_answers=Count('pk', filter=Q(correct=False)),
            do_not_know=Count('pk', filter=Q(do_not_know=True))
        )

        return Response({
            'result': result,
            'quiz': quiz
        })
