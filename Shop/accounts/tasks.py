from celery import shared_task
from .models import OtpCode


@shared_task
def remove_expired_otp_codes():
    otp_codes = OtpCode.objects.all()
    for otp in otp_codes:
        otp.is_valid()
