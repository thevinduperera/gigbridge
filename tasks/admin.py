# We register our models here so they show up in the admin panel.
# The admin is mainly used to add Categories and Skills since clients and freelancers can't create those themselves.

from django.contrib import admin
from .models import Category, Skill, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug', 'icon']
    search_fields       = ['name']
    prepopulated_fields = {'slug': ('name',)}  # auto-fills slug as you type the name


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display    = ['title', 'client', 'category', 'status', 'deadline', 'created_at']
    list_filter     = ['status', 'category']
    search_fields   = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']  # these are auto-set so no point editing them manually
    