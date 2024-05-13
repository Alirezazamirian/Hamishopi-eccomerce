from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.urls import reverse
from kavenegar import *
from hamishopy.settings import Kavenegar_API
from random import randint
from zeep import Client
from . import models
import datetime
import time


# from background_task import background


def send_otp(phone, otp):
    phone = [phone, ]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '2000500666',  # optional
            'receptor': phone,  # multiple mobile number, split by comma
            'message': 'به خانواده ی حامی خوش آمدید.\n'
                       'کد ورود شما : {}'.format(otp),
        }
        response = api.sms_send(params)
        print('OTP: ', otp)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)





def send_otp_soap(phone, otp):
    client = Client('http://api.kavenegar.com/soap/v1.asmx?WSDL')
    receptor = [phone, ]

    empty_array_placeholder = client.get_type('ns0:ArrayOfString')
    receptors = empty_array_placeholder()
    for item in receptor:
        receptors['string'].append(item)

    api_key = Kavenegar_API
    message = 'Your OTP is {}'.format(otp)
    sender = '2000500666'
    status = 0
    status_message = ''

    result = client.service.SendSimpleByApikey(api_key,
                                               sender,
                                               message,
                                               receptors,
                                               0,
                                               1,
                                               status,
                                               status_message)
    print(result)
    print('OTP: ', otp)


def get_random_otp():
    return randint(1000, 9999)


# def check_otp_expiration(phone):
#     try:
#         user = models.User.objects.get(phone=phone)
#         now = datetime.datetime.now()
#         otp_time = user.otp_create_time
#         diff_time = now - otp_time
#         print('OTP TIME: ', diff_time)
#
#         if diff_time.seconds > 120:
#             return False
#         return True
#
#     except models.User.DoesNotExist:
#         return False


def check_otp_expiration(phone):
    try:
        user = models.User.objects.get(phone=phone)
        now = datetime.datetime.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        print('OTP TIME: ', diff_time)


        if diff_time.seconds > 120:
            return False


        return True

    except models.User.DoesNotExist:
        return False