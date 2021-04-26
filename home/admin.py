from django.contrib import admin
from .models import Book, Chapter, Tag, Genre, Person
# Register your models here.

class TagAdmin(admin.ModelAdmin):     
    prepopulated_fields = {"slug": ("name",)}


class GenreAdmin(admin.ModelAdmin):     
    prepopulated_fields = {"slug": ("name",)}
 
admin.site.register(Tag, TagAdmin)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Person)
admin.site.register(Genre, GenreAdmin)