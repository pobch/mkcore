from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListRooms.as_view()),
    path('<int:pk>/', views.DetailRoom.as_view()),
    path('answers/', views.ListAnswers.as_view()),
    path('answers/<int:pk>/', views.DetailAnswer.as_view()),
]
