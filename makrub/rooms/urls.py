from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListRooms.as_view()),
    path('<int:pk>/', views.DetailRoom.as_view()),
]
