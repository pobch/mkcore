from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app', views.app, name='app'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
]

