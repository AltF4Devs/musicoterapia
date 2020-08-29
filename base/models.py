import unicodedata
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class Playlist(models.Model):
    name = models.CharField(_('Nome'), max_length=255)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    def __str__(self):
        return f"{self.name}"


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
    duration = models.IntegerField(_('Duração'), default=0)
    order = models.IntegerField(_('Ordem de Reprodução'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Música')
        verbose_name_plural = _('Músicas')

    def __str__(self):
        return f"{self.author} - {self.name}"

    def get_order(self):
        return "%02d" % (self.order)

    def get_formatted_duration(self):
        return "%02d:%02d" % (int(self.duration) / 60, self.duration % 60)


class Checklist(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    listened_musics = models.ManyToManyField(Music, blank=True)
    completed = models.BooleanField(default=False)
    time_elapsed = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='checklists')

    def __str__(self):
        return f"Checklist de {self.user.full_name} da {self.playlist.name}"

    class Meta:
        ordering = ['-date']
        verbose_name = _('Checklist')
        verbose_name_plural = _('Checklists')


class Form(models.Model):
    description = models.TextField(_('Descrição'), max_length=500)
    url = models.URLField()

    def __str__(self):
        return f"Form {self.description}"

    class Meta:
        ordering = ['-id']
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')
