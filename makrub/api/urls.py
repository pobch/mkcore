from django.urls import path, re_path, include
# from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from .views import auth, base


urlpatterns = [
    # django-rest-framework-jwt:
    path('auth/login/', jwt_views.ObtainJSONWebToken.as_view(), name='auth_login'),
    path('auth/login/refresh/', jwt_views.RefreshJSONWebToken.as_view(), name='auth_login_refresh'),
    path('auth/login/verify/', jwt_views.verify_jwt_token, name='auth_login_verify'),  # verify_jwt_token is a function

    # metz's auth views:
    path('auth/register/', auth.Register.as_view(), name="auth_register"),
    path('auth/confirmation/', auth.Confirmation.as_view(), name='confirmation'),
    path('auth/check-me/', auth.CheckMe.as_view(), name="auth_check_me"),

    # my base views:
    path('users/', base.ListUsers.as_view(), name='user-list'),
    path('users/<int:pk>/', base.DetailUser.as_view(), name='user-detail'),
    path('users/profiles/', base.ListUserProfiles.as_view()),
    path('users/profiles/<int:pk>/', base.DetailUserProfile.as_view()),
    path('rooms/', base.ListRooms.as_view()),
    path('rooms/search/', base.DetailRoomByRoomCode.as_view()), # search by ?room_code=xxxx
    path('rooms/<int:pk>/', base.DetailRoom.as_view(), name='room-detail'),
    path('answers/', base.ListRoomAnswers.as_view()),
    path('answers/me/', base.ListRoomAnswersOfMe.as_view()),
    path('answers/<int:pk>/', base.DetailRoomAnswer.as_view(), name='answer-detail'),
    path('answers/byroomid/<int:room>/', base.DetailRoomAnswerByRoomId.as_view()),

    #### 'joinreqs' endpoints == GuestRoomRelation model endpoint
    path('joinreqs/byroomid/<int:room_id>/', base.ListJoinRequestsByRoomId.as_view()),
                                                                # List all row in GuestRoomRelation model,
                                                                # filtered by room_id field
    path('joinreqs/<int:pk>/', base.DetailJoinRequest.as_view()), # For accept/deny a join req by PATCH/DELETE
                                                                # to a GuestRoomRelation row
    path('joinreqs/bulkcreate/', base.BulkCreateJoinRequests.as_view()),
    path('joinreqs/bulkupdate/', base.BulkUpdateJoinRequests.as_view()),
                                                                # For accept many join reqs
                                                                # by bulk update GuestRoomRelation rows
    path('joinreqs/pending/', base.ListPendingRooms.as_view()),
    path('guestroomrelation/', base.ListGuestRoomRelation.as_view()),

    #### query from other model(s) then create/modify the row of GuestRoomRelation model
    path('join/', base.JoinRoom.as_view()),
    path('unjoin/', base.LeaveRoom.as_view()),

    # djoser official doc:
    path('djoser/', include('djoser.urls')),

    # djoser modified:
    # re_path(r'^view/$', djoser_views.UserView.as_view(), name='user-view'),
    # re_path(r'^delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    # re_path(r'^create/$', djoser_views.UserCreateView.as_view(), name='user-create'),
    # re_path(r'^logout/$', base.UserLogoutAllView.as_view(), name='user-logout-all'),
]
