from django.urls import path, re_path

# from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from .views import auth, base


urlpatterns = [
    # djangorestframework-jwt views
    path('auth/login/', jwt_views.ObtainJSONWebToken.as_view(), name='auth_login'),
    path('auth/login/refresh/', jwt_views.RefreshJSONWebToken.as_view(), name='auth_login_refresh'),
    path('auth/login/verify/', jwt_views.verify_jwt_token, name='auth_login_verify'),  # verify_jwt_token is a function

    path('auth/register/', auth.Register.as_view(), name="auth_register"),
    path('auth/confirmation/', auth.Confirmation.as_view(), name='confirmation'),
    path('auth/check-me/', auth.CheckMe.as_view(), name="auth_check_me"),
    path('users/', base.ListUsers.as_view()),
    path('users/<int:pk>/', base.DetailUser.as_view()),
    path('users/profiles/', base.ListUserProfiles.as_view()),
    path('users/profiles/<int:pk>/', base.DetailUserProfile.as_view()),

    path('rooms/', base.ListRooms.as_view()),
    path('rooms/<int:pk>/', base.DetailRoom.as_view()),
    path('answers/', base.ListRoomAnswers.as_view()),
    path('answers/<int:pk>/', base.DetailRoomAnswer.as_view()),

    # djoser
    # re_path(r'^view/$', djoser_views.UserView.as_view(), name='user-view'),
    # re_path(r'^delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    # re_path(r'^create/$', djoser_views.UserCreateView.as_view(), name='user-create'),
    # re_path(r'^logout/$', base.UserLogoutAllView.as_view(), name='user-logout-all'),
]
