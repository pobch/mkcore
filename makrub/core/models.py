# import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='E-mail address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # jwt_secret = models.UUIDField(default=uuid.uuid4)

    objects = UserManager()

    USERNAME_FIELD = 'email'

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


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(max_length=200,null=False,blank=True)
    last_name = models.CharField(max_length=200,null=False,blank=True)
    mobile_number = models.CharField(max_length=15,null=False,blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# This function is set in 'settings.py' telling where JWT secret keys are stored
# def jwt_get_secret_key(user_model):
#         return user_model.jwt_secret


class Room(models.Model):
    name = models.CharField(max_length=200, verbose_name='this is your room\'s name')
    description = models.TextField()
    # one owner per room
    room_owner = models.ForeignKey(User, related_name='own_rooms', on_delete=models.CASCADE)
    room_login = models.CharField(max_length=200, unique=True, blank=False, null=False)
    room_password = models.CharField(max_length=100, blank=False, null=False)
    guests = models.ManyToManyField(User, related_name='guest_in_rooms')
    survey = JSONField(null=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    # room = models.ForeignKey()
    guest_user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    answer = JSONField(null=True)

    def __str__(self):
        return self.guest_user + ' answers in room: '  # + self.room
