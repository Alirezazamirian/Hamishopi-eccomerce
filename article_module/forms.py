from django import forms
from .models import ArticleComment


class ArticleCommentForm(forms.ModelForm):

    first_name = forms.CharField(required=True, error_messages={'required': 'نام اجباری میباشد'},
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'نام خانوادگی اجباری میباشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}))
    text = forms.CharField(required=True, error_messages={'required': 'درج پیام اجباری میباشد'},
                               widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'متن پیام'}))
    class Meta:
        model = ArticleComment
        fields = ['first_name', 'last_name', 'text']


        labels = {
            'first_name': 'نام شما',
            'last_name': 'نام خانوادگی شما',
            'text': 'متن پیام'
        }



