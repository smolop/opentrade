from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin

from django.utils.translation import gettext_lazy as _

from ..validators.validators import UnicodeUsernameValidator

from opentrade.utils.models import OpenTradeModel 

from rest_framework.authtoken.models import Token

class AbsUser(AbstractUser):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time about when was created the object.'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time about when was the last modify of the object.'
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] 
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        """Return username."""
        return self.username
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.username            
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)            

class User(AbsUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Username and password are required. Other fields are optional.
    """
    class Meta(AbsUser.Meta):
        swappable = 'AUTH_USER_MODEL'