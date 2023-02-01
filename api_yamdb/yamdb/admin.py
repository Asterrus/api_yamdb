from django.contrib import admin

from .models import Category, Genre, Title

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('pk','name','slug',)
#     search_fields = ('name','slug',)
#     list_filter = ('name','slug',)
#     empty_value_display = '-пусто-'
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'  
    
    
@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    
