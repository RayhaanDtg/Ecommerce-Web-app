from django.db import models
from Cart.models import Cart

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



# class GuestEmail(models.Model):
#     email = models.EmailField()
#     active = models.BooleanField(default=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.email

class UserManager(BaseUserManager):
    def create_user(self, email,first_name,last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
           
           
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,first_name,last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
           
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name= models.CharField(max_length=255,blank=True,null=True)
    last_name=models.CharField(max_length=255,blank=True,null=True)
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE,primary_key=False)
    
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name'] # Email & Password are required by default.

    @property
    def full_name(self):
        # The user is identified by their email address
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
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
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
    
    @property
    def cart(self):
        return self.cart

    @property
    def billing_profile(self):
        return self.billing_profile



