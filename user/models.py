from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(first_name=first_name, last_name=last_name, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="profile/images", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="profile",
    )
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    body_fat = models.FloatField(blank=True, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='profile/images', null=True, blank=True)
    # background_image = models.ImageField()
    # followed_programmes = models.ManyToManyField('Programme', related_name='followers', blank=True, null=True)

    def __str__(self):
        return self.user.first_name


# class Programme(models.Model):
#     name = models.CharField(max_length=255)
#     trainer = models.OneToOneField('Trainer', on_delete=models.CASCADE, related_name='programme')

#     def __str__(self):
#         return self.name

# class Trainer(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.first_name


# class Posts(models.Model):
#     title = models.CharField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
