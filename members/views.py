from io import BytesIO

import qrcode
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


class MemberLoginView(auth_views.LoginView):
    template_name = 'members/login.html'
    redirect_authenticated_user = True


# Ejemplo de proteccion explicita (el middleware ya lo hace,
# pero puedes usar el decorador si prefieres control por vista):
# @login_required
# def dashboard(request):
#     ...

from .forms import AttendanceCodeForm, MemberForm
from .models import Attendance, Member

# Create your views here.


def clear_old_attendance(today):
	"""Elimina asistencias de dias anteriores para mantener solo el dia actual."""
	Attendance.objects.filter(date__lt=today).delete()


def can_member_enter(member, today):
	"""Valida si el miembro puede ingresar segun estado y vigencia de membresia."""
	if not member.is_active:
		return False, 'Cliente inactivo. No puede ingresar.'

	if member.membership_end and member.membership_end < today:
		return False, 'Membresia vencida. No puede ingresar.'

	if member.membership_start and member.membership_start > today:
		return False, 'La membresia aun no inicia. No puede ingresar.'

	return True, ''


def build_qr_png_bytes(data):
	"""Genera una imagen PNG en memoria para el QR."""
	qr = qrcode.QRCode(version=1, box_size=8, border=2)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill_color='black', back_color='white')
	buffer = BytesIO()
	img.save(buffer, format='PNG')
	return buffer.getvalue()


@login_required
def dashboard(request):
	"""Panel principal de miembros con resumen y listado reciente."""
	today = timezone.localdate()
	clear_old_attendance(today)
	soon_limit = today + timedelta(days=7)
	attendance_filter = request.GET.get('attendance', 'all')

	members_qs = Member.objects.order_by('-created_at')
	all_members_qs = Member.objects.order_by('last_name', 'first_name')
	today_attendance_qs = Attendance.objects.filter(date=today).select_related('member')
	today_attendance_map = {item.member_id: item for item in today_attendance_qs}
	checked_today_ids = list(today_attendance_map.keys())

	if attendance_filter == 'checked':
		filtered_members_qs = all_members_qs.filter(id__in=checked_today_ids)
	elif attendance_filter == 'pending':
		filtered_members_qs = all_members_qs.exclude(id__in=checked_today_ids)
	else:
		attendance_filter = 'all'
		filtered_members_qs = all_members_qs

	visible_members = list(filtered_members_qs[:30])
	for member in visible_members:
		today_mark = today_attendance_map.get(member.id)
		member.checked_today = bool(today_mark)
		member.checked_time = today_mark.marked_at if today_mark else None

	context = {
		'total_members': members_qs.count(),
		'active_members': members_qs.filter(is_active=True).count(),
		'inactive_members': members_qs.filter(is_active=False).count(),
		'expiring_soon': members_qs.filter(
			membership_end__isnull=False,
			membership_end__gte=today,
			membership_end__lte=soon_limit,
		).count(),
		'attendance_today': len(checked_today_ids),
		'pending_today': max(0, members_qs.count() - len(checked_today_ids)),
		'attendance_filter': attendance_filter,
		'today': today,
		'checked_today_ids': checked_today_ids,
		'attendance_code_form': AttendanceCodeForm(),
		'recent_members': members_qs[:8],
		'recent_attendance': today_attendance_qs.order_by('-marked_at')[:8],
		'all_members': visible_members,
	}
	return render(request, 'members/index.html', context)


@login_required
def mark_attendance_by_code(request):
	"""Marca asistencia mediante codigo de acceso (o cedula)."""
	if request.method != 'POST':
		messages.warning(request, 'Metodo no permitido para registrar por codigo.')
		return redirect('members:index')

	form = AttendanceCodeForm(request.POST)
	if not form.is_valid():
		messages.error(request, 'Ingresa un codigo valido.')
		return redirect('members:index')

	code = form.cleaned_data['code']
	today = timezone.localdate()
	clear_old_attendance(today)

	member = Member.objects.filter(
		Q(access_code__iexact=code) | Q(id_number__iexact=code)
	).first()

	if not member:
		messages.error(request, 'Codigo no encontrado.')
		return redirect('members:index')

	can_enter, reason = can_member_enter(member, today)
	if not can_enter:
		messages.error(request, f'{member}: {reason}')
		return redirect('members:index')

	_, created = Attendance.objects.get_or_create(member=member, date=today)
	if created:
		messages.success(request, f'Ingreso registrado para {member}.')
	else:
		messages.warning(request, f'{member} ya marco asistencia hoy.')

	return redirect('members:index')


