from django.urls import path

from .views import RoomAnswerExportView, ForTest


urlpatterns = [
    path('answers/', RoomAnswerExportView.as_view()), # e.g., + ?format=xlsx&room_id=34
    path('test/', ForTest.as_view()),
]
