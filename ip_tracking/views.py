from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from ratelimit.decorators import ratelimit

@method_decorator(csrf_protect, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='post')
@method_decorator(ratelimit(key='user', rate='10/m', method='POST', block=True), name='post')
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get(self, request, *args, **kwargs):
        # Apply rate limiting to GET requests as well
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return render(request, 'rate_limited.html', status=429)
        return super().get(request, *args, **kwargs)