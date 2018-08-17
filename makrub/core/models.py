# import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
        Define a model manager for User model with no username field.
        source : https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
    """

    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """ Create and save a User with the given email and password. """
        if not email:
            raise ValueError('The given email must be set')
        if not first_name:
            raise ValueError('User must provide their first name')
        if not last_name:
            raise ValueError('User must provide their last name')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """ Create and save a regular User with the given email and password. """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """ Create and save a regular User with the given email and password. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractUser):
    """ User model """

    username = models.CharField(max_length=254, blank=True, null=False)
    email = models.EmailField(_('E-mail address'), unique=True, null=False)
    first_name = models.CharField(_('first name'), max_length=50, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=False)

    # My custom fields :
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # jwt_secret = models.UUIDField(default=uuid.uuid4)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)

    mobile_num = models.CharField(max_length=20, blank=True, null=False, default='')

    def __str__(self):
        return "user's mobile num: {}".format(self.mobile_num)


# This function is set in 'settings.py' telling where JWT secret keys are stored
# def jwt_get_secret_key(user_model):
#         return user_model.jwt_secret


class Room(models.Model):
    # pattern : ( <actual value in database>, <user friendly choice name> )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active Room'),
        ('closed', 'Closed Room'),
    )
    # one owner per room
    user = models.ForeignKey(User, related_name='rooms_owner', on_delete=models.CASCADE, null=False)
    # many guests per room, many rooms per user
    guests = models.ManyToManyField(
        User,
        related_name='rooms_guest',
        through='GuestRoomRelation')
        # can be [] (no need to set blank and null = False)
    last_date_to_join = models.DateTimeField(blank=True, null=True)
    guest_ttl_in_days = models.IntegerField(blank=True, null=True)

    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    room_code = models.CharField(max_length=20, unique=True, blank=False, null=False)
    room_password = models.CharField(max_length=20, blank=True, null=False)
    instructor_name = models.CharField(max_length=200, blank=False, null=False)
    survey = JSONField(null=False, blank=True, default=list)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=False) # this is CharField
    attached_links = JSONField(null=False, blank=True, default=list)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    published_at = models.DateTimeField(null=True, blank=True)
    have_survey_when_published = models.BooleanField(null=False, blank=True, default=True)

    def __str__(self):
        return self.room_code + ':' + self.title


class RoomAnswer(models.Model):
    guest_room_relation = models.OneToOneField('GuestRoomRelation',
        related_name='answer_detail', null=True, on_delete=models.CASCADE)

    answer = JSONField(null=False, blank=True, default=list)
    first_saved_at = models.DateTimeField(auto_now_add=True, null=False)
    submitted = models.BooleanField(null=False, default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.guest_room_relation.user.email + ' answer in room: ' + (
            self.guest_room_relation.room.room_code)


#pylint:disable=E1101
class GuestRoomRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # guest user
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    request_date = models.DateTimeField(null=False, auto_now_add=True)
    accepted = models.BooleanField(null=False, default=False)
    accept_date = models.DateTimeField(null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    created_by_room_owner = models.BooleanField(null=False, default=False) # when a room owner clones guest list

    class Meta:
        unique_together = ('user', 'room',)

    def __str__(self):
        return '{0} {1} is a guest in this room: {2} {3}'.format(
            self.user.id, self.user.email, self.room.id, self.room.title)
