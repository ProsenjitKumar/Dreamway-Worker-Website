
from django.db import models
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager
)
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords

# For history
from simple_history import register


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an Email address.")
        if not password:
            raise ValueError("Users must have a Password")
        if not full_name:
            raise ValueError("Users must have a Full Name")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=False # will be True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    #address = models.CharField(max_length=455)
    active = models.BooleanField(default=True) # Can Login
    staff = models.BooleanField(default=False) # staff user non Superuser
    admin = models.BooleanField(default=False) # Superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm = models.BooleanField(default=False)
    # confiremed_date = models.DateTimeField(default=False)

    # Profile
    lead = models.IntegerField(default=0)
    balance = models.IntegerField(default=0.00)
    address = models.CharField(max_length=255, default="Bangladesh")
    first_refer = models.IntegerField(default=0)
    second_refer = models.IntegerField(default=0)
    third_refer = models.IntegerField(default=0)
    fourth_refer = models.IntegerField(default=0)
    update = models.DateTimeField(null=True, blank=True)

    #changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    history = HistoricalRecords()

    # Personal Info
    age = models.IntegerField(default=20)

    USERNAME_FIELD = 'email'  # Username
    # USERNAME_FILED and password are required by default
    REQUIRED_FIELDS = ['full_name'] # 'full_name'

    objects = UserManager()



    def __str__(self):
        return self.email

    def  get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



#register(User, inherit=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend extra data
    #lead = models.CharField(max_length=45)
    weekly_lead = models.IntegerField(default=0)
    history = HistoricalRecords()
    #update_time = models.DateTimeField()
    #monthy_lead = models.ForeignKey(UserManager, on_delete=models.CASCADE)



def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)




class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# for history
#register(User, excluded_fields=['last_login'])
#register(User, inherit=True)


# def get_User_user(instance, **kwargs):
#     return instance.changed_by
#
#
# register(User, get_user=get_User_user)
