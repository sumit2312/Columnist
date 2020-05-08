from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, favorite_color, password=None):
        """
        Creates and saves a User with the given email, favorite color
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            favorite_color=favorite_color,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, favorite_color, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            favorite_color=favorite_color,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # STUDENT = 1
    # TEACHER = 2
    # SECRETARY = 3
    # SUPERVISOR = 4
    # ADMIN = 5
    USER_TYPE_CHOICES = (
        ('AUTHOR', 'author'),
        ('EDITOR', 'editor'),
        ('PUBLISHER', 'publisher'),
        ('SUPERVISOR', 'supervisor'),
        ('ADMIN', 'admin'),
    )

    user_type = models.CharField(choices=USER_TYPE_CHOICES,max_length=64, default='student')

    favorite_color = models.CharField(max_length=50)
    bio = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['favorite_color']

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


# --                   --------------------------------------------

class Tweet(models.Model):
    author = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    # author_email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)
    STATE_CHOICES = (
        ('pending','pending'),
        ('published', 'published'),
        ('rejected','rejected'),
    )
    state = models.CharField(max_length=15, choices=STATE_CHOICES)

    class Meta:
        permissions = (
            ("can_approve_or_reject_tweet","Can approve or reject tweets"),
        )

    # def __str__(self):
    #     return self.name

    def get_absolute_url(self):
        return reverse("Tweet_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE,related_name='comments')
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.text