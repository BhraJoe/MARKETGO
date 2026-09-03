from django.db import migrations
from django.utils.text import slugify


def seed_categories(apps, schema_editor):
    Category = apps.get_model('marketplace', 'Category')
    for name, icon in [
        ('Electronics', 'TECH'), ('Phones & Tablets', 'PHONE'), ('Computers', 'PC'), ('Fashion', 'WEAR'),
        ('Home & Furniture', 'HOME'), ('Appliances', 'APPL'), ('Vehicles', 'AUTO'), ('Beauty & Care', 'CARE'),
        ('Baby & Kids', 'KIDS'), ('Agriculture', 'FARM'), ('Sports & Fitness', 'PLAY'), ('Other', 'MORE'),
    ]:
        Category.objects.get_or_create(name=name, defaults={'icon': icon, 'slug': slugify(name)})


def remove_categories(apps, schema_editor):
    Category = apps.get_model('marketplace', 'Category')
    Category.objects.filter(name__in=['Electronics', 'Phones & Tablets', 'Computers', 'Fashion', 'Home & Furniture', 'Appliances', 'Vehicles', 'Beauty & Care', 'Baby & Kids', 'Agriculture', 'Sports & Fitness', 'Other']).delete()


class Migration(migrations.Migration):
    dependencies = [('marketplace', '0001_initial')]
    operations = [migrations.RunPython(seed_categories, remove_categories)]
