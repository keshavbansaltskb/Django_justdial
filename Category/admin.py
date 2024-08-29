from django.contrib import admin
from .models import Category
from django.utils.html import format_html
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        return format_html('<img src="{}" style="width:100px;height:100px">'.format(obj.image.url))
    
    list_display=["id","category","image_tag"]

admin.site.register(Category,CategoryAdmin)