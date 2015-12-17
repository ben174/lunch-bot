import logging
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context
from menu.models import Menu


def send_menu_email():
    """
    Sends out today's menu to the notification list. If the menu has already been sent today,
    this will log a warning and do nothing.

    This is intended to be called at a regular interval, so if the menu is not available yet
    it will be sent as soon as it is.
    """
    today = datetime.date.today()
    try:
        menu = Menu.objects.get(date=today, notified=False, lunch__isnull=False)
    except Menu.DoesNotExist:
        logging.warning("No un-notified lunch menu exists.")
        return
    d = Context({ 'menu': menu, 'date': today })
    plaintext = ''
    htmly = render_to_string('menu_email.html', d)

    subject = 'Lunch Menu for {}'.format(today)
    if menu.lunch.cuisine:
        subject = 'Lunch ({}) - {}'.format(menu.lunch.cuisine, today)

    from_email = 'Lunch Bot'
    to = ['lunch-bot@intrafile.com']
    text_content = plaintext
    html_content = htmly
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    menu.notified = True
    menu.save()
