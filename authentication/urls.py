from django.urls import path
from authentication import views

urlpatterns = [
    path('users/signup/', views.UserSignup.as_view())
]

