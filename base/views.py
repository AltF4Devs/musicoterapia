from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import json

from base.models import Checklist, Playlist, Form


class IndexView(LoginRequiredMixin, View):
    template_music = "index.html"  # Template com as musicas
    template_wait = "wait.html"  # Template avisando que não terá músicas nesta fase

    def get(self, request, *args, **kwargs):
        # Checa se o usuário está na fase de músicas
        user = request.user
        phase_music = (
            user.week == 1
            and user.music_group == 1
            or user.week == 2
            and user.music_group == 2
        )
        form_allow = datetime.now().day >= user.next_form.day

        if phase_music:
            # Checa se é a primeira vez que o usuário acessa a fase de músicas
            if user.is_first_access:
                try:
                    playlist = Playlist.objects.get(id=1)
                    Checklist.objects.create(playlist=playlist, user=user)
                    musics = playlist.musics.all()

                    user.is_first_access = False
                    user.save()
                    return render(
                        request,
                        self.template_music,
                        {
                            "playlist": playlist,
                            "musics": musics,
                            "status": "new",
                            "form_allow": form_allow,
                        },
                    )
                except Playlist.DoesNotExist:
                    messages.error(request, "Nenhuma playlist encontrada")

            checklist = (
                Checklist.objects.prefetch_related("playlist", "playlist__musics")
                .filter(user=user)
                .first()
            )

            # Checa se a playlist atual ja foi completa
            if checklist.completed:
                # Checa se a ultima playlist completa foi iniciada hoje
                if checklist.date.day == datetime.now().day:
                    return render(
                        request,
                        self.template_music,
                        {"status": "completed", "form_allow": form_allow},
                    )

                # Cria uma nova checklist com a proxima playlist da fila
                total_playlists = Playlist.objects.all().count()
                prox_playlist = (checklist.playlist.id % total_playlists) + 1
                try:
                    playlist = Playlist.objects.get(id=prox_playlist)
                    Checklist.objects.create(playlist=playlist, user=user)
                    musics = playlist.musics.all()

                    return render(
                        request,
                        self.template_music,
                        {
                            "playlist": playlist,
                            "musics": musics,
                            "status": "new",
                            "form_allow": form_allow,
                        },
                    )
                except Playlist.DoesNotExist:
                    messages.error(request, "Próxima playlist não encontrada")

            # Retorna a playlist atual com as musicas que faltam ouvir
            playlist = checklist.playlist
            listened_musics = checklist.listened_musics.all()
            musics_not_listened = playlist.musics.exclude(id__in=listened_musics)

            return render(
                request,
                self.template_music,
                {
                    "playlist": playlist,
                    "listened_musics": listened_musics,
                    "musics": musics_not_listened,
                    "status": "incomplete",
                    "form_allow": form_allow,
                },
            )
        else:
            return render(request, self.template_wait, {"form_allow": form_allow})

    def post(self, request, *args, **kwargs):
        user = request.user
        post = json.loads(request.body)
        music = post['music']
        checklist = (
            Checklist.objects.prefetch_related("playlist", "playlist__musics")
            .filter(user=user, completed=False)
            .first()
        )

        checklist.listened_musics.add(music)
        total_musics = checklist.playlist.musics.count()
        total_listened = checklist.listened_musics.count()
        playlist_completed = (
            total_musics == total_listened
        )  # Checa se a playlist foi finalizada

        # Finaliza a checklist
        if playlist_completed:
            checklist.completed = True
            checklist.save()

        return JsonResponse({'playlistCompleted': playlist_completed})

class FormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Checa se o usuário está na fase de músicas
        user = request.user

        if datetime.now().date() >= user.next_form:
            try:
                form = Form.objects.get(week=user.week)
                return render(request, "formulario.html", {"form": form})
            except ObjectDoesNotExist:
                return redirect("dashboard")
        else:
            return redirect("dashboard")