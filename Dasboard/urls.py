from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard_full'),
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
    path('dashboard/partial/', views.dashboard_partial, name='dashboard_partial'),
    path('', views.index, name='index'),
    path('general/', views.dashboard_general, name='dashboard_general'),

    # --- CÓDIGO AÑADIDO ---
    # Rutas para la exportación de datos del sensor
    path('export/csv/<str:sensor_id>/', views.export_sensor_csv, name='export_sensor_csv'),
    path('export/excel/<str:sensor_id>/', views.export_sensor_excel, name='export_sensor_excel'),
]