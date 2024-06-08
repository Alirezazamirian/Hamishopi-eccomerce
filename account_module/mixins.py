from django.shortcuts import redirect

class RedirectIfLoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')  # Redirect to home page or any other URL
        return super().dispatch(request, *args, **kwargs)