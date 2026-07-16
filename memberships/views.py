from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect

from .forms import PlanForm
from .models import Plan

# Create your views here.


@login_required
def dashboard(request):
	"""Panel de membresias con estadisticas de planes."""
	plans = Plan.objects.annotate(
		total_payments=Count('payment'),
		active_members=Count('payment__member', filter=Q(payment__member__is_active=True), distinct=True),
	).order_by('name')

	context = {
		'plans': plans,
		'total_plans': plans.count(),
		'average_price': Plan.objects.aggregate(avg=Avg('price'))['avg'] or 0,
		'total_active_links': sum(plan.active_members for plan in plans),
	}
	return render(request, 'memberships/index.html', context)


@login_required
def create_plan(request):
	"""Crea un nuevo plan de membresia."""
	form = PlanForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Plan creado correctamente.')
		return redirect('memberships:index')

	return render(request, 'dashboard/form.html', {
		'form': form,
		'title': 'Nuevo plan',
		'cancel_url': 'memberships:index',
	})


@login_required
def edit_plan(request, pk):
	"""Edita un plan existente."""
	plan = get_object_or_404(Plan, pk=pk)
	form = PlanForm(request.POST or None, instance=plan)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Plan actualizado correctamente.')
		return redirect('memberships:index')

	return render(request, 'dashboard/form.html', {
		'form': form,
		'title': f'Editar plan: {plan.name}',
		'cancel_url': 'memberships:index',
	})


@login_required
def delete_plan(request, pk):
	"""Elimina un plan con confirmacion previa."""
	plan = get_object_or_404(Plan, pk=pk)
	if request.method == 'POST':
		plan.delete()
		messages.success(request, 'Plan eliminado correctamente.')
		return redirect('memberships:index')

	return render(request, 'dashboard/confirm_delete.html', {
		'title': 'Eliminar plan',
		'object_name': plan.name,
		'cancel_url': 'memberships:index',
	})
