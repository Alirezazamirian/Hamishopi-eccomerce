from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from . import helper
from .models import User
from .forms import LoginForm, RegisterForm, PhoneLoginForm, ForgotPasswordForm, ResetPassForm
from django.contrib.auth import login, logout
from django.urls import reverse
from django.utils.crypto import get_random_string
from . import mixins


class RegisterView(mixins.RedirectIfLoggedInMixin, View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_username = register_form.cleaned_data.get('username')
            user_password = register_form.cleaned_data.get('password')
            user_phone = register_form.cleaned_data.get('phone')
            username: bool = User.objects.filter(username__iexact=user_username).exists()
            phone: bool = User.objects.filter(phone__iexact=user_phone).exists()
            if username or phone:
                messages.error(request, "نام کاربری یا شماره همراه وارد شده تکراری می باشد")
                register_form.add_error('username', 'نام کاربری یا شماره همراه وارد شده تکراری می باشد')
            else:
                new_user = User(
                    username=user_username,
                    is_active=False,
                    phone=user_phone)
                new_user.set_password(user_password)
                new_user.save()
                otp = helper.get_random_otp()
                print(otp)
                helper.send_otp(new_user.phone, otp)
                new_user.otp = otp

                new_user.save()

                request.session['user_phone'] = new_user.phone
                # todo:send OTP sms to be activate
                return redirect(reverse('verify-page'))

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)


class PhoneLoginView(mixins.RedirectIfLoggedInMixin, View):
    def get(self, request: HttpRequest):
        login_form = PhoneLoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/phone_login.html', context)

    def post(self, request):
        login_form = PhoneLoginForm(request.POST)
        if login_form.is_valid():
            user_phone = request.POST.get('phone')

            phone: bool = User.objects.filter(phone__iexact=user_phone).exists()
            if not phone:

                messages.error(request, "شماره همراه وارد شده وجود ندارد ابتدا ثبت نام کنید")
            else:
                user = User.objects.get(phone=user_phone)
                del user.otp
                new_otp = helper.get_random_otp()
                print(new_otp)
                helper.send_otp(user.phone, new_otp)
                user.otp = new_otp

                user.save()
                request.session['user_phone'] = user.phone
                # todo:send OTP sms to be activated
                return redirect(reverse('verify-page'))

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/phone_login.html', context)


def verify(request):
    user = request.user
    if not user.is_authenticated:
        try:

            phone = request.session.get('user_phone')
            user = User.objects.get(phone=phone)

            if request.method == "POST":

                # check otp expiration
                if not helper.check_otp_expiration(user.phone):
                    messages.error(request, "کد منقضی شده است دولاره امتحان کنید")
                    return HttpResponseRedirect(reverse('login-phone-page'))

                elif user.otp != int(request.POST.get('otp')):
                    messages.error(request, "کد وارد شده اشتباه است")
                    return HttpResponseRedirect(reverse('verify-page'))
                else:
                    user.is_active = True
                    user.activation_code = get_random_string(20)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('home_page'))

            return render(request, 'account_module/verify.html', {'mobile': phone})

        except User.DoesNotExist:
            messages.error(request, "خطایی رخ داد دوباره امتحان کنید")
            return HttpResponseRedirect(reverse('register-page'))
    else:
        return redirect(reverse('home_page'))

class UsernameLoginView(mixins.RedirectIfLoggedInMixin, View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/username_login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_username = login_form.cleaned_data.get('username')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(username__iexact=user_username).first()
            if user is not None:
                if not user.is_active:
                    messages.error(request, "حساب کاربری فعال نیست")
                    login_form.add_error('username',
                                         'حساب کاربری شما فعال نشده است. برای فعال سازی با شماره همراه وارد شوید')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        messages.error(request, "کلمه عبور اشتباه است")
                        login_form.add_error('password', 'کلمه عبور اشتباه است')
            else:
                messages.error(request, "کاربر وجود ندارد ابتدا ثبت نام کنید")
                login_form.add_error('username', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/username_login.html', context)


class ForgetPasswordView(mixins.RedirectIfLoggedInMixin, View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forget_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_phone = forget_pass_form.cleaned_data.get('phone')
            user_username = forget_pass_form.cleaned_data.get('username')
            user: User = User.objects.filter(phone__iexact=user_phone, username__iexact=user_username).first()
            if user is not None:

                return redirect(reverse('reset_password_page', kwargs={'activation_code': user.activation_code}))
            else:
                messages.error(request, "نام کاربری یا شماره همراه وارد شده وجود ندارد")
                forget_pass_form.add_error('phone', 'چنین کاربری وجود ندارد')

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forget_password.html', context)


class ResetPasswordView(mixins.RedirectIfLoggedInMixin, View):
    def get(self, request: HttpRequest, activation_code):
        user: User = User.objects.filter(activation_code__iexact=activation_code).first()
        if user is None:
            return redirect(reverse('login-username-page'))

        reset_pass_form = ResetPassForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, activation_code):
        reset_pass_form = ResetPassForm(request.POST)
        user: User = User.objects.filter(activation_code__iexact=activation_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.activation_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login-username-page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home_page'))
