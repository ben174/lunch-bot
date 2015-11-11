from django.core.management.base import BaseCommand
from util.mailer import send_menu_email


class Command(BaseCommand):
    help = 'Sends today\'s menu to lunch-bot mailing list. If this menu has already been notified, it will' \
           'skip sending.'

    def handle(self, *args, **options):
        send_menu_email()
