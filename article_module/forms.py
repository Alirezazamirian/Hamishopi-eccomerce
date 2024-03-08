# from django import forms
# from .models import ArticleComment
#
#
# class ArticleCommentForm(forms.ModelForm):
#     class Meta:
#         model = ArticleComment
#         fields = ['first_name', 'last_name', 'text']
#         widgets = {
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'نام'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'نام خانوادگی'
#             }),
#             'text': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'متن کامنت',
#             })
#         }
#
#         labels = {
#             'first_name': 'نام شما',
#             'last_name': 'نام خانوادگی شما',
#             'text': 'متن کامنت شما'
#         }
#
#         error_messages = {
#             'first_name' and 'last_name': {
#                 'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
#             },
#             'text': {
#                 'required': 'لطفا متن پیام را وارد کنید'
#             },
#         }
