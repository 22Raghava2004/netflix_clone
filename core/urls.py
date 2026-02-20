from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('add-to-list/', views.add_to_list, name='add-to-list'),
]
