from . import views
from django.urls import path

urlpatterns = [
    path('', views.DashboardView.as_view(), name='user-panel'),
    path('edit-profile', views.EditUserProfile.as_view(), name='edit_profile_page'),
    path('account-info', views.ProfileView.as_view(), name='account_info_page'),
    path('change-pass', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('ordered-product', views.OrderedListView.as_view(), name='ordered_list_page'),
    path('ordered-product/<order_id>', views.detail_ordered_product, name='ordered_detail_page'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('shipping-form', views.shipping_form, name='shipping_form_page'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_count_ajax'),
]
