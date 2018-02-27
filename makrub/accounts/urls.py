from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListAccounts.as_view()),
    path('signup', views.Signup.as_view()),
    path('login', views.Login.as_view()),
    path('<int:pk>/', views.DetailAccount.as_view()),
]
