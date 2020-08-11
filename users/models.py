from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email'), unique=True, error_messages={'unique': _("Já existe um usuário com este email")}
    )
    full_name = models.CharField(_('Nome Completo'), max_length=255)
    is_staff = models.BooleanField(_('Membro da Equipe'), default=False)
    is_active = models.BooleanField(_('Ativo'), default=True, help_text=_('Desative para tirar o acesso do usuário'))
    date_joined = models.DateTimeField(_('Criação da Conta'), default=timezone.now)
    week = models.IntegerField(_('Semana'), help_text=_('Semana que o usuário está'), default=0)
    music_group = models.IntegerField(_('Grupo do Usuário'), blank=True)
    next_form = models.DateField()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'week', 'music_group', 'next_form']

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return f'{self.email} {self.full_name[:30]}'


