from django.test import TestCase
from ..models import User, OtpCode
from datetime import timedelta


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='sample@gmail.com',
            phone_number='09123456789',
            full_name='sample sample',
            password='abc'
        )
        self.user.groups.create(name='sample')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'sample@gmail.com')
        self.assertEqual(self.user.phone_number, '09123456789')
        self.assertEqual(self.user.full_name, 'sample sample')
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_admin, False)
        self.assertEqual(self.user.is_staff, False)

    def test_user_is_staff(self):
        self.user.is_admin = True
        self.assertEqual(self.user.is_staff, True)

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_role(self):
        self.assertEqual(str(self.user.role()), 'sample')


class TestOtpCode(TestCase):
    def setUp(self):
        self.otp = OtpCode.objects.create(
            phone_number='09123456789',
            code=1234,
        )

    def test_otp_creation(self):
        self.assertEqual(self.otp.phone_number, '09123456789')
        self.assertEqual(self.otp.code, 1234)

    def test_otp_is_code_available(self):
        self.assertEqual(OtpCode.is_code_available('09123456789'), True)
        for i in range(5):
            OtpCode.objects.create(
                phone_number='09123456789',
                code=1234,
            )
        self.assertEqual(OtpCode.is_code_available('09123456789'), False)

    def test_otp_str(self):
        self.assertEqual(str(self.otp), f'{self.otp.phone_number} - {self.otp.code} - {self.otp.created}')

    def test_otp_is_valid(self):
        self.assertEqual(self.otp.is_valid(), True)
        self.otp.created -= timedelta(minutes=3)
        self.assertEqual(self.otp.is_valid(), False)
