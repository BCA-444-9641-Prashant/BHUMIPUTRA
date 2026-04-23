from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User management
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # Scheme management
    path('schemes/', views.scheme_home, name='scheme_home'),
    path('schemes/list/', views.scheme_list, name='scheme_list'),
    path('schemes/create/', views.scheme_create, name='scheme_create'),
    path('schemes/<int:pk>/update/', views.scheme_update, name='scheme_update'),
    path('schemes/<int:pk>/delete/', views.scheme_delete, name='scheme_delete'),
    
    # Crop management
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/create/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/update/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    
    # Equipment management
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/update/', views.equipment_update, name='equipment_update'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    
    # Course management
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Farm monitoring
    path('farms/', views.farm_monitoring, name='farm_monitoring'),
    path('farms/<int:pk>/update/', views.farm_update, name='farm_update'),
    path('farms/<int:pk>/delete/', views.farm_delete, name='farm_delete'),
    
    # CSRF Test
    path('csrf-test/', views.csrf_test, name='csrf_test'),
]
