"""Celery tasks."""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from opentrade.users.models import User, Profile
from opentrade.assets.models import ScheduledSharesOperations, Share

from celery.decorators import task, periodic_task

from opentrade.utils.functions import (
    shares as f_shares, 
    profile as f_profile
    )

import jwt
import time
from datetime import timedelta


def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=1)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


#@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! You only must to verify your accout for stat to use Open Trade'.format(user.username)
    from_email = 'Open Trade <noreply@opentrade.com>'
    content = render_to_string(
        'emails/get_up_account.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()

@periodic_task(run_every=timedelta(hours=1))
def clean_schedule_operations():
    print("Cleanning operations")
    date = timezone.localtime() - timedelta(hours=1)
    ScheduledSharesOperations.objects.filter(schedule_start__time__lte=date)
    schedule_shares_operations.delete()

@periodic_task(run_every=timedelta(minutes=1))
def execute_schedule_operations():
    print("PERIODIC TASK: SCHEDULE OPEATION")
    start_date = timezone.localtime() - timedelta(minutes=1)
    end_date = timezone.localtime() + timedelta(minutes=5)
    schedule_shares_operations = ScheduledSharesOperations.objects.filter(
        schedule_start__time__range=(start_date, end_date)
        )
    if schedule_shares_operations :
        for sch_op in schedule_shares_operations:
            execute_schedule_operations(sch_op)

@task(name='execute_schedule_operations', max_retries=5)
def execute_schedule_operations(schedule_op):
    print("Executing Schedule operation")
    print(schedule_op)
    user = schedule_op.user
    symbol = schedule_op.symbol
    quantity = schedule_op.quantity
    operation = schedule_op.operation
    constraint_max_price = schedule_op.max_price
    constraint_min_price = schedule_op.min_price
    profile = Profile.objects.get(user=user)
    price = f_shares.get_price(symbol)
    amount = quantity * price
    if not f_profile.has_funds(profile, amount):
        return
    if price < constraint_min_price or price > constraint_max_price:
        schedule_op.delete()
        return
    f_profile.payoff_balance(profile, amount)
    share = Share.objects.create(
                    symbol = symbol,
                    quantity = quantity,
                    price = price,
                    operation = operation,
                    portfolio = profile.portfolio
                )
    schedule_op.delete()
    f_profile.save(profile)


