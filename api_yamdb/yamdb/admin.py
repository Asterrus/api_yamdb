from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk','name','slug',)
    search_fields = ('name','slug',)
    list_filter = ('name','slug',)
    empty_value_display = '-пусто-'
    
admin.site.register(Category, CategoryAdmin)