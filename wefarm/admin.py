from models import Farmer
from django.contrib import admin

# Admin


class FarmerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Farmer, FarmerAdmin)
