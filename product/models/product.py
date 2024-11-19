from django.db import models
from django.utils import timezone
from painless.models import SlugMixin
from django.utils.text import slugify

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    se_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(SlugMixin):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    final_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    added_value_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    is_external = models.BooleanField(default=False)  # Add this field
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    guarantee_option = models.CharField(max_length=255, blank=True, null=True)

    def update_final_price(self):
        # calcullating final price with added_value_percent
        self.final_price = self.price * (1 + self.added_value_percent / 100)
        self.save(update_fields=['final_price'])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_products")
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_to")


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    rating = models.IntegerField()  # Rating from 1 to 5
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} Image {self.position}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductDiscount(models.Model):
    product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percent}% off on {self.product.name}"
