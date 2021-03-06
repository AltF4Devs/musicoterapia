from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
import json

from base.models import Checklist, Playlist, Form


class IndexView(LoginRequiredMixin, View):
    template_music = "index.html"  # Template com as musicas
    template_wait = "wait.html"  # Template avisando que não terá músicas nesta fase
    template_treatment = "completed_treatment.html"

    def get(self, request, *args, **kwargs):
        # Checa se o usuário está na fase de músicas
        user = request.user

        if user.complete_treatment:
            return render(request, self.template_treatment)

        if user.form_allow():
            return redirect('form')

        if user.phase_music():
            # Checa se é a primeira vez que o usuário acessa a fase de músicas
            if user.is_first_access:
                try:
                    playlist = Playlist.objects.get(order=1)
                    Checklist.objects.create(playlist=playlist, user=user)
                    musics = playlist.musics.all()

                    user.is_first_access = False
                    user.save()
                    return render(
                        request,
                        self.template_music,
                        {"playlist": playlist, "musics": musics, "status": "new"},
                    )
                except Playlist.DoesNotExist:
                    messages.error(request, "Nenhuma playlist encontrada")
                    return render(request, '404.html', {})

            checklist = (
                Checklist.objects.prefetch_related("playlist", "playlist__musics")
                .filter(user=user)
                .first()
            )

            # Checa se a playlist atual ja foi completa
            if checklist.completed:
                # Checa se a ultima playlist completa foi iniciada hoje
                if checklist.date == datetime.now().date():
                    return render(request, self.template_music, {"status": "completed"})

                # Cria uma nova checklist com a proxima playlist da fila
                total_playlists = Playlist.objects.all().count()
                prox_playlist = (checklist.playlist.order % total_playlists) + 1
                try:
                    playlist = Playlist.objects.get(order=prox_playlist)
                    Checklist.objects.create(playlist=playlist, user=user)
                    musics = playlist.musics.all()

                    return render(
                        request,
                        self.template_music,
                        {"playlist": playlist, "musics": musics, "status": "new"},
                    )
                except Playlist.DoesNotExist:
                    messages.error(request, "Próxima playlist não encontrada")
                    return render(request, '404.html', {})

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
                },
            )
        else:
            return render(request, self.template_wait)

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


class FormView(LoginRequiredMixin, generic.TemplateView):
    template_name = "formulario.html"

    def get(self, request, *args, **kwargs):
        # Checa se o usuário está na fase de músicas
        user = request.user

        if user.form_allow():
            try:
                form = Form.objects.get(week=user.week)
                return render(request, self.template_name, {"form": form})
            except Form.DoesNotExist:
                messages.error(request, 'Form não encontrado')
        return redirect("dashboard")


class CompletedFormView(LoginRequiredMixin, View):
    template_form = 'completed_form.html'
    template_treatment = 'completed_treatment.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        '''
         Se for a última semana do usuário, o tratamento é completado, se não,
         ele avança para a próxima fase e o novo formulário é setado para daqui
         8 dias
        '''
        if not user.form_allow():
            return redirect('dashboard')

        if user.week == 1:
            user.next_form = timezone.now().date() + timezone.timedelta(days=7)
            user.week = 2
            user.save()
            return render(request, self.template_form)

        user.complete_treatment = True
        user.save()

        return render(request, self.template_treatment)
