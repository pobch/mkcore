from django.urls import path
from . import views


urlpatterns = [
    path('rooms/', views.ListRooms.as_view()),
    path('rooms/<int:pk>/', views.DetailRoom.as_view()),
    path('answers/', views.ListAnswers.as_view()),
    path('answers/<int:pk>/', views.DetailAnswer.as_view()),
]
