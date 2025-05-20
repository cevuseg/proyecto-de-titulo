"""
Vistas para el sistema de reportes Power BI.
Este módulo maneja:
- Autenticación y autorización de usuarios
- Visualización de reportes
- Gestión de roles y permisos
- Panel de administración
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Role, UserRole, PowerBIReport
from django.contrib.auth.models import User
from azure.identity import ClientSecretCredential
from azure.mgmt.powerbiembedded import PowerBIEmbeddedManagementClient
from django.conf import settings
import msal
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from powerbi_reports.pbirs_client import PBIRSClient
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from collections import defaultdict

logger = logging.getLogger(__name__)

# reports/views.py: Contiene las vistas de Django para dashboards, gestión de reportes, roles y usuarios.

@login_required
def dashboard(request):
    """
    Vista principal del dashboard.
    Muestra los reportes disponibles para el usuario según sus roles.
    """
    try:
        # Obtener roles del usuario
        user_roles = UserRole.objects.filter(user=request.user).select_related('role')
        roles = [ur.role for ur in user_roles]

        # Obtener reportes disponibles para los roles del usuario
        reports = PowerBIReport.objects.filter(roles__in=roles).distinct()

        # Verificar permisos en PBIRS
        pbirs_client = PBIRSClient()
        accessible_reports = []
        for report in reports:
            if pbirs_client.check_permissions(report.report_id, request.user.username):
                accessible_reports.append(report)

        # Mostrar acceso a PBIRS solo a admin/staff
        mostrar_pbirs = request.user.is_superuser or request.user.is_staff
        pbirs_url = getattr(settings, 'PBIRS_CONFIG', {}).get('REPORT_MANAGER_URL', '#')

        context = {
            'reports': accessible_reports,
            'roles': roles,
            'mostrar_pbirs': mostrar_pbirs,
            'pbirs_url': pbirs_url,
        }
        return render(request, 'reports/dashboard.html', context)
    except Exception as e:
        import traceback
        error_message = f"Error en dashboard: {e}\n{traceback.format_exc()}"
        return render(request, 'reports/dashboard.html', {'error_message': error_message})

@login_required
def view_report(request, report_id):
    """
    Vista para mostrar un reporte específico.
    Verifica permisos y redirige al visor de PBIRS.
    """
    try:
        report = get_object_or_404(PowerBIReport, report_id=report_id)
        
        # Verificar si el usuario tiene acceso al reporte
        user_roles = UserRole.objects.filter(user=request.user).select_related('role')
        user_role_ids = [ur.role.id for ur in user_roles]
        
        if not report.roles.filter(id__in=user_role_ids).exists():
            messages.error(request, "No tienes permiso para ver este reporte")
            return redirect('reports:dashboard')

        # Verificar permisos en PBIRS
        pbirs_client = PBIRSClient()
        if not pbirs_client.check_permissions(report.report_id, request.user.username):
            messages.error(request, "No tienes permiso para ver este reporte en PBIRS")
            return redirect('reports:dashboard')

        # Redirigir al visor de PBIRS
        return redirect(report.get_absolute_url())
    except Exception as e:
        logger.error(f"Error al ver reporte {report_id}: {e}")
        messages.error(request, "Error al cargar el reporte")
        return redirect('reports:dashboard')

@user_passes_test(lambda u: u.is_authenticated)
def manage_roles(request):
    """
    Vista para gestionar roles: crear, editar, eliminar roles y asignar reportes a roles y roles a usuarios.
    Solo accesible para usuarios con permisos de administrador.
    """
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos suficientes para acceder a esta sección. Si crees que esto es un error, contacta al administrador.')
        return redirect('reports:dashboard')

    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para gestionar roles.')
        return redirect('dashboard')

    # Barra de búsqueda de roles
    search_query = request.GET.get('search', '').strip()

    # Crear rol
    if request.method == 'POST' and 'create_role' in request.POST:
        name = request.POST.get('role_name', '').strip()
        description = request.POST.get('role_description', '').strip()
        windows_group = request.POST.get('windows_group', '').strip()
        report_ids = request.POST.getlist('role_reports')
        if not name:
            messages.error(request, 'El nombre del rol es obligatorio.')
        elif Role.objects.filter(name=name).exists():
            messages.error(request, f'Ya existe un rol con el nombre "{name}".')
        elif not report_ids:
            messages.warning(request, 'Se recomienda asignar al menos un reporte al rol.')
            role = Role.objects.create(name=name, description=description, windows_group=windows_group)
            role.reports.clear()
            messages.success(request, f'Rol "{name}" creado sin reportes asignados.')
        else:
            role = Role.objects.create(name=name, description=description, windows_group=windows_group)
            role.reports.set(PowerBIReport.objects.filter(id__in=report_ids))
            messages.success(request, f'Rol "{name}" creado exitosamente.')
        return redirect('reports:manage_roles')

    # Editar rol
    if request.method == 'POST' and 'edit_role_id' in request.POST:
        role = Role.objects.get(id=request.POST.get('edit_role_id'))
        new_name = request.POST.get('role_name', '').strip()
        description = request.POST.get('role_description', '').strip()
        windows_group = request.POST.get('windows_group', '').strip()
        report_ids = request.POST.getlist('role_reports')
        if not new_name:
            messages.error(request, 'El nombre del rol es obligatorio.')
        elif Role.objects.exclude(id=role.id).filter(name=new_name).exists():
            messages.error(request, f'Ya existe otro rol con el nombre "{new_name}".')
        else:
            role.name = new_name
            role.description = description
            role.windows_group = windows_group
            role.save()
            if report_ids is not None:
                role.reports.set(PowerBIReport.objects.filter(id__in=report_ids))
            if not report_ids:
                messages.warning(request, 'Este rol no tiene reportes asignados.')
            messages.success(request, f'Rol "{new_name}" actualizado exitosamente.')
        return redirect('reports:manage_roles')

    # Eliminar rol
    if request.method == 'POST' and 'delete_role_id' in request.POST:
        role = Role.objects.get(id=request.POST.get('delete_role_id'))
        role_name = role.name
        role.delete()
        messages.success(request, f'Rol "{role_name}" eliminado exitosamente.')
        return redirect('reports:manage_roles')

    # Asignar roles a usuarios (ya existente)
    if request.method == 'POST' and 'action' in request.POST:
        user_id = request.POST.get('user')
        role_id = request.POST.get('role')
        action = request.POST.get('action')
        try:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
            if action == 'add':
                UserRole.objects.get_or_create(user=user, role=role)
                messages.success(request, f'Rol "{role.name}" asignado a {user.username}.')
            elif action == 'remove':
                UserRole.objects.filter(user=user, role=role).delete()
                messages.success(request, f'Rol "{role.name}" removido de {user.username}.')
        except (User.DoesNotExist, Role.DoesNotExist):
            messages.error(request, 'Usuario o rol inválido seleccionado.')
        return redirect('reports:manage_roles')

    # Obtener todos los usuarios, roles, reportes y asignaciones actuales
    users = User.objects.all()
    reports = PowerBIReport.objects.all()
    roles = Role.objects.all()
    if search_query:
        roles = roles.filter(name__icontains=search_query)
    user_roles = UserRole.objects.all().select_related('user', 'role')
    # Conteo de usuarios por rol
    role_user_count = {role.id: UserRole.objects.filter(role=role).count() for role in roles}

    context = {
        'users': users,
        'roles': roles,
        'reports': reports,
        'user_roles': user_roles,
        'role_user_count': role_user_count,
        'search_query': search_query,
    }
    return render(request, 'reports/manage_roles.html', context)

@user_passes_test(lambda u: u.is_authenticated)
def manage_users(request):
    """
    Vista para administrar usuarios: listar, crear, editar y eliminar usuarios (solo staff/superusuario).
    """
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos suficientes para acceder a esta sección. Si crees que esto es un error, contacta al administrador.')
        return redirect('reports:dashboard')

    users = User.objects.all()
    user_form = UserCreationForm()
    edit_user = None
    edit_form = None

    # Crear usuario
    if request.method == 'POST' and 'create_user' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_active = True if request.POST.get('is_active') == 'on' else False
        is_staff = True if request.POST.get('is_staff') == 'on' else False
        is_superuser = True if request.POST.get('is_superuser') == 'on' else False
        if password1 == password2 and username:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create(
                    username=username,
                    email=email,
                    is_active=is_active,
                    is_staff=is_staff,
                    is_superuser=is_superuser,
                    password=make_password(password1)
                )
                messages.success(request, 'Usuario creado exitosamente.')
            else:
                messages.error(request, 'El nombre de usuario ya existe.')
        else:
            messages.error(request, 'Las contraseñas no coinciden o falta el nombre de usuario.')
        return redirect('reports:manage_users')

    # Editar usuario
    if request.method == 'POST' and 'edit_user_id' in request.POST:
        edit_user = User.objects.get(id=request.POST.get('edit_user_id'))
        edit_user.username = request.POST.get('username')
        edit_user.email = request.POST.get('email')
        edit_user.is_active = True if request.POST.get('is_active') == 'on' else False
        edit_user.is_staff = True if request.POST.get('is_staff') == 'on' else False
        edit_user.is_superuser = True if request.POST.get('is_superuser') == 'on' else False
        # Cambiar contraseña si se ingresan los campos
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if new_password1 or new_password2:
            if new_password1 == new_password2 and new_password1.strip() != '':
                edit_user.set_password(new_password1)
                messages.success(request, 'Contraseña actualizada exitosamente.')
            else:
                messages.error(request, 'Las contraseñas no coinciden o están vacías. La contraseña no se actualizó.')
        edit_user.save()
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('reports:manage_users')

    # Eliminar usuario
    if request.method == 'POST' and 'delete_user_id' in request.POST:
        user_to_delete = User.objects.get(id=request.POST.get('delete_user_id'))
        if user_to_delete != request.user:
            user_to_delete.delete()
            messages.success(request, 'Usuario eliminado exitosamente.')
        else:
            messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('reports:manage_users')

    # Si se va a editar, cargar el formulario con los datos del usuario
    if request.method == 'GET' and 'edit' in request.GET:
        edit_user = User.objects.get(id=request.GET.get('edit'))
        edit_form = UserChangeForm(instance=edit_user)

    context = {
        'users': users,
        'user_form': user_form,
        'edit_user': edit_user,
        'edit_form': edit_form,
    }
    return render(request, 'reports/manage_users.html', context)

class RoleListView(LoginRequiredMixin, ListView):
    """
    Vista para listar roles.
    Solo accesible para administradores.
    """
    model = Role
    template_name = 'reports/role_list.html'
    context_object_name = 'roles'

    def get_queryset(self):
        """Filtra roles según permisos del usuario."""
        if not self.request.user.is_staff:
            return Role.objects.none()
        return Role.objects.all()

class RoleDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para ver detalles de un rol.
    Muestra usuarios y reportes asociados.
    """
    model = Role
    template_name = 'reports/role_detail.html'
    context_object_name = 'role'

    def get_context_data(self, **kwargs):
        """Agrega información adicional al contexto."""
        context = super().get_context_data(**kwargs)
        role = self.get_object()
        context['users'] = UserRole.objects.filter(role=role).select_related('user')
        context['reports'] = role.reports.all()
        return context

@login_required
def sync_reports(request):
    """
    Vista para sincronizar reportes con PBIRS.
    Solo accesible para administradores.
    """
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para realizar esta acción")
        return redirect('reports:dashboard')

    try:
        pbirs_client = PBIRSClient()
        reports = pbirs_client.get_reports()
        
        for report in reports:
            PowerBIReport.objects.update_or_create(
                report_id=report['Id'],
                defaults={
                    'name': report['Name'],
                    'description': report.get('Description', ''),
                    'workspace_id': report.get('Path', ''),
                    'path': report.get('Path', '')
                }
            )
        
        messages.success(request, "Reportes sincronizados correctamente")
    except Exception as e:
        logger.error(f"Error al sincronizar reportes: {e}")
        messages.error(request, "Error al sincronizar reportes")
    
    return redirect('reports:dashboard')
