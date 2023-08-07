from django.contrib import admin

from .models import Blog

# Register your models here.
# admin.site.register(Student)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug',)
    list_filter = ('title',)
    search_fields = ('description',)


admin.site.register(Blog, BlogAdmin)

