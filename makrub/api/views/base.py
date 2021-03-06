# import uuid
from django.utils import timezone # use this instead of python's datetime to avoid
                        # RuntimeWarning: received a naive datetime while time zone support is active.
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_bulk import BulkCreateAPIView

from core.models import Room, RoomAnswer, UserProfile, GuestRoomRelation
from api.serializers import (UserSerializer, UserProfileSerializer, RoomSerializer,
    RoomAnswerSerializer, GuestRoomRelationSerializer, GuestRoomRelationBulkSerializer)
from api.permissions import IsOwnerForUserModel, IsOwner, IsOwnerOrGuest


User = get_user_model()


# For testing purpose only. Have to delete this view in production
class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerForUserModel,)
    # permission_classes = (IsAuthenticated,)


# For testing purpose only. Have to delete this view in production
class ListUserProfiles(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class DetailUserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwner,)


class ListRooms(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('query', None)
        if query == 'owner':
            return Room.objects.filter(user=user).order_by('-published_at', '-created_at')
        if query == 'guest':
            return Room.objects.filter(
                    Q(guest_ttl_in_days__isnull=True) | Q(guestroomrelation__expire_date__gte=timezone.now()),
                    guests=user,
                    guestroomrelation__accepted=True
                ).order_by('-guestroomrelation__accept_date')
            # bcoz the field which is ordered by is reverse relation (list type), so if there are
            #   multiple values in the list, the result will include duplicate items without raising error!!!
            #   see 'Note' section on https://docs.djangoproject.com/en/2.0/ref/models/querysets/#order-by

        return Room.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerOrGuest,)


