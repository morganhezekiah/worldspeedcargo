from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings



class SendEmail():
    def __init__(self, message, subject) -> None:
        self.subject = subject
        self.message = message

    def send(self):
        msg = send_mail(self.subject, self.message, 'worldspeedcargo', ["morganhezekiah11@gmail.com","support@worldspeedcargo.com"])
