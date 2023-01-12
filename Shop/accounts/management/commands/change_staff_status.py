from django.core.management import BaseCommand, CommandError
from accounts.models import User


class Command(BaseCommand):
    help = """
    Change user's staff status
  
    Form changing user's staff status to True
        $ python manage.py change_staff_status --status True
        
    For changing user's staff status to False
        $ python manage.py change_staff_status
    """

    def get_user(self):
        phone = input('Enter phone number: ')
        user = User.objects.filter(phone_number=phone)
        if not user.exists():
            raise CommandError(f'User with phone number {phone} not found')
        return user.get()

    def add_arguments(self, parser):
        parser.add_argument('--status', type=bool, help='True or False', default=False, required=False)

    def handle(self, *args, **options):
        user = self.get_user()
        self.stdout.write(self.style.SUCCESS(f'User {user} found.'))
        control = input('Do you want to change staff status? (Y/n): ').lower()

        if control == 'y' or control == '':
            print(options.get('status'))
            print(options)
            user.is_admin = options.get('status')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"User's {user.phone_number} staff status changed to {options['status']} successfully"))

        else:
            self.stdout.write('Operation canceled')
