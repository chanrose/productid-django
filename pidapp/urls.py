from django.urls import path
from . import views


app_name = 'pidapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
]
