from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # path('request_word_list', views.get_word_list),
    path('', TemplateView.as_view(template_name='index.html')),
    path('request_word_list', views.get_word_list, name='get_word_list'),
]
