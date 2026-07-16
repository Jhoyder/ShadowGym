from django.urls import path
from .views import dashboard, create_payment, edit_payment, delete_payment

app_name = "payments"

urlpatterns = [
	path('', dashboard, name='index'),
	path('new/', create_payment, name='create'),
	path('<int:pk>/edit/', edit_payment, name='edit'),
	path('<int:pk>/delete/', delete_payment, name='delete'),
]
