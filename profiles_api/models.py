from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles (helps Django work with our custom user model)"""
    
    def create_user(self, email, name, password=None):  # same as in UserManager(BaseUserManager)
        """Create a new user profile"""
        
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) # lowercasing the domain portion of the email address
        user = self.model(email=email, name=name) # creating an object 
        
        user.set_password(password) # method from AbstractBaseUser class
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password): # same as in UserManager(BaseUserManager)
        """Create a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'    #  used for log-in, required field by default 
    REQUIRED_FIELDS = ['name']  # 'email' is required also, but already set above

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
