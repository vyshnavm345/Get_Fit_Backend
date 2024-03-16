from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_superuser(self,first_name, last_name, email, password=None):
        
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
    email = models.EmailField(unique = True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    body_fat = models.FloatField(blank=True, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    # image = models.ImageField()
    # background_image = models.ImageField()
    
    def __str__(self):
        return self.user.first_name
    
