from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import datetime
from .managers import UserManager


def date_next_form():
    return timezone.now().date() + timezone.timedelta(days=7)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={'unique': _("Já existe um usuário com este email")},
    )
    full_name = models.CharField(_('Nome Completo'), max_length=255)
    phone = models.CharField(_('Número de celular'), max_length=20)
    is_staff = models.BooleanField(_('Membro da Equipe'), default=False)
    is_active = models.BooleanField(
        _('Ativo'), default=True, help_text=_('Desative para tirar o acesso do usuário')
    )
    date_joined = models.DateTimeField(_('Criação da Conta'), default=timezone.now)
    week = models.IntegerField(
        _('Semana'), help_text=_('Semana que o usuário está'), default=1
    )
    music_group = models.IntegerField(
        _('Grupo do Usuário'),
        blank=True,
        null=True,
        help_text=_('O Grupo 1 ouve música na primeira semana e o Grupo 2 não ouve.'),
    )
    next_form = models.DateField(
        _('Data do próximo formulário'), default=date_next_form
    )
    is_first_access = models.BooleanField(
        _('Primeiro Acesso do Usuário ?'),
        default=True,
        help_text=_(
            'Esse status estará marcado caso o usuário ainda não tenha entrado na plataforma'
        ),
    )
    complete_treatment = models.BooleanField(_('Tratamento Completo'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'week']

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return f'{self.email} {self.full_name[:30]}'

    def form_allow(self):
        # Retorna true caso a checklist do dia do form tenha sido completada
        # ou caso ja tenha passado um dia
        checklist = self.checklists.filter(date=self.next_form).first()
        complete_last_check = True if checklist and checklist.completed else False
        form_allow = datetime.now().date() >= (
            self.next_form + timezone.timedelta(days=1)
        )
        return complete_last_check or form_allow

    def phase_music(self):
        return (
            self.week == 1
            and self.music_group == 1
            or self.week == 2
            and self.music_group == 2
        )

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            if self.id % 2 == 0:
                self.music_group = 1
            else:
                self.music_group = 2
        return super().save(*args, **kwargs)
