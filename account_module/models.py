from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', verbose_name='تصویر آواتار', null=True, blank=True)
    phone = models.CharField(max_length=12,unique=True, blank=True, null=True, verbose_name='شماره شخص')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره شخص')
    province = models.CharField(max_length=100, blank=True, null=True, verbose_name='استان')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='شهر')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    postal_code = models.CharField(max_length=15,null=True, blank=True, verbose_name='کد پستی')
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    activation_code = models.CharField(max_length=100, blank=True, verbose_name='کد تغییر رمز عبور')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()

        return self.username
