from django.core.management import BaseCommand, CommandError
from accounts.models import OtpCode


class Command(BaseCommand):

    def handle(self, *args, **options):
        otp_codes = OtpCode.objects.all()
        if otp_codes.first():
            for otp in otp_codes:
                otp.is_valid()
            else:
                self.stdout.write(self.style.SUCCESS('All Expired Otp codes removed'))
        else:
            self.stdout.write(self.style.WARNING('There\'s no Otp code to remove'))
    help = "Removes all of the expired otp_codes"
