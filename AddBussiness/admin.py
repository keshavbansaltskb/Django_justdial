from django.contrib import admin
from .models import Business,Search, Message, Gallery,Lead,Adv
from django.utils.html import format_html
# New Bussiness
class BusinessAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        return format_html('<img src="{}" style="width:100px;height:100px">'.format(obj.image.url))
    
    list_display = ('id','title','district', 'category', 'image_tag')

admin.site.register(Business, BusinessAdmin)

# Bussiness Search
class SearchAdmin(admin.ModelAdmin):
    list_display = ('id','business_id', 'city')

admin.site.register(Search, SearchAdmin)

#User Rating
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','business_id', 'user','rating','message')

admin.site.register(Message, MessageAdmin)

# Bussiness Gallery
class GalleryAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        return format_html('<img src="{}" style="width:100px;height:100px">'.format(obj.image.url))
    
    list_display = ('id','business_id', 'image_tag')

admin.site.register(Gallery, GalleryAdmin)

# Bussiness Lead 
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','business_id','user','email','search','location')

admin.site.register(Lead,LeadAdmin)

# Advertisement
class AdvertisementAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        return format_html('<img src="{}" style="width:100px;height:100px">'.format(obj.image.url))
    list_display = ('id','business_email','option1','option2','option3','option4','image_tag')

admin.site.register(Adv,AdvertisementAdmin)
