from django.db import models
from account_module.models import User
from product_app.models import Product
from account_module.forms import validate_phone_number_startswith_09

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False,verbose_name='نهایی شده/نشده')
    is_start = models.BooleanField(default=True, verbose_name='در حال بررسی')
    is_progress = models.BooleanField(default=False, verbose_name='در حال انجام')
    is_finish = models.BooleanField(default=False, verbose_name='ارسال شده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return str(self.user.username)

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                if order_detail.product.off_price:
                    total_amount += order_detail.product.off_price * order_detail.count
                else:
                    total_amount += order_detail.product.price * order_detail.count
        return total_amount

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        if self.product.off_price:
            return self.count * self.product.off_price
        else:
            return self.count * self.product.price

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'


class OrderFormClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(blank=True, max_length=30, verbose_name='نام سفارش دهنده')
    last_name = models.CharField(blank=True, max_length=30, verbose_name='نام خانوادگی سفارش دهنده')
    province = models.CharField(blank=True, max_length=30, verbose_name='استان سفارش دهنده')
    city = models.CharField(blank=True, max_length=30, verbose_name='شهر سفارش دهنده')
    address = models.TextField(blank=True, max_length=200, verbose_name='آدرس سفارش دهنده')
    postal_code = models.CharField(blank=True, max_length=30, verbose_name='کد پستی سفارش دهنده')
    phone = models.CharField(null=True, blank=True, max_length=30, verbose_name='شماره سفارش دهنده', validators=[validate_phone_number_startswith_09])
    followup_code = models.IntegerField(blank=True, verbose_name='کد پیگیری')
    instagram = models.CharField(max_length=30, blank=True, null=True, verbose_name='ایدی اینستا سفارش دهنده')
    is_paid = models.BooleanField(default=False, verbose_name='نهایی شده/نشده')

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'سفارش کاربر'
        verbose_name_plural = 'سفارشات کاربران'
