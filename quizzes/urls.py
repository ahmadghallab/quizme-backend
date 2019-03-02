from django.urls import path
from django.conf import settings
from django.views.static import serve

from . import views

app_name = 'apiv1'

urlpatterns = [
    path('users/<int:user_pk>/classes/',
        views.ListCreateClassGroup.as_view(),
        name='class_list'),

    path('join/',
        views.CreateStudentClassGroup.as_view(),
        name='student_class_create'),

    path('leave/class/<int:class_pk>/student/<int:student_pk>/',
        views.DestroyStudentClassGroup.as_view(),
        name='student_class_delete'),

    path('studentclass/',
        views.ListStudentClassGroup.as_view(),
        name='student_class_list'),

    path('classes/<int:pk>/',
        views.RetrieveUpdateDestroyClassGroup.as_view(),
        name='class_detail'),

    path('classes/<int:class_pk>/quizzes/',
        views.ListCreateQuiz.as_view(),
        name='quiz_list'),

    path('quizzes/<int:pk>/',
        views.RetrieveUpdateDestroyQuiz.as_view(),
        name='quiz_detail'),

    path('users/<int:user_pk>/today/',
        views.ListTodayQuiz.as_view(),
        name='today_quizzes'),

    path('quizzes/<int:quiz_pk>/questions/',
        views.ListCreateQuestion.as_view(),
        name='question_list'),
    path('questions/<int:pk>/',
        views.RetrieveUpdateDestroyQuestion.as_view(),
        name='question_detail'),
    path('questions/<int:pk>/file/',
        views.UpdateQuestionFile.as_view(),
        name='question_file'),

    path('questions/<int:question_pk>/answers/',
        views.ListCreateAnswer.as_view(),
        name='answer_list'),
    path('answers/<int:pk>/',
        views.RetrieveUpdateDestroyAnswer.as_view(),
        name='answer_detail'),

    path('quizzes/<int:quiz_pk>/assessment/',
        views.ListQuestionWithAnswers.as_view(),
        name='assessment'),

    path('quizzes/<int:quiz_pk>/results/',
        views.ListResult.as_view(),
        name='result_list'),

    path('quizzes/<int:quiz_pk>/student/<int:student_pk>/results/',
        views.ListAssessmentResult.as_view(),
        name='assessment_result_list'),

    path('results/multiplechoice/',
        views.MultipleChoiceResult.as_view(),
        name="result_multiplechoice"),

    path('results/multipleanswer/',
        views.MultipleAnswerResult.as_view(),
        name="result_multipleanswer"),

    path('results/enumerate/',
        views.EnumerateResult.as_view(),
        name="result_enumerate"),

    path('results/fillblank/',
        views.FillBlankResult.as_view(),
        name="result_fillblank"),

    path('results/donotknow/',
        views.DoNotKnowResult.as_view(),
        name="result_donotknow"),

    path('files/questions/<int:question_pk>/',
        views.ListCreateFile.as_view(),
        name="file_list"),

    path('static/<path>', serve, {'document_root': settings.MEDIA_ROOT,}),
]