@login_required
def mark_attendance(request, pk):
	"""Marca la asistencia diaria de un miembro una sola vez por dia."""
	if request.method != 'POST':
		messages.warning(request, 'Metodo no permitido para marcar asistencia.')
		return redirect('members:index')

	member = get_object_or_404(Member, pk=pk)
	today = timezone.localdate()
	clear_old_attendance(today)
	can_enter, reason = can_member_enter(member, today)
	if not can_enter:
		messages.error(request, f'{member}: {reason}')
		return redirect('members:index')

	_, created = Attendance.objects.get_or_create(member=member, date=today)

	if created:
		messages.success(request, f'Asistencia marcada para {member}.')
	else:
		messages.warning(request, f'{member} ya marco asistencia hoy.')

	return redirect('members:index')


@login_required
def member_qr(request, pk):
	"""Devuelve la imagen QR del codigo de acceso del miembro."""
	member = get_object_or_404(Member, pk=pk)
	png_bytes = build_qr_png_bytes(member.access_code)
	response = HttpResponse(png_bytes, content_type='image/png')
	response['Content-Disposition'] = f'inline; filename="qr_{member.id}.png"'
	return response


@login_required
def send_member_code_email(request, pk):
	"""Envia por correo el codigo de acceso y su QR al miembro."""
	if request.method != 'POST':
		messages.warning(request, 'Metodo no permitido para envio de codigo.')
		return redirect('members:index')

	member = get_object_or_404(Member, pk=pk)
	if not member.email:
		messages.error(request, f'{member} no tiene correo registrado.')
		return redirect('members:index')

	body = (
		f'Hola {member.first_name},\\n\\n'
		'Este es tu codigo de acceso para ShadowGym.\\n'
		f'Codigo: {member.access_code}\\n\\n'
		'Puedes presentar el codigo o el QR adjunto para registrar tu ingreso.\\n'
	)

	try:
		email = EmailMessage(
			subject='Tu codigo de acceso - ShadowGym',
			body=body,
			to=[member.email],
		)
		email.attach(
			filename=f'shadowgym_qr_{member.id}.png',
			content=build_qr_png_bytes(member.access_code),
			mimetype='image/png',
		)
		email.send(fail_silently=False)
		messages.success(request, f'Codigo enviado por correo a {member.email}.')
	except Exception:
		messages.error(request, 'No se pudo enviar el correo. Revisa la configuracion SMTP.')

	return redirect('members:index')


@login_required
def create_member(request):
	"""Crea un nuevo miembro desde el dashboard."""
	form = MemberForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Miembro creado correctamente.')
		return redirect('members:index')

	return render(request, 'dashboard/form.html', {
		'form': form,
		'title': 'Nuevo miembro',
		'cancel_url': 'members:index',
	})


@login_required
def edit_member(request, pk):
	"""Edita un miembro existente desde el dashboard."""
	member = get_object_or_404(Member, pk=pk)
	form = MemberForm(request.POST or None, instance=member)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Miembro actualizado correctamente.')
		return redirect('members:index')

	return render(request, 'dashboard/form.html', {
		'form': form,
		'title': f'Editar miembro: {member}',
		'cancel_url': 'members:index',
	})


@login_required
def delete_member(request, pk):
	"""Elimina un miembro con confirmacion previa."""
	member = get_object_or_404(Member, pk=pk)
	if request.method == 'POST':
		member.delete()
		messages.success(request, 'Miembro eliminado correctamente.')
		return redirect('members:index')

	return render(request, 'dashboard/confirm_delete.html', {
		'title': 'Eliminar miembro',
		'object_name': str(member),
		'cancel_url': 'members:index',
	})
