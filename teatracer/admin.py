from django.contrib import admin
from .models import Unit,ProductType,Product,Provider,Taker,Room,PickingPeriod,MovementType

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    readonly_fields = ['created_at', 'updated_at']



@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku', 'product_type', 'is_final', 'created_at']
    list_filter = ['product_type', 'is_final']
    search_fields = ['name', 'sku']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'conversion_to_kg', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at', 'updated_at']  
    
    
@admin.register(Taker)
class TakerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'created_at']
    search_fields = ['name', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']   
    
    
@admin.register(Room) 
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PickingPeriod)
class PickingPeriodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']
    
    
    
@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
