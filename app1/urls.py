from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user-form', views.assignment, name='assignment'),
    path('list-of-all-submitted-forms', views.forms, name='forms'),
    
] 