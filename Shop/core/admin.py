from django.contrib import admin
from django.utils import timezone


class BaseAdmin(admin.ModelAdmin):
    def logical_deleter(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
        queryset.update(is_deleted=True)
        queryset.update(is_active=False)

    def logical_restore(self, request, queryset):
        queryset.update(restored_at=timezone.now())
        queryset.update(is_deleted=False)
        queryset.update(is_active=True)

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    def activate(self, request, queryset):
        queryset.update(is_active=True)

    actions = ['logical_deleter', 'logical_restore', 'deactivate', 'activate']
