from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from . import models


def validate_phone_number_startswith_09(value):
    if not value.startswith('09'):
        raise ValidationError(
            _('شماره همراه باید با 09 شروع شود'),
            code='invalid_phone_number'
        )


class RegisterForm(forms.Form):
    phone = forms.CharField(
        label='شماره همراه',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'شماره همراه خود را وارد کنید'
            }
        ),
        help_text='شماره همراه با 09 شروع می شود',
        validators=[
            validators.ProhibitNullCharactersValidator,
            validators.MinLengthValidator(11),
            validators.MaxLengthValidator(11),
            validate_phone_number_startswith_09
        ]
    )
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'نام کاربری تعریف کنید'
            }
        ),
        help_text='برای مثال : alizomorodi',
        validators=[
            validators.MaxLengthValidator(100),
            validators.ProhibitNullCharactersValidator,
            validators.MinLengthValidator(4, 'نام کاربری بیشتر از 4 حرف است')
        ]
    )

    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'رمز عبور تعریف کنید'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8, 'رمز عبور باید بیشتر از 8 کارکتر باشد '),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'تکرار رمز عبور'
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


class PhoneLoginForm(forms.Form):
    phone = forms.CharField(
        label='شماره همراه',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'شماره همراه خود را وارد کنید'
            }
        ),
        help_text='شماره همراه با 09 شروع می شود',
        validators=[
            validators.ProhibitNullCharactersValidator,
            validators.MinLengthValidator(11),
            validators.MaxLengthValidator(11),
            validate_phone_number_startswith_09
        ]
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        help_text='برای مثال : alizomorodi',
        label='نام کاربری',
        widget=forms.TextInput(
            attrs={
                'id': 'username_input',
                'placeholder': 'نام کاربری',
                'name': 'username',
                'type': 'text',
            }
        ),
        error_messages={
            'required': 'لطفا نام کاربری خود را وارد کنید'
        },

        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(5, 'نام کاربری بیشتر از 5 حرف است '),
            validators.ProhibitNullCharactersValidator
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_input',
                'placeholder': 'کلمه عبور',
                'name': 'password',
                'type': 'password',
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8, 'رمز عبور باید بیشتر از 8 کارکتر باشد '),
            validators.ProhibitNullCharactersValidator
        ]
    )


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'نام کاربری خود را وارد کنید'
            }
        ),
        help_text='برای مثال : alizomorodi',
        validators=[
            validators.MaxLengthValidator(100),
            validators.ProhibitNullCharactersValidator,
            validators.MinLengthValidator(4, 'نام کاربری بیشتر از 4 حرف است')
        ]
    )

    phone = forms.CharField(
        label='شماره همراه',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'شماره همراهی که در سایت ثبت کردید را وارد کنید'
            }
        ),
        help_text='شماره همراه با 09 شروع می شود',
        validators=[
            validators.ProhibitNullCharactersValidator,
            validate_phone_number_startswith_09,
            validators.MinLengthValidator(11),
            validators.MaxLengthValidator(11)
        ]
    )




class ResetPassForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'رمز عبور تعریف کنید'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8, 'رمز عبور باید بیشتر از 8 کارکتر باشد '),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'تکرار رمز عبور'
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
