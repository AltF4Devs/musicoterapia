from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from base.models import Checklist, Playlist

class IndexView(LoginRequiredMixin, View):
    template_name = 'teste.html'

    def get(self, request, *args, **kwargs):
        # Checa se é o primeiro acesso do usuário
        if not request.user.checklists.exists():
            playlist = Playlist.objects.get(id=1)
            checklist = Checklist.objects.create(playlist=playlist, user=request.user)
            musics = playlist.musics.all()
            return render(request, self.template_name, 
                          {'playlist': playlist, 'musics': musics, 'status': 'new'})
        
        checklist = Checklist.objects.filter(user=request.user).first()

        # Checa se a playlist atual ja foi completa
        if checklist.completed:
            # Checa se a ultima playlist completa foi iniciada hoje
            if checklist.date.day == datetime.now().day:
                return render(request, self.template_name, {'status': 'completed'})
            
            # Cria uma nova checklist com a proxima playlist da fila
            total_playlists = Playlist.objects.all().count()
            prox_playlist = (checklist.playlist.id % total_playlists) + 1
            playlist = Playlist.objects.get(id=prox_playlist)
            checklist = Checklist.objects.create(playlist=playlist, user=request.user)
            musics = playlist.musics.all()

            return render(request, self.template_name, 
                          {'playlist': playlist, 'musics': musics, 'status': 'new'})
        
        # Retorna a playlist atual, incompleta
        playlist = checklist.playlist
        musics = playlist.musics.all()

        return render(request, self.template_name, 
                      {'playlist': playlist, 'musics': musics, 'status': 'incomplete'} )
