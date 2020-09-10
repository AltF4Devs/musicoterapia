import unicodedata
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class Playlist(models.Model):
    name = models.CharField(_('Nome'), max_length=255)
    order = models.IntegerField(_('Ordem de Reprodução'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    def __str__(self):
        return f"{self.name}"

    def display_music_count(self):
        return self.musics.count()

    display_music_count.short_description = _('Quantidade de músicas')


def path_music(instance, filename):
    titulo_format = ''.join(
        ch
        for ch in unicodedata.normalize('NFKD', filename)
        if not unicodedata.combining(ch)
    )
    return f'musics/{titulo_format}'


validator_music = FileExtensionValidator(allowed_extensions=['mp3', 'wav'])


class Music(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name='musics'
    )
    name = models.CharField(_('Nome'), max_length=255)
    author = models.CharField(_('Autor'), max_length=255)
    compositor = models.CharField(_('Compositor'), max_length=255)
    performer = models.CharField(_('Intérprete'), max_length=255)
    file = models.FileField(upload_to=path_music, validators=[validator_music])
    order = models.IntegerField(_('Ordem de Reprodução'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Música')
        verbose_name_plural = _('Músicas')

    def __str__(self):
        return f"{self.author} - {self.name}"

    def get_order(self):
        return "%02d" % self.order

    '''
    def get_formatted_duration(self):
        return "%02d:%02d" % (int(self.duration) / 60, self.duration % 60)
    '''


class Checklist(models.Model):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.PROTECT,
        help_text=_('Playlist de músicas que o usuário está ouvindo'),
    )
    date = models.DateField(
        _('Criada em'),
        auto_now_add=True,
        help_text=_('Data que a checklist foi criada'),
    )
    listened_musics = models.ManyToManyField(
        Music,
        blank=True,
        verbose_name=_('Músicas escutadas'),
        help_text=_(
            'Músicas que o úsuario ouviu desta playlist, desde a criação da checklist'
        ),
    )
    completed = models.BooleanField(
        _('Checklist completa'),
        default=False,
        help_text=_(
            'Se o campo estiver marcado, o usuário ouviu todas as músicas desta playlist e completou esta checklist'
        ),
    )
    time_elapsed = models.IntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='checklists',
        verbose_name=_('Usuário'),
    )

    class Meta:
        ordering = ['-date']
        verbose_name = _('Checklist')
        verbose_name_plural = _('Checklists')

    def __str__(self):
        return f"Checklist de {self.user.full_name} da {self.playlist.name}"

    def display_music_count(self):
        return self.musics.count()

    display_music_count.short_description = _('Quantidade de músicas ouvidas')


class Form(models.Model):
    description = models.TextField(_('Descrição'), max_length=500)
    url = models.URLField()
    week = models.IntegerField(_('Semana do formulário'))

    def __str__(self):
        return f"Form {self.description}"

    class Meta:
        ordering = ['-id']
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')
