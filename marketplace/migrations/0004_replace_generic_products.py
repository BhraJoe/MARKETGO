from decimal import Decimal
from django.db import migrations
from django.utils.text import slugify


PRODUCTS = {
    'agriculture': ['Pruning Shears', 'Garden Hose', 'Hand Trowel', 'Watering Can', 'Wheelbarrow', 'Farm Boots', 'Hedge Clipper', 'Seedling Tray', 'Organic Compost', 'Fertilizer Spreader', 'Knapsack Sprayer', 'Garden Rake', 'Hoe and Cutlass Set', 'Drip Irrigation Kit', 'Plant Nursery Bags', 'Maize Seeds', 'Tomato Seeds', 'Poultry Feeder', 'Chicken Waterer', 'Harvest Basket'],
    'appliances': ['Samsung 43-inch Smart TV', 'LG Double-Door Refrigerator', 'Nasco Chest Freezer', 'Binatone Standing Fan', 'Philips Blender', 'Moulinex Electric Kettle', 'Russell Hobbs Toaster', 'Ramtons Microwave Oven', 'Scanfrost Gas Cooker', 'Hisense Washing Machine', 'Electric Rice Cooker', 'Black+Decker Iron', 'Kenwood Food Processor', 'Midea Air Conditioner', 'Rechargeable Table Fan', 'Hot Plate Cooker', 'Electric Coffee Maker', 'Water Dispenser', 'Hand Mixer', 'Sandwich Maker'],
    'baby-kids': ['Wooden Baby Cot', 'Baby Stroller', 'Infant Car Seat', 'Baby Carrier', 'Silicone Feeding Set', 'Newborn Gift Set', 'Kids Bicycle', 'Building Blocks Set', 'Remote Control Car', 'Educational Flash Cards', 'Children’s Story Books', 'School Backpack', 'Kids Rain Boots', 'Baby Bath Tub', 'Nursing Pillow', 'Baby Monitor', 'Toddler Tricycle', 'Plush Teddy Bear', 'Kids Drawing Table', 'Reusable Diaper Pack'],
    'beauty-care': ['Shea Body Butter', 'Black Soap', 'Cocoa Butter Lotion', 'Natural Hair Shampoo', 'Conditioning Hair Mask', 'Electric Hair Clipper', 'Hair Dryer', 'Wig Stand', 'Makeup Brush Set', 'Matte Lipstick Set', 'Facial Cleansing Brush', 'Sunscreen SPF 50', 'Aloe Vera Gel', 'Men’s Grooming Kit', 'Perfume Gift Set', 'Nail Care Kit', 'Bath and Body Set', 'Beard Oil', 'Hair Bonnet', 'Roller Skin Care Set'],
    'computers': ['Dell Latitude 5420 Laptop', 'HP EliteBook 840', 'Lenovo ThinkPad T14', 'Apple MacBook Air', 'Acer Aspire 5', '27-inch LED Monitor', 'Wireless Keyboard and Mouse', 'USB-C Docking Station', 'External SSD 1TB', 'Portable Hard Drive', 'Wi-Fi Router', 'Laptop Cooling Stand', 'USB Webcam', 'Laser Printer', 'Laptop Backpack', 'Mechanical Gaming Keyboard', 'Wireless Mouse', 'HDMI Adapter', '8GB DDR4 RAM', 'Laptop Power Charger'],
    'electronics': ['Apple AirPods Pro', 'JBL Bluetooth Speaker', 'Anker Power Bank', 'Samsung Galaxy Watch', 'Sony Noise-Cancelling Headphones', 'Ring Light with Tripod', 'GoPro Action Camera', 'Canon EOS Camera', 'Bluetooth Earbuds', 'USB-C Fast Charger', 'LED Strip Lights', 'Smartphone Gimbal', 'Digital Voice Recorder', 'Kindle Paperwhite', 'Portable Projector', 'HDMI Streaming Stick', 'Rechargeable Emergency Light', 'Wireless Game Controller', 'Smart LED Bulb', 'Multi-Port USB Hub'],
    'fashion': ['Men’s Oxford Shirt', 'Women’s Ankara Dress', 'Cotton Polo Shirt', 'Classic Blue Jeans', 'Leather Belt', 'Men’s Kaftan', 'Women’s Blazer', 'Linen Trousers', 'Hooded Sweatshirt', 'Summer Maxi Dress', 'Ankara Two-Piece Set', 'Denim Jacket', 'Formal Suit', 'Cotton T-Shirt Pack', 'Pleated Skirt', 'Chiffon Blouse', 'Sports Tracksuit', 'Traditional Kente Shirt', 'Cargo Shorts', 'Rain Jacket'],
    'home-furniture': ['Three-Seater Sofa', 'Solid Wood Dining Table', 'Queen Bed Frame', 'Office Study Desk', 'Six-Piece Dining Chair Set', 'TV Console', 'Wooden Bookshelf', 'Bedside Table', 'Fabric Accent Chair', 'Plastic Storage Cabinet', 'Foam Mattress', 'Full-Length Dressing Mirror', 'Kitchen Cabinet', 'Shoe Rack', 'Curtain Set', 'Carpet Runner', 'Laundry Basket', 'Wall-Mounted Shelf', 'Garden Chair Set', 'Coffee Table'],
    'other': ['Rechargeable Torch', 'Travel Suitcase', 'Stainless Steel Flask', 'Reusable Shopping Bags', 'Sewing Machine', 'Umbrella', 'Pocket Calculator', 'Key Storage Box', 'Metal Tool Box', 'Picnic Cooler Box', 'First Aid Kit', 'Water Bottle Pack', 'Extension Cable', 'Folding Ladder', 'Digital Weighing Scale', 'Mosquito Net', 'Bicycle Lock', 'Travel Neck Pillow', 'Storage Trunk', 'Camping Tent'],
    'phones-tablets': ['iPhone 13', 'Samsung Galaxy S22', 'Google Pixel 7', 'Tecno Camon 20', 'Infinix Note 30', 'Xiaomi Redmi Note 12', 'Nokia C32', 'iPad 10th Generation', 'Samsung Galaxy Tab A8', 'Tecno Spark 10', 'iPhone 11', 'OnePlus Nord CE', 'Oppo Reno 8', 'Huawei MatePad', 'Phone Ring Light', 'Tempered Glass Screen Protector', 'Universal Phone Tripod', 'Fast-Charging Power Bank', 'Wireless Phone Charger', 'Phone Protective Case'],
    'sports-fitness': ['Adjustable Dumbbells', 'Yoga Mat', 'Football Boots', 'Professional Football', 'Resistance Bands', 'Skipping Rope', 'Exercise Bike', 'Treadmill', 'Boxing Gloves', 'Basketball', 'Table Tennis Set', 'Camping Backpack', 'Hiking Shoes', 'Swimming Goggles', 'Kettlebell', 'Gym Gloves', 'Sports Water Bottle', 'Pull-Up Bar', 'Cycling Helmet', 'Fitness Tracker'],
    'vehicles': ['Toyota Corolla 2015', 'Honda Civic 2014', 'Toyota RAV4 2017', 'Hyundai Elantra 2016', 'Kia Sportage 2018', 'Nissan X-Trail 2015', 'Mercedes-Benz C200', 'Volkswagen Golf 2013', 'Toyota Hiace Bus', 'Honda CR-V 2016', 'Suzuki Swift 2017', 'Ford Ranger Pickup', 'Kia Picanto 2015', 'Mitsubishi Outlander', 'Toyota Camry 2014', 'Hyundai Tucson 2018', 'Nissan Navara Pickup', 'Mercedes-Benz Sprinter', 'Toyota Yaris 2016', 'Land Rover Discovery'],
}


