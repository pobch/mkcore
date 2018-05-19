# import uuid
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from core.models import User, Room, RoomAnswer, UserProfile, GuestRoomRelation
from api.serializers import (UserSerializer, UserProfileSerializer, RoomSerializer,
    RoomAnswerSerializer, GuestRoomRelationSerializer)
from api.permissions import IsOwnerForUserModel, IsOwner, IsOwnerOrGuest


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
            return Room.objects.filter(user=user).order_by('-created_at')
        if query == 'guest':
            return Room.objects.filter(guests=user, guestroomrelation__accepted=True) \
                .order_by('-guestroomrelation__accept_date')
        return Room.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListPendingRooms(generics.ListAPIView):
    queryset = GuestRoomRelation.objects.all()
    serializer_class = GuestRoomRelationSerializer

    def get_queryset(self):
        user = self.request.user
        return GuestRoomRelation.objects.filter(user=user, accepted=False).order_by('-request_date')


class DetailRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerOrGuest,)


class ListRoomAnswers(generics.ListCreateAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer

    def create(self, request, *args, **kwargs):
        guestRoomRelation_obj = get_object_or_404(GuestRoomRelation.objects.all(),
            user=request.user,
            room_guest=request.data.pop('room', 0))
        request.data['guest_room_relation'] = guestRoomRelation_obj.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DetailRoomAnswer(generics.RetrieveAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter_for_GuestRoomRelation = {
            'room_guest': get_object_or_404(Room.objects.all(), id=self.kwargs['room']),
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
        room_obj = get_object_or_404(Room.objects.all(), **filter_keywords)
        guest_obj = request.user
        # data = {'user': guest_obj.id, 'room_guest': room_obj.id}
        # serializer = GuestRoomRelationSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        guest_room_relation_obj, created = GuestRoomRelation.objects \
            .get_or_create(user=guest_obj, room_guest=room_obj)
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
        guest_room_relation_obj = get_object_or_404(GuestRoomRelation, user=guest_obj, room_guest=room_obj)
        guest_room_relation_obj.delete()
        ##### Work around (Temp) ######
        # room_answer_obj = get_object_or_404(RoomAnswer, user=guest_obj, room=room_obj)
        # room_answer_obj.delete()
        ###############################
        return Response('Leave success', status=status.HTTP_200_OK)


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

