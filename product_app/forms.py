from django import forms
from .models import ProductComment


class ProductCommentForm(forms.ModelForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'نام اجباری میباشد'},
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'نام خانوادگی اجباری میباشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}))
    text = forms.CharField(required=True, error_messages={'required': 'درج پیام اجباری میباشد'},
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'متن پیام'}))
    score = forms.IntegerField(required=True, error_messages={'required': 'به محصول امتیاز دهید'},
                               widget=forms.NumberInput(attrs={'min': '1', 'max': '5'}))

    class Meta:
        model = ProductComment
        fields = ['first_name', 'last_name', 'text', 'score']

        labels = {
            'first_name': 'نام شما',
            'last_name': 'نام خانوادگی شما',
            'text': 'متن پیام'
        }

        help_texts = {
            'score': 'از 1 تا 5 امتیاز دهید'
        }