def replace_products(apps, schema_editor):
    Product = apps.get_model('marketplace', 'Product')
    Category = apps.get_model('marketplace', 'Category')
    seller = apps.get_model('auth', 'User').objects.filter(username='marketgo_demo_seller').first()
    if not seller:
        return

    for category in Category.objects.all():
        names = PRODUCTS.get(category.slug)
        if not names:
            continue
        products = list(Product.objects.filter(category=category, seller=seller).order_by('created_at', 'pk')[:20])
        for index, product in enumerate(products):
            product.name = names[index]
            product.slug = f'{slugify(names[index])}-{category.pk}'
            product.description = f'{names[index]} available from a local {category.name.lower()} seller on MarketGo. Check the listing details and contact the seller before purchase.'
            product.brand = ''
            product.price = Decimal(75 + ((index + 1) * 42) + (category.pk * 9))
            product.save(update_fields=['name', 'slug', 'description', 'brand', 'price'])


def restore_generic_names(apps, schema_editor):
    Product = apps.get_model('marketplace', 'Product')
    for product in Product.objects.filter(seller__username='marketgo_demo_seller'):
        product.name = f'{product.category.name} - MarketGo Product'
        product.slug = f'{slugify(product.name)}-{product.pk}'
        product.save(update_fields=['name', 'slug'])


class Migration(migrations.Migration):
    dependencies = [('marketplace', '0003_seed_twenty_products_per_category')]
    operations = [migrations.RunPython(replace_products, restore_generic_names)]
