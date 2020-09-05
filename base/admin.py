from django.contrib import admin
from .models import Checklist, Playlist, Music, Form


class ChecklistAdmin(admin.ModelAdmin):
    readonly_fields = ('listened_musics', 'completed')
    list_display = ('user', 'playlist', 'date', 'completed')
    list_filter = ('user', 'completed', 'playlist')


class MusicsInline(admin.StackedInline):
    model = Music
    extra = 1


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [MusicsInline]

    list_display = ('name', 'display_music_count')


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'playlist', 'author')
    list_filter = ('playlist',)


admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Form)
admin.site.site_header = "MusicaMCT"
admin.site.index_title = "Gerenciamento"
admin.site.site_title = admin.site.site_header + " - Painel"
