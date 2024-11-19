from django.contrib import admin
from product.models import Product, RelatedProduct, ProductReview, Manufacturer, ProductImage, ProductAttribute, ProductDiscount 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'in_stock', 'manufacturer', 'is_external','final_price', 'added_value_percent', )
    list_editable = ('added_value_percent',)
    search_fields = ('name', 'sku')
    list_filter = ('in_stock', 'manufacturer', 'is_external')
    readonly_fields = ('created_on', 'updated_on', 'is_external')

    def update_final_prices(self, request, queryset):
        for product in queryset:
            old_final_price = product.final_price
            product.final_price = product.price * (1 + product.added_value_percent / 100)
            product.save(update_fields=['final_price'])
            self.message_user(
                request,
                f"Updated {product.name}: {old_final_price} to {product.final_price}"
            )

    update_final_prices.short_description = "Update final prices based on added value percent"

    def save_model(self, request, obj, form, change):
        # ابتدا شیء را ذخیره کنید تا یک کلید اصلی به آن اختصاص داده شود
        super().save_model(request, obj, form, change)

        # سپس عملیات محاسبه و به روزرسانی را انجام دهید
        obj.final_price = obj.price * (1 + obj.added_value_percent / 100)
        super().save_model(request, obj, form, True) 



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'position', 'image_url')
    search_fields = ('product__name',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    search_fields = ('product__name', 'name')


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')


@admin.register(RelatedProduct)
class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'related_product')
    search_fields = ('product__name', 'related_product__name')
    list_filter = ('product',)
    raw_id_fields = ('product', 'related_product')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ['created_at']
    readonly_fields = ('created_at',)
