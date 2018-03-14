from django.urls import path, re_path

from rest_framework_jwt.views import verify_jwt_token
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from .views import register, base


urlpatterns = [
    path('users/', base.ListUsers.as_view()),
    path('users/<int:pk>/', base.DetailUser.as_view()),
    path('users/profiles/', base.ListUserProfiles.as_view()),
    path('users/profiles/<int:pk>/', base.DetailUserProfile.as_view()),
    path('signup/', register.Signup.as_view(), name="signup"),
    path('confirmation/', register.Confirmation.as_view(), name='confirmation'),
    path('login/', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
    path('login/refresh/', jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
    path('login/verify/', verify_jwt_token),

    path('rooms/', base.ListRooms.as_view()),
    path('rooms/<int:pk>/', base.DetailRoom.as_view()),
    path('answers/', base.ListAnswers.as_view()),
    path('answers/<int:pk>/', base.DetailAnswer.as_view()),

    ##### djoser
    re_path(r'^view/$', djoser_views.UserView.as_view(), name='user-view'),
    re_path(r'^delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    re_path(r'^create/$', djoser_views.UserCreateView.as_view(), name='user-create'),
    # re_path(r'^logout/$', base.UserLogoutAllView.as_view(), name='user-logout-all'),
]
