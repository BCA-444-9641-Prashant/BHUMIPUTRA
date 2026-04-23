from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Farm, EquipmentOrder, CourseEnrollment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone', 'role', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'role')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'role')}),
    )

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'location', 'size', 'crop', 'soil_type', 'farm_status', 'created_at']
    list_filter = ['farm_status', 'soil_type', 'created_at']
    search_fields = ['farmer__username', 'location', 'crop']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(EquipmentOrder)
class EquipmentOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'equipment', 'start_date', 'end_date', 'total_cost', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'equipment__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrollment_date', 'status']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['user__username', 'course__name']
    readonly_fields = ['enrollment_date']
    ordering = ['-enrollment_date']
