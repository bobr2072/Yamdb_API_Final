from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    '''Пользовательские роли'''
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.TextField('Имя пользователя', max_length=50,
                                unique=True)
    email = models.EmailField('Почта', unique=True)
    role = models.CharField('Роль пользователя',
                            choices=ROLE, default=USER, max_length=50)
    bio = models.TextField(verbose_name='О себе', null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_user(self):
        '''Роли'''
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
