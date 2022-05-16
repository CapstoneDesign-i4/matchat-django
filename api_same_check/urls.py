from django.urls import path
from api_same_check import views

app_name = 'api_same_check'

urlpatterns =[
   path('result/', views.Result.as_view()),
]