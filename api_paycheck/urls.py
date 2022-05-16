from django.urls import path
from api_paycheck import views
app_name = 'api_paycheck'

urlpatterns =[
   path('result/', views.pay_check.as_view()),
]