from django.core.management.base import BaseCommand
from util.mailer import send_menu_email


class Command(BaseCommand):
    help = 'Sends today\'s menu to lunch-bot mailing list.'

    def handle(self, *args, **options):
        send_menu_email()
