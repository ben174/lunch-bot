import logging
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context
from menu.models import Menu



def send_menu_email():
    today = datetime.date.today()
    if not Menu.objects.filter(menu_type='L', date=today, notified=False).exists:
        logging.warning("No un-notified lunch menu exists.")
        return
    try:
        lunch_menu = Menu.objects.get(date=today, menu_type='L', notified=False)
    except Menu.DoesNotExist:
        message = "Lunch menu does not exist for today."
        logging.warning(message)
        return
    dinner_menu = None
    try:
        dinner_menu = Menu.objects.get(date=today, menu_type='D')
    except Menu.DoesNotExist:
        message = "Dinner menu does not exist for today."
        logging.warning(message)

    d = Context({ 'lunch_menu': lunch_menu, 'dinner_menu': dinner_menu, 'date': today })
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

    lunch_menu.notified = True
    lunch_menu.save()
    if dinner_menu:
        dinner_menu.notified = True
        dinner_menu.save()
