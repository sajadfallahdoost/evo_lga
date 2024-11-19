import requests
from django.utils import timezone
from product.models import Product, Manufacturer, ProductImage, ProductAttribute

API_ENDPOINT = "https://staging.hamrahtel.com/api/categories/20/products"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOiIxNzI4NzM2NjA0IiwiZXhwIjoiMTczNjUxNjIwNCIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL2VtYWlsYWRkcmVzcyI6IjA5MTIyMDE4MzAwQGhhbXJhaHRlbC5jb20iLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjI1M2M3NGE3LTEwZjAtNGVhZS1hMDJhLTNhZWVkZjg0OTgzMiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiIwOTEyMjAxODMwMCIsIkN1c3RvbWVySWQiOiIxNjg0OTY2In0.a4VjnLSMqqSz5fVeMQy8XlIdk5lE2QvAT5NG7s4A_2c"


def fetch_and_bulk_save_products():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    manufacturers_cache = {m.name: m for m in Manufacturer.objects.all()}
    page = 1  # Start with page 0

    while True:
        # Add page parameter to the API URL
        next_page_url = f"{API_ENDPOINT}?page={page}"

        response = requests.get(next_page_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            break

        data = response.json()
        products_data = data.get('products', [])

        # Stop the loop if no products are returned (indicating the last page)
        if not products_data:
            print("All products have been fetched.")
            break

        for item in products_data:
            # Manufacturer Handling
            manufacturers = item.get('manufacturers', [])
            manufacturer_name = manufacturers[0].get('name', 'Unknown Manufacturer') if manufacturers else 'Unknown Manufacturer'
            manufacturer = manufacturers_cache.get(manufacturer_name)
            if not manufacturer:
                manufacturer = Manufacturer(name=manufacturer_name, se_name=item.get('se_name', ''))
                manufacturer.save()
                manufacturers_cache[manufacturer_name] = manufacturer

            # Handle colors and unique SKUs
            color_data = item.get('attributes', [{}])[0].get('attribute_values', [{}])
            color = color_data[0].get('name', 'Default') if color_data else 'Default'

            # Update or create the product
            product, created = Product.objects.update_or_create(
                sku=item.get('sku', ''),
                defaults={
                    "name": item.get('name', ''),
                    "description": item.get('short_description', ''),
                    "price": item.get('price', 0.0),
                    "final_price": item.get('final_price_value', 0.0),
                    "in_stock": item.get('in_stock', True),
                    "created_on": item.get('created_on_utc', timezone.now()),
                    "updated_on": timezone.now(),
                    "manufacturer": manufacturer,
                    "color": color,
                    "guarantee_option": item.get('guarantee_option', 'No Guarantee'),
                    "is_external": True,
                }
            )

            # Clear out existing images and attributes if updating
            if not created:
                product.images.all().delete()
                product.attributes.all().delete()

            # Add images
            images = item.get('images', [])
            for index, image_data in enumerate(images):
                image_url = image_data.get('src')
                if image_url:
                    ProductImage.objects.create(
                        product=product,
                        image_url=image_url,
                        position=index
                    )

            # Add attributes
            attribute_groups = item.get('product_specification', {}).get('groups', [])
            for group in attribute_groups:
                attributes = group.get('attributes', [])
                for attribute in attributes:
                    attr_name = attribute.get('name')
                    attr_value = attribute.get('value')
                    if attr_name and attr_value:
                        ProductAttribute.objects.create(
                            product=product,
                            name=attr_name,
                            value=attr_value,
                            description=attribute.get('description', '')
                        )

        # Move to the next page
        page += 1

    print("All products have been successfully fetched and upserted.")
