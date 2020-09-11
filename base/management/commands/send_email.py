from django.core.management.base import BaseCommand
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.models import User
from base.models import Form


class Command(BaseCommand):
    help = 'Send email to users'
    template_email_music = 'email/form_email_music.html'
    template_email_wait = 'email/form_email_wait.html'
    template_admin = 'email/form_admin_email.html'

    def send_user_email(self, user, form):
        template = self.template_email_music if user.phase_music() else self.template_email_wait
        subject, from_email = 'Lembrete de formulário', 'musicoterapiacovid@gmail.com'

        html_msg = render_to_string(template, {'user': user, 'form': form})

        msg = EmailMultiAlternatives(subject, html_msg, from_email, [user.email])
        msg.content_subtype = "html"
        self.stdout.write(
            self.style.SUCCESS(
                'Sending email to user "%s (%s)" ...' % (user.full_name, user.id)
            )
        )
        msg.send()

    def send_admin_email(self, user):
        subject, from_email = 'Formulário Usuário', 'musicoterapiacovid@gmail.com'

        html_msg = render_to_string(self.template_admin, {'user': user})

        msg = EmailMultiAlternatives(subject, html_msg, from_email, [from_email])
        msg.content_subtype = "html"
        msg.send()

    def handle(self, *args, **kwargs):
        users = User.objects.filter(next_form=datetime.now().date())

        for user in users:
            try:
                form = Form.objects.get(week=user.week)
                self.send_user_email(user, form)
                self.send_admin_email(user)
            except Form.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        'Form with week "%s" does not exist.' % user.week
                    )
                )
