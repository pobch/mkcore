from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('', views.ListAccounts.as_view()),
    path('signup/', views.Signup.as_view()),
    path('login/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('<int:pk>/', views.DetailAccount.as_view()),
]
