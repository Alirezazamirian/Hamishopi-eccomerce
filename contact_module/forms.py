from django import forms
from .models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'title', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع پیام'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'rows': 5,
                'id': 'message'
            })
        }

        labels = {
            'first_name': 'نام شما',
            'last_name': 'نام خانوادگی شما',
            'email': 'ایمیل شما'
        }

        error_messages = {
            'first_name' and 'last_name': {
                'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
            },
            'title': {
                'required': 'لطفا موضوع خود را وارد کنید'
            },
            'message': {
                'required': 'لطفا متن پیام را وارد کنید'
            },
        }
