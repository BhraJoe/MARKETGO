from django.db import migrations


IMAGE_IDS = {
    'agriculture': ['photo-1416879595882-3373a0480b5b', 'photo-1464226184884-fa280b87c399', 'photo-1592982537447-7440770cbfc9'],
    'appliances': ['photo-1571175443880-49e1d25b2bc5', 'photo-1584622650111-993a426fbf0a', 'photo-1556911220-e15b29be8c8f'],
    'baby-kids': ['photo-1516627145497-ae6968895b74', 'photo-1596461404969-9ae70f2830c1', 'photo-1503919545889-aef636e10ad4'],
    'beauty-care': ['photo-1596462502278-27bfdc403348', 'photo-1522337360788-8b13dee7a37e', 'photo-1556228578-8c89e6adf883'],
    'computers': ['photo-1496181133206-80ce9b88a853', 'photo-1517336714731-489689fd1ca8', 'photo-1525547719571-a2d4ac8945e2'],
    'electronics': ['photo-1498049794561-7780e7231661', 'photo-1505740420928-5e560c06d30e', 'photo-1511707171634-5f897ff02aa9'],
    'fashion': ['photo-1445205170230-053b83016050', 'photo-1490481651871-ab68de25d43d', 'photo-1529139574466-a303027c1d8b'],
    'home-furniture': ['photo-1555041469-a586c61ea9bc', 'photo-1618220179428-22790b461013', 'photo-1616486338812-3dadae4b4ace'],
    'other': ['photo-1586023492125-27b2c045efd7', 'photo-1553062407-98eeb64c6a62', 'photo-1581578731548-c64695cc6952'],
    'phones-tablets': ['photo-1511707171634-5f897ff02aa9', 'photo-1598327105666-5b89351aff97', 'photo-1544244015-0df4b3ffc6b0'],
    'sports-fitness': ['photo-1534438327276-14e5300c3a48', 'photo-1517836357463-d25dfeac3438', 'photo-1579952363873-27f3bade9f55'],
    'vehicles': ['photo-1492144534655-ae79c964c9d7', 'photo-1502877338535-766e1452684a', 'photo-1549317661-bd32c8ce0db2'],
}


def seed_images(apps, schema_editor):
    Product = apps.get_model('marketplace', 'Product')
    Category = apps.get_model('marketplace', 'Category')
    for category in Category.objects.all():
        image_ids = IMAGE_IDS.get(category.slug, ['photo-1523275335684-37898b6baf30'])
        products = Product.objects.filter(category=category).order_by('created_at', 'pk')
        for index, product in enumerate(products):
            product.image_source_url = f'https://images.unsplash.com/{image_ids[index % len(image_ids)]}?auto=format&fit=crop&w=900&q=80'
            product.save(update_fields=['image_source_url'])


def clear_images(apps, schema_editor):
    Product = apps.get_model('marketplace', 'Product')
    Product.objects.all().update(image_source_url='')


class Migration(migrations.Migration):
    dependencies = [('marketplace', '0005_product_image_source_url')]
    operations = [migrations.RunPython(seed_images, clear_images)]
