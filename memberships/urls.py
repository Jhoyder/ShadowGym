from django.urls import path
from .views import dashboard, create_plan, edit_plan, delete_plan

app_name = "memberships"

urlpatterns = [
	path('', dashboard, name='index'),
	path('new/', create_plan, name='create'),
	path('<int:pk>/edit/', edit_plan, name='edit'),
	path('<int:pk>/delete/', delete_plan, name='delete'),
]

