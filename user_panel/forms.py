from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from account_module.models import User
from order_module.models import Order, OrderFormClass


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'about_user', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'id': 'message'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'address': 'آدرس',
            'about_user': 'درباره شما',
            'email': 'آدرس ایمیل'
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class ShippingUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'نام اجباری میباشد'},
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'نام خانوادگی اجباری میباشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}))
    province = forms.CharField(required=True, error_messages={'required': 'استان اجباری میباشد'},
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'استان'}))
    city = forms.CharField(required=True, error_messages={'required': 'شهر اجباری میباشد'},
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}))
    address = forms.CharField(required=True, error_messages={'required': 'آدرس میباشد'},
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس'}))
    postal_code = forms.CharField(required=True, error_messages={'required': 'کد پستی میباشد'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پستی'}))
    phone = forms.CharField(required=True, error_messages={'required': 'شماره همراه اجباری میباشد'},
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره همراه'}))
    instagram = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'ایدی اینستاگرام'}))

    class Meta:
        model = OrderFormClass
        fields = ['first_name', 'last_name', 'province', 'city', 'address', 'postal_code', 'phone', 'instagram']

        widgets = {
            'instagram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'province': 'استان',
            'city': 'شهر',
            'address': 'آدرس ',
            'postal_code': 'کد پستی',
            'phone': 'شماره همراه',
            'instagram': 'ایدی پیح اینستاگرام(اختیاری)',
        }


