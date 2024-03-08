from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from account_module.models import User
from order_module.models import Order, OrderDetail
from user_panel.forms import EditProfileModelForm, ChangePasswordForm, ShippingUserForm
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        context = {
            'user': user
        }
        return render(request, 'user_panel/dashboard_page.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        context = {
            'user': current_user
        }
        return render(request, 'user_panel/account_info.html', context)


@method_decorator(login_required, name='dispatch')
class EditUserProfile(View):
    def get(self, request: HttpRequest):
        current_user: User = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel/change_account_info.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect('user-panel')

        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel/change_account_info.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'user_panel/change_password.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login-phone-page'))
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': form
        }
        return render(request, 'user_panel/change_password.html', context)


@login_required
def profile_partial(request):
    return render(request, 'user_panel/partial/partial.html', {})


@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    shipping_total_amount = total_amount + 40000
    context = {
        'order': current_order,
        'shipping_sum': shipping_total_amount,
        'sum': total_amount,
        'shipping': 40000
    }
    return render(request, 'user_panel/user_basket.html', context)


@login_required
def shipping_form(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    if request.method == 'GET':
        if current_order.orderdetail_set.all().exists():
            form = ShippingUserForm()
            shipping_total_amount = total_amount + 40000
            context = {
                'form': form,
                'order': current_order,
                'shipping_sum': shipping_total_amount,
                'sum': total_amount,
                'shipping': 40000
            }
            return render(request, 'user_panel/shipping_form.html', context)
        else:
            return render(request, 'article_module/video_list.html', {})
    if request.method == 'POST':
        form = ShippingUserForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('request_payment')

        context = {'form': form}
        return render(request, 'user_panel/shipping_form.html', context)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel/user_basket.html', context)
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel/user_basket.html', context)
    })


@method_decorator(login_required, name='dispatch')
class OrderedListView(ListView):
    model = Order
    template_name = 'user_panel/ordered_product.html'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_paid=True, user_id=self.request.user.id)
        return query


@login_required
def detail_ordered_product(request, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(user_id=request.user.id, id=order_id).first()
    if order is None:
        raise Http404('Order not found')
    context = {
        'order': order
    }
    return render(request, 'user_panel/detail_ordered_product.html', context)
