# import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('User must provide their first name')
        if not last_name:
            raise ValueError('User must provide their last name')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='E-mail address', max_length=255, unique=True)
    first_name = models.CharField(blank=False,null=False,max_length=200)
    last_name = models.CharField(blank=False,null=False,max_length=200)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # jwt_secret = models.UUIDField(default=uuid.uuid4)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)

    mobile_num = models.CharField(max_length=20, blank=True, null=False, default='')

    def __str__(self):
        return "user's mobile num: {}".format(self.mobile_num)


# This function is set in 'settings.py' telling where JWT secret keys are stored
# def jwt_get_secret_key(user_model):
#         return user_model.jwt_secret


# For 'attached_links' field in Room model:
def default_attached_links_value():
    """
    'link_url': 'http://www.example.com/data.pdf'
    'content_type': 'doc' ### choose one of 'doc' / 'video' / 'audio' / 'others'
    """
    return [
        {'link_url': '', 'content_type': 'others'},
        {'link_url': '', 'content_type': 'others'},
        {'link_url': '', 'content_type': 'others'},
    ]


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

    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    room_code = models.CharField(max_length=20, unique=True, blank=False, null=False)
    room_password = models.CharField(max_length=20, blank=True, null=False)
    instructor_name = models.CharField(max_length=200, blank=False, null=False)
    survey = JSONField(null=False, blank=True, default=list)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=False) # this is CharField
    attached_links = JSONField(null=False, blank=True, default=default_attached_links_value)
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


class GuestRoomRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # guest user
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    request_date = models.DateTimeField(null=False, auto_now_add=True)
    accepted = models.BooleanField(null=False, default=False)
    accept_date = models.DateTimeField(null=True, blank=True)
    created_by_room_owner = models.BooleanField(null=False, default=False)

    class Meta:
        unique_together = ('user', 'room',)

    def __str__(self):
        return '{0} {1} is a guest in this room: {2} {3}'.format(
            self.user.id, self.user.email, self.room.id, self.room.title)
