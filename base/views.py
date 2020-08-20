from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from base.models import Checklist, Playlist

class IndexView(LoginRequiredMixin, View):
    template_music = 'teste.html' # Template com as musicas
    template_wait = 'teste2.html' # Template avisando que não terá músicas nesta fase

    def get(self, request, *args, **kwargs):
        # Checa se o usuário está na fase de músicas
        user = request.user
        phase_music = user.week == 1 and user.music_group == 1 or user.week == 2 and user.music_group == 2

        if phase_music:
            # Checa se é a primeira vez que o usuário acessa a fase de músicas
            if user.is_first_access:
                playlist = Playlist.objects.get(id=1)
                checklist = Checklist.objects.create(playlist=playlist, user=request.user)
                musics = playlist.musics.all()
                user.is_first_access = False
                user.save()
                return render(request, self.template_music, 
                            {'playlist': playlist, 'musics': musics, 'status': 'new'})
            
            checklist = Checklist.objects.filter(user=request.user).first()

            # Checa se a playlist atual ja foi completa
            if checklist.completed:
                # Checa se a ultima playlist completa foi iniciada hoje
                if checklist.date.day == datetime.now().day:
                    return render(request, self.template_music, {'status': 'completed'})
                
                # Cria uma nova checklist com a proxima playlist da fila
                total_playlists = Playlist.objects.all().count()
                prox_playlist = (checklist.playlist.id % total_playlists) + 1
                playlist = Playlist.objects.get(id=prox_playlist)
                checklist = Checklist.objects.create(playlist=playlist, user=request.user)
                musics = playlist.musics.all()

                return render(request, self.template_music, 
                            {'playlist': playlist, 'musics': musics, 'status': 'new'})
            
            # Retorna a playlist atual, incompleta
            playlist = checklist.playlist
            musics = playlist.musics.all()

            return render(request, self.template_music, 
                        {'playlist': playlist, 'musics': musics, 'status': 'incomplete'} )
        else:
            return render(request, self.template_wait)
