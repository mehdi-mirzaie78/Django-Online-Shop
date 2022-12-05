from random import randint
from kavenegar import *


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
