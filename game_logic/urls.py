from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('request_word_list', views.get_word_list, name='request_word_list'),
    path('gameplay/', views.gameplay, name='gameplay'),
] 