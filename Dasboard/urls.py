from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard_full'),
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
    path('dashboard/partial/', views.dashboard_partial, name='dashboard_partial'),
    path('', views.index, name='index'),
]
