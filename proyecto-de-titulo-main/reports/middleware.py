"""
Middleware para la aplicación de reportes.
Proporciona funcionalidades de:
- Autenticación y autorización
- Registro de acceso a reportes
- Manejo de errores
"""

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class ReportAccessMiddleware(MiddlewareMixin):
    """
    Middleware para controlar el acceso a los reportes.
    Verifica permisos y registra accesos.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Procesa la vista antes de su ejecución.
        Verifica permisos y registra el acceso.
        """
        # Ignorar si no es una vista de reporte
        if not hasattr(view_func, 'view_name') or view_func.view_name != 'view_report':
            return None

        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Debe iniciar sesión para ver reportes")
            return redirect('login')

        # Registrar el acceso
        logger.info(
            f"Acceso a reporte: {view_kwargs.get('report_id')} "
            f"por usuario: {request.user.username}"
        )

        return None

class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware para manejar errores de la aplicación.
    Proporciona mensajes de error amigables y registra errores.
    """
    def process_exception(self, request, exception):
        """
        Procesa las excepciones no manejadas.
        Registra el error y muestra un mensaje apropiado.
        """
        # Registrar el error
        logger.error(
            f"Error en {request.path}: {str(exception)}",
            exc_info=True
        )

        # Mostrar mensaje de error
        messages.error(
            request,
            "Ha ocurrido un error. Por favor, intente nuevamente."
        )

        # Redirigir al dashboard
        return redirect('reports:dashboard')

class LoggingMiddleware(MiddlewareMixin):
    """
    Middleware para registro de actividad.
    Registra información sobre las peticiones y respuestas.
    """
    def process_request(self, request):
        """
        Registra información de la petición.
        """
        if request.user.is_authenticated:
            logger.info(
                f"Petición: {request.method} {request.path} "
                f"por usuario: {request.user.username}"
            )

    def process_response(self, request, response):
        """
        Registra información de la respuesta.
        """
        if request.user.is_authenticated:
            logger.info(
                f"Respuesta: {response.status_code} para {request.path} "
                f"por usuario: {request.user.username}"
            )
        return response 