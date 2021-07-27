from django.urls import path
from . import views


app_name = 'pidapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('register_product', views.RegisterProduct.as_view(), name='register_product'),
    path('view_product/<str:prod_pk>', views.ViewProduct.as_view(), name='view_product'),
    path('edit_product/<str:prod_pk>', views.EditProduct.as_view(), name="edit_product"),
    path('validate_product', views.validate_product, name='validate_product'),
]
