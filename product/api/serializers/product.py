from rest_framework import serializers
from product.models import Product, Manufacturer, ProductImage, ProductAttribute, ProductDiscount, RelatedProduct, ProductReview


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'se_name', 'is_active']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'position']


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value', 'description']


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ['id', 'discount_percent', 'start_date', 'end_date', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    images = ProductImageSerializer(many=True)
    attributes = ProductAttributeSerializer(many=True)
    discounts = ProductDiscountSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'price', 'final_price', 'in_stock',
            'created_on', 'updated_on', 'manufacturer', 'color', 'guarantee_option',
            'images', 'attributes', 'discounts', 'is_external', 'added_value_percent'
        ]

    def update(self, instance, validated_data):
        # به‌روزرسانی فیلدهای محصول
        instance = super().update(instance, validated_data)
        # محاسبه و به‌روزرسانی قیمت نهایی
        instance.update_final_price()
        return instance


class RelatedProductSerializer(serializers.ModelSerializer):
    related_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = RelatedProduct
        fields = ["id", "product", "related_product"]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductReview
        fields = ["id", "product", "user", "rating", "review_text", "created_at"]
        read_only_fields = ["created_at"]
