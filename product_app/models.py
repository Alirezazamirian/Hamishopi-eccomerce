from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from account_module.models import User


class Brand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Car(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'ماشین'
        verbose_name_plural = 'ماشین ها'


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    car = models.ForeignKey(Car,
                            related_name='product_car', verbose_name='ماشین', on_delete=models.CASCADE)
    brand = models.ManyToManyField(Brand, related_name='product_brand', verbose_name='برند')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    price = models.IntegerField(verbose_name='قیمت')
    off_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت با تخفیف')
    avg_rating = models.FloatField(default=0, verbose_name='میانگین امتیاز')
    number_rating = models.IntegerField(default=0, verbose_name='تعداد نظر ها')
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد موجودی')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    is_new = models.BooleanField(default=False, verbose_name='جدید')
    is_best_sell = models.BooleanField(default=False, verbose_name='پر فروش')
    is_hot_suggest = models.BooleanField(default=False, verbose_name='یشنهاد داغ')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ثبت')
    score = models.PositiveSmallIntegerField(verbose_name='امتیاز', default=1,
                                             validators=[MaxValueValidator(5), MinValueValidator(1)])
    text = models.TextField(verbose_name='متن نظر')
    is_okay = models.BooleanField(default=False, verbose_name='مورد تایید')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'
