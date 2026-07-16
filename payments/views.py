from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from .forms import PaymentForm
from .models import Payment

# Create your views here.


@login_required
def dashboard(request):
	"""Panel de pagos con resumen financiero y ultimos movimientos."""
	today = timezone.localdate()
	month_start = today.replace(day=1)

	payments = Payment.objects.select_related('member', 'plan').order_by('-payment_date')
	methods_map = dict(Payment.PAYMENT_METHODS)

	methods = payments.values('method').annotate(
		total=Count('id'),
		amount=Sum('amount'),
	).order_by('-amount')

	for row in methods:
		row['label'] = methods_map.get(row['method'], row['method'])

	context = {
		'total_payments': payments.count(),
		'month_payments': payments.filter(payment_date__gte=month_start).count(),
		'total_revenue': payments.aggregate(sum=Sum('amount'))['sum'] or 0,
		'month_revenue': payments.filter(payment_date__gte=month_start).aggregate(sum=Sum('amount'))['sum'] or 0,
		'recent_payments': payments[:20],
		'methods': methods,
	}
	return render(request, 'payments/index.html', context)


@login_required
def create_payment(request):
	"""Crea un nuevo pago desde el dashboard."""
	form = PaymentForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Pago creado correctamente.')
		return redirect('payments:index')

	return render(request, 'dashboard/form.html', {
		'form': form,
		'title': 'Nuevo pago',
		'cancel_url': 'payments:index',
	})


@login_required
def edit_payment(request, pk):
	"""Edita un pago existente."""
	payment = get_object_or_404(Payment, pk=pk)
	form = PaymentForm(request.POST or None, instance=payment)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Pago actualizado correctamente.')
		return redirect('payments:index')

	return render(request, 'dashboard/form.html', {
		'form': form,
		'title': f'Editar pago: {payment}',
		'cancel_url': 'payments:index',
	})


@login_required
def delete_payment(request, pk):
	"""Elimina un pago con confirmacion previa."""
	payment = get_object_or_404(Payment, pk=pk)
	if request.method == 'POST':
		payment.delete()
		messages.success(request, 'Pago eliminado correctamente.')
		return redirect('payments:index')

	return render(request, 'dashboard/confirm_delete.html', {
		'title': 'Eliminar pago',
		'object_name': str(payment),
		'cancel_url': 'payments:index',
	})
