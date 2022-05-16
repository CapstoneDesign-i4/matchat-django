from django.urls import path
from api_finish import views

app_name = 'api_finish'

urlpatterns =[
   path('result/', views.Result.as_view()),
]