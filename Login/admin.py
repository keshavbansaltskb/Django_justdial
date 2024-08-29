from django.contrib import admin
from Login.models import Signup,History
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    fields = ["name","email","password","phone","bussiness"]
    list_display = ["id","name",'email',"phone","bussiness"]

admin.site.register(Signup,StudentAdmin)

class HistoryAdmin(admin.ModelAdmin):
    fields = ["name","email","password"]
    list_display = ["id","name","email"]

admin.site.register(History,HistoryAdmin)