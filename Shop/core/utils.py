from random import randint
from kavenegar import *
from django.core.validators import RegexValidator


def random_code(start=1000, end=9999):
    return randint(start, end)


def send_otp_code(phone_number, code):
    API_KEY = '662F4F5676312B644B2F624C43516E79314A5A72384E4865426B5272674D454A74494330586E7133506E773D'
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'Your verification code is {code} '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


# ############################################# REGEX #####################################################
phone_regex = r'^(\+989|09)+\d{9}$'

phone_regex_validator = RegexValidator(
    regex=phone_regex, message="Invalid Phone number. Phone number must be like: +989XXXXXXXXX or 09XXXXXXXXX"
)

full_name_regex = r'(^[A-Za-z]{3,16})([ ]{0,1})([A-Za-z]{3,16})?([ ]{0,1})?([A-Za-z]{3,16})$'

full_name_regex_validator = RegexValidator(
    regex=full_name_regex,
    message="Invalid Full name. Full name must only contain alphabet letters and whitespace."
)
