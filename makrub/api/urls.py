from django.urls import path

from .views import register

# from rest_framework_jwt.views import verify_jwt_token
# from djoser import views as djoser_views
# from rest_framework_jwt import views as jwt_views

urlpatterns = [
    path('signup', register.Signup.as_view(), name="signup")
]

# urlpatterns = [
#     path('', views.ListAccounts.as_view()),
#     path('<int:pk>/', views.DetailAccount.as_view()),
#     path('signup', views.Signup.as_view(), name='sign-up'),
#     path('confirmation/', views.confirmation, name='confirmation'),
#
#     path('login/', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
#     path('login/refresh/', jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
#     path('login/verify/', verify_jwt_token),
#
#     re_path(r'^view/$', djoser_views.UserView.as_view(), name='user-view'),
#     re_path(r'^delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
#     re_path(r'^create/$', djoser_views.UserCreateView.as_view(), name='user-create'),
#     re_path(r'^logout/$', views.UserLogoutAllView.as_view(), name='user-logout-all'),
# ]