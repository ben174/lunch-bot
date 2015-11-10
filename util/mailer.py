import logging
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context
from menu.models import Menu


def send_menu_email():
    today = datetime.date.today()
    try:
        menu = Menu.objects.get(date=today, notified=False, lunch__isnull=False)
    except Menu.DoesNotExist:
        logging.warning("No un-notified lunch menu exists.")
        return


    d = Context({ 'menu': menu, 'date': today })
    plaintext = 'This is just plain text'
    htmly = render_to_string('menu_email.html', d)

    subject = 'Lunch Menu for {}'.format(today)
    from_email = 'Lunch Bot'
    to = ['lunch-bot@intrafile.com']
    text_content = plaintext
    html_content = htmly
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    menu.notified = True
    menu.save()
