from django.urls import path

from question import views

app_name = 'question'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.QuestionView.as_view(), name='detail'),
    path('ask/', views.ask_questin, name='ask'),
    path('answer/<int:qid>', views.write_answer, name='answer'),
]
