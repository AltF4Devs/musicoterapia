from django.shortcuts import render
from django.views import View

from base.models import Checklist, Playlist

class IndexView(View):
    template_name = 'teste.html'

    def get(self, request, *args, **kwargs):
        # Checa se é o primeiro acesso do usuário
        if not request.user.checklists.exists():
            checklist = Checklist.objects.create(playlist=0, user=request.user)
            playlist = Playlist.objects.get(id=0)
            musics = playlist.musics.all()
            return render(request, self.template_name, {'playlist': playlist, 'musics': musics} )
        
        checklist = Checklist.objects.filter(user=request.user, completed=False).first()

        # Checa se a playlist atual ja foi completa
        if checklist is None:
            # Criar playlist
            pass
        
        playlist = checklist.playlist
        musics = playlist.musics.all()

        return render(request, self.template_name, {'playlist': playlist, 'musics': musics} )
