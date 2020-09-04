from django.core.management.base import BaseCommand
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.models import User
from base.models import Form


class Command(BaseCommand):
    help = 'Send email to users'

    def send_user_email(self, user, form):
        subject, from_email = 'Lembrete de formulário', 'musicoterapiacovid@gmail.com'

        html_msg = render_to_string(
            'email/form_email.html', {'user': user, 'form': form}
        )
        text_msg = render_to_string(
            'email/form_email.txt', {'user': user, 'form': form}
        )

        msg = EmailMultiAlternatives(subject, html_msg, from_email, [user.email])
        msg.content_subtype = "html"
        msg.attach_alternative(text_msg, "text/plain")
        self.stdout.write(
            self.style.SUCCESS(
                'Sending email to user "%s (%s)" ...' % (user.full_name, user.id)
            )
        )
        msg.send()

    def send_admin_email(self, user):
        subject, from_email = 'Formulário Usuário', 'musicoterapiacovid@gmail.com'

        html_msg = render_to_string('email/form_admin_email.html', {'user': user})
        text_msg = render_to_string('email/form_admin_email.txt', {'user': user})

        msg = EmailMultiAlternatives(subject, html_msg, from_email, [from_email])
        msg.content_subtype = "html"
        msg.attach_alternative(text_msg, "text/plain")
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
