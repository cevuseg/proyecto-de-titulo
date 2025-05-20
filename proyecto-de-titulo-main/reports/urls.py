"""
Configuración de URLs para la aplicación de reportes.
Define las rutas para:
- Dashboard y visualización de reportes
- Gestión de roles y usuarios
- Sincronización con PBIRS
"""

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard y reportes
    path('', views.dashboard, name='dashboard'),
    path('reporte/<str:report_id>/', views.view_report, name='view_report'),
    
    # Gestión de roles
    path('roles/', views.RoleListView.as_view(), name='role_list'),
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='role_detail'),
    
    # Sincronización
    path('sync/', views.sync_reports, name='sync_reports'),

    # FALTANTES:
    path('manage_roles/', views.manage_roles, name='manage_roles'),
    path('manage_users/', views.manage_users, name='manage_users'),
] 