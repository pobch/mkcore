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
    room_password = models.CharField(max_length=20, blank=False, null=False)
    instructor_name = models.CharField(max_length=200, blank=False, null=False)
    survey = JSONField(null=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=False) # this is CharField
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.room_code + ':' + self.title


class RoomAnswer(models.Model):
    room = models.ForeignKey(Room, related_name='guests_answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)

    answer = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user',)

    def __str__(self):
        return self.user.email + ' answer in room: ' + self.room.room_code


class GuestRoomRelation(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    room_guest = models.ForeignKey(Room, on_delete=models.CASCADE)
    join_date = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        unique_together = ('guest', 'room_guest',)

    def __str__(self):
        return '{0} {1} is a guest in this room: {2} {3}'.format(
            self.guest.id, self.guest.email, self.room_guest.id, self.room_guest.title)
