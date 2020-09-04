from django.core.management.base import BaseCommand
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.models import User
from base.models import Form


class Command(BaseCommand):
    help = 'Send email to users'

    def send_email(self, user, form):
        subject, from_email = 'Lembrete de formulário', 'musicomtr@gmail.com'
        html_msg = render_to_string('form_email.html', {'user': user, 'form': form})
        text_content = strip_tags(html_msg)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(html_msg, "text/html")
        self.stdout.write(
            self.style.SUCCESS(
                'Sending email to user "%s (%s)" ...' % (user.full_name, user.id)
            )
        )
        msg.send()

    def handle(self, *args, **kwargs):
        users = User.objects.filter(next_form=datetime.now().date())

        for user in users:
            try:
                form = Form.objects.get(week=user.week)
                self.send_email(user, form)
            except Form.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        'Form with week "%s" does not exist.' % user.week
                    )
                )
