from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListAccounts.as_view()),
    path('<int:pk>/', views.DetailAccount.as_view()),
]
