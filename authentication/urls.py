from django.urls import path
from authentication import views

urlpatterns = [
    path('signup', views.UserSignup.as_view()),
    path('login', views.UserLogin.as_view()),
    path('save_progress', views.SaveProgress.as_view()),
    path('next_level', views.NextLevel.as_view()),
]