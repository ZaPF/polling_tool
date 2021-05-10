from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.open_polls, name='open_polls'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
]
