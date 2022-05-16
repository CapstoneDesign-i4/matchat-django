from django.urls import path
from matchat import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'matchat'

urlpatterns =[
   path('', views.main, name='main'),
   path('<int:product_id>/', views.detail, name='detail'),
   path('product/create/', views.product_create, name='product_create'),
   path('product/modify/<int:product_id>/', views.product_modify, name='product_modify'),
   path('product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
   path('product/reserve/<int:product_id>/', views.product_reserve, name='product_reserve'),
   path('product/reserve_delete/<int:product_id>/', views.product_reserve_delete, name='product_reserve_delete'),
   path('product/my/', views.product_my, name='my'),
   path('product/my/<int:product_id>/', views.my_detail, name='my_detail'),
   path('pay/<int:product_id>/', views.pay, name='pay'),
   path('pay/approval/', views.approval, name='approval'),
   path('pay/cancel/', views.cancel, name='cancel'),
   path('pay/fail/', views.fail, name='fail'),
]