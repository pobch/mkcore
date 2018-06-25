from django.urls import path

from .views import RoomAnswerExportView, ForTest


urlpatterns = [
    path('answers/', RoomAnswerExportView.as_view()), # + ?room_id=<'id' of Room model>
    path('test/', ForTest.as_view()),
]
