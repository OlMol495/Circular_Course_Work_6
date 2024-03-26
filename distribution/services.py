from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from distribution.models import CircularSettings, Logs


def send_circular():
    current_time = timezone.localtime(timezone.now())
    mailing_list = CircularSettings.objects.all()
    for mailing in mailing_list:
        if mailing.end_time < current_time:
            mailing.status = CircularSettings.Status.COMPLETED
            continue
        if mailing.start_time <= current_time < mailing.end_time:
            mailing.status = CircularSettings.Status.IN_PROGRESS
            mailing.save()
            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )

                    log = Logs.objects.create(
                        date=mailing.start_time,
                        status=Logs.SENT,
                        circular=mailing,
                        client=client,
                        response='200'
                    )
                    log.save()
                    return log

                except SMTPException as error:
                    log = Logs.objects.create(
                        date=mailing.start_time,
                        status=Logs.FAILED,
                        mailling=mailing,
                        client=client,
                        response=error
                    )
                    log.save()

                    return log

        else:
            mailing.status = CircularSettings.Status.COMPLETED
            mailing.save()
