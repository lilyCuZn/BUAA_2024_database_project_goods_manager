from django.contrib import admin

from .models import Member, Department, Category, ApprovalRecord, UserApplication
from .models import Material, MaintainRecord
from .models import Supplier, Supplier_Product, PurchaseOrder
from .models import Warehouse, Zone, Shelf, Level
from .models import Location, StockWarning

# Register your models here.
admin.site.register(Department)
admin.site.register(Member)
admin.site.register(Category)
admin.site.register(ApprovalRecord)
admin.site.register(Material)
admin.site.register(UserApplication)
admin.site.register(MaintainRecord)
admin.site.register(Supplier)
admin.site.register(Supplier_Product)
admin.site.register(PurchaseOrder)
admin.site.register(Warehouse)
admin.site.register(Zone)
admin.site.register(Shelf)
admin.site.register(Level)
admin.site.register(Location)
admin.site.register(StockWarning)


