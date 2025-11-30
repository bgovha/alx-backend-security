from django.contrib import admin
from django.urls import path, include
from ip_tracking import urls as ip_tracking_urls
from ip_tracking.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
      path('accounts/login/', CustomLoginView.as_view(), name='login'),
]
