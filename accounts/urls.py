from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('',
        views.ListCreateUser.as_view(),
        name="user_list"),

    path('<int:pk>/',
        views.RetrieveUpdateDestroyUser.as_view(),
        name="user_detail"),

    path('api-token-auth/',
        views.CustomAuthToken.as_view(),
        name='token-auth'),
]