class DetailRoomByRoomCode(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter_by = {
            'room_code': self.request.query_params.get('room_code', None),
            'user': self.request.user, # will search only owned room
        }
        room_obj = get_object_or_404(queryset, **filter_by)
        self.check_object_permissions(self.request, room_obj)
        return room_obj


class ListPendingRooms(generics.ListAPIView):
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationSerializer

    def get_queryset(self):
        user = self.request.user
        return GuestRoomRelation.objects.filter(user=user, accepted=False).order_by('-request_date')


class ListJoinRequestsByRoomId(generics.ListAPIView):
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationSerializer

    def get_queryset(self):

        # # Filter only accepted guests
        # return GuestRoomRelation.objects.filter(accepted=False, room=self.kwargs['room_id'])

        # # Backend does not filter 'accepted' field, let the frontend do the filter logic
        return GuestRoomRelation.objects.filter(room=self.kwargs['room_id'])


class DetailJoinRequestOfMeByRoomId(generics.RetrieveAPIView):
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationSerializer

    def get_object(self):
        me = self.request.user
        room_id = self.kwargs['room_id']
        return get_object_or_404(GuestRoomRelation.objects.all(), user=me, room=room_id)


class DetailJoinRequest(generics.RetrieveUpdateDestroyAPIView):
    """
    To accept each join req, frontend will send a json body below via
        URL containing row 'id' to PATCH a GuestRoomRelation row of that 'id'
        json body : { accepted: true, accept_date: <date type>, expire_date: <date type> }
    To deny each join req, frontend will send a DELETE method via URL containing row 'id'
        to DELETE a GuestRoomRelation row of that 'id'
    """
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationSerializer


class BulkUpdateJoinRequests(views.APIView):
    def post(self, request, format='json'):
        """
        receive json :
        {
            "ids": [...], # A list of row 'id' of GuestRoomRelation model to filter
            "eachRowData": {"accepted": true, "accept_date": <date type>, "expire_date": <date type>}
                # data to bulk update each row (same data in every row)
        }
        """
        row_ids_to_update = request.data.get('ids', [])
        each_row_data = request.data.get('eachRowData', {})
        try:
            queryset_filtered = GuestRoomRelation.objects.filter(id__in=row_ids_to_update)
            queryset_filtered.update(**each_row_data)
            # DB already updated, then serialize to response in json:
            serializer = GuestRoomRelationSerializer(queryset_filtered, many=True)
        except:
            return Response(
                {'detail': 'Unexpected errors when accepting many join reqs'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class BulkCreateJoinRequests(BulkCreateAPIView):
    """
    Input: POST a list like this:
        [   {   "created_by_room_owner": true,
                "user": <guest id>,
                "room": <room id>,
                "accepted": <true/false>,
                "accept_date": <date type>,
                "expire_date": <date type>
            },
            {...},
            ...
        ]
    Return: a list of new created rows
    Error When: an error will occurs if creating some elements in the list violates unique_together condition
    Performance Note: each row created at different timestamp bcoz (as my guess) django-rest-framework-bulk
        creates each row using loop, not using django's bulk_create()
    """
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationBulkSerializer


class ListRoomAnswers(generics.ListCreateAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer

    def create(self, request, *args, **kwargs):
        guestRoomRelation_obj = get_object_or_404(GuestRoomRelation.objects.all(),
            user=request.user,
            room=request.data.pop('room', 0))
        request.data['guest_room_relation'] = guestRoomRelation_obj.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListRoomAnswersOfMe(generics.ListAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer

    def get_queryset(self):
        user = self.request.user
        return RoomAnswer.objects.filter(guest_room_relation__user=user)


class DetailRoomAnswer(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer


class DetailRoomAnswerByRoomId(generics.RetrieveAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter_for_GuestRoomRelation = {
            'room': get_object_or_404(Room.objects.all(), id=self.kwargs['room']),
            'user': self.request.user
        }
        guestRoomRelation_obj = get_object_or_404(GuestRoomRelation.objects.all(), **filter_for_GuestRoomRelation)
        roomAnswer_obj = get_object_or_404(queryset, guest_room_relation=guestRoomRelation_obj)
        self.check_object_permissions(self.request, roomAnswer_obj)
        return roomAnswer_obj


class JoinRoom(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        receive 'room_code' and 'room_password'
        then find room to join
        then create new record in m2m relation model
        """
        filter_keywords = {}
        for field in ['room_code', 'room_password']:
            filter_keywords[field] = request.data.get(field, '')
        room_obj = get_object_or_404(Room.objects.all(),
            Q(last_date_to_join__isnull=True) | Q(last_date_to_join__gte=timezone.now()),
            **filter_keywords, status='active')
        guest_obj = request.user
        # data = {'user': guest_obj.id, 'room': room_obj.id}
        # serializer = GuestRoomRelationSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        guest_room_relation_obj, created = GuestRoomRelation.objects \
            .get_or_create(user=guest_obj, room=room_obj)
        # room_serialize = RoomSerializer(room_obj)
        # return Response(room_serialize.data)
        return Response('Room joined, wait for acceptance of the owner', status=status.HTTP_201_CREATED)


class LeaveRoom(views.APIView):
    permission_classes = (IsOwnerOrGuest,)

    def post(self, request):
        """
        receive 'user' and 'room_id'
        then filter user obj and room obj in m2m relation model and delete this record
        """
        room_obj = get_object_or_404(Room.objects.all(), id=request.data.get('room_id'))
        guest_obj = request.user
        guest_room_relation_obj = get_object_or_404(GuestRoomRelation, user=guest_obj, room=room_obj)
        guest_room_relation_obj.delete()
        ##### Work around (Temp) ######
        # room_answer_obj = get_object_or_404(RoomAnswer, user=guest_obj, room=room_obj)
        # room_answer_obj.delete()
        ###############################
        return Response('Leave success', status=status.HTTP_200_OK)


# for testing
class ListGuestRoomRelation(generics.ListCreateAPIView):
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationSerializer


# class UserLogoutAllView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, format=None):
#         user = request.user
#         user.jwt_secret = uuid.uuid4()
#         user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)


######### for Manytomany field ('guests' field) that DONT have 'through' attribute, also need to
######### set 'queryset=User.objects.all()' attribute on 'guests' field in Serializers.py
# class JoinRoom(generics.UpdateAPIView, generics.GenericAPIView):
#     serializer_class = RoomSerializer
#     permission_classes = (IsAuthenticated,)
#     queryset = Room.objects.all()
#     http_method_names = ['patch',]
#     multiple_lookup_fields = ('room_code', 'room_password') # my custom attr

#     # Business logic :
#     def get_object(self):
#         queryset = self.get_queryset()
#         filter_keywords = {}
#         for field in self.multiple_lookup_fields:
#             filter_keywords[field] = self.request.data.get(field)

#         obj = get_object_or_404(queryset, **filter_keywords)
#         self.check_object_permissions(self.request, obj)
#         return obj

#     def partial_update(self, request, *args, **kwargs):
#         partial = True
#         instance = self.get_object()
#         serializer = self.get_serializer(instance) # change queryset object type to dict type, then call dict by .data

#         # get current list of guests, then append this user to the list
#         new_guest_list = serializer.data['guests'] + ([request.user.id] if getattr(request.user,'id',None) else [])
#         data = {'guests': new_guest_list}
#         serializer = self.get_serializer(instance, data=data, partial=partial) # 'data' will receive only normal python type
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)

#     def perform_update(self, serializer):
#         serializer.save()

