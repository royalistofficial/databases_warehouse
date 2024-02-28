from django.contrib import admin

from .models import Warehouse, WarehouseProducts

admin.site.register(Warehouse)
admin.site.register(WarehouseProducts)
