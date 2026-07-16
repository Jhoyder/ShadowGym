
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
#Con eso tendrás login y logout listos con Django Auth
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='members:index', permanent=False)),
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('memberships/', include('memberships.urls')),
    path('payments/', include('payments.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
