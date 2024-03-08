from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from order_module.models import Order
from site_module.models import SiteSetting, FooterLinkBox, Slider
from product_app.models import Brand, Product, Car, ProductVisit
from utils.convertors import group_list


class AboutPage(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context


class HomeView(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        best_sell = Product.objects.filter(is_active=True, is_delete=False, is_best_sell=True).order_by('-id')[:5]
        hot_suggest = Product.objects.filter(is_active=True, is_delete=False, is_best_sell=True).order_by('-id')[:5]
        most_visited_by_user = ProductVisit.objects.filter(user_id=self.request.user.id, ip__iexact=self.request.META.get('REMOTE_ADDR'))[:10]
        context['hot_suggest'] = hot_suggest
        context['best_sell'] = best_sell
        context['sliders'] = sliders
        context['most_visited_by_user'] = most_visited_by_user
        latest_products = Product.objects.filter(is_active=True, is_delete=False, is_new=True).order_by('-id')[:10]
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = latest_products
        context['most_visit_products'] = group_list(most_visit_products)

        return context


def site_footer_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    context = {
        'site_setting': site_setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/footer.html', context)


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    brands: Brand = Brand.objects.filter(is_active=True)
    context = {
        'site_setting': setting,
        'brands': brands
    }

    return render(request, 'shared/header.html', context)
