from decimal import Decimal
from django.db import migrations
from django.utils.text import slugify


PRODUCT_NAMES = [
    'Everyday Essential', 'Premium Choice', 'Classic Edition', 'Smart Upgrade',
    'Compact Set', 'Home Favorite', 'New Arrival', 'Value Pick',
    'Limited Find', 'Practical Bundle', 'Modern Select', 'Reliable Choice',
    'Popular Model', 'Weekend Special', 'Simple Starter', 'Deluxe Version',
    'Fresh Stock', 'Trusted Basic', 'Complete Kit', 'Signature Pick',
]


def seed_products(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Category = apps.get_model('marketplace', 'Category')
    Product = apps.get_model('marketplace', 'Product')

    seller, _ = User.objects.get_or_create(
        username='marketgo_demo_seller',
        defaults={
            'first_name': 'MarketGo',
            'last_name': 'Seller',
            'email': 'seller@marketgo.local',
            'is_active': True,
        },
    )
    seller.password = '!'
    seller.save(update_fields=['password'])

    for category in Category.objects.all():
        for index, product_name in enumerate(PRODUCT_NAMES, start=1):
            name = f'{category.name} - {product_name}'
            Product.objects.get_or_create(
                category=category,
                name=name,
                defaults={
                    'seller': seller,
                    'slug': f'{slugify(category.name)}-{slugify(product_name)}-{category.pk}',
                    'description': f'{product_name} from the {category.name.lower()} category. A quality marketplace find from a local MarketGo seller.',
                    'price': Decimal(75 + (index * 42) + (category.pk * 9)),
                    'condition': 'new' if index % 4 == 0 else 'good',
                    'location': ['Accra', 'Kumasi', 'Takoradi', 'Tema'][category.pk % 4],
                    'brand': 'MarketGo Select',
                    'quantity': 5 + (index % 6),
                    'negotiable': index % 3 == 0,
                    'featured': index <= 2,
                    'active': True,
                },
            )


def remove_products(apps, schema_editor):
    Product = apps.get_model('marketplace', 'Product')
    Product.objects.filter(seller__username='marketgo_demo_seller').delete()


class Migration(migrations.Migration):
    dependencies = [('marketplace', '0002_default_categories')]
    operations = [migrations.RunPython(seed_products, remove_products)]
