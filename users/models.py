from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email'), unique=True, error_messages={'unique': _("Já existe um usuário com este email")}
    )
    name = models.CharField(_('Nome Completo'), max_length=255)
    is_staff = models.BooleanField(_('Membro da Equipe'), default=False)
    is_active = models.BooleanField(_('Ativo'), default=True, help_text=_('Desative para tirar o acesso do usuário'))
    date_joined = models.DateTimeField(_('Criação da Conta'), default=timezone.now)
    week = models.IntegerField(_('Semana'), help_text=_('Semana que o usuário está'))
    group = models.IntegerField(_('Grupo do Usuário'))
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return f'{self.email} {self.name[:30]}'


