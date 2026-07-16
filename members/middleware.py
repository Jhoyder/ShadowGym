from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """Obliga a estar autenticado para ver cualquier pantalla,
    excepto login, admin y archivos estaticos/media."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path

            is_exempt = (
                path.startswith('/admin/')
                or path.startswith(settings.STATIC_URL)
                or (getattr(settings, 'MEDIA_URL', None) and path.startswith(settings.MEDIA_URL))
            )

            try:
                login_path = reverse('login')
            except Exception:
                login_path = '/login/'

            if not is_exempt and path != login_path:
                return redirect(login_path)

        return self.get_response(request)