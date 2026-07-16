from django.urls import path
from .views import (
	create_member,
	dashboard,
	delete_member,
	edit_member,
	mark_attendance,
	mark_attendance_by_code,
	member_qr,
	send_member_code_email,
)

app_name = "members"

urlpatterns = [
	path('', dashboard, name='index'),
	path('attendance/by-code/', mark_attendance_by_code, name='attendance_by_code'),
	path('<int:pk>/attendance/', mark_attendance, name='attendance'),
	path('<int:pk>/qr/', member_qr, name='qr'),
	path('<int:pk>/send-code/', send_member_code_email, name='send_code'),
	path('new/', create_member, name='create'),
	path('<int:pk>/edit/', edit_member, name='edit'),
	path('<int:pk>/delete/', delete_member, name='delete'),
]
