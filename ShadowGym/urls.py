from django.contrib.auth import views as auth_views
from members.views import MemberLoginView

urlpatterns = [
    path('login/', MemberLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]