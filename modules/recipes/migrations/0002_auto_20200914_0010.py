import csv

from django.conf import settings
from django.db import migrations


def load_foodstuffs(apps, schema_editor):
    """Загружает единицы измерения и ингредиенты в базу из csv-файла."""

    Dimension = apps.get_model('recipes', 'Dimension')
    Foodstuff = apps.get_model('recipes', 'Foodstuff')

    dimensions_names = []
    foodstuff_to_create = []

    initial_data_file = settings.BASE_DIR / 'fixtures' / 'ingredients.csv'
    with open(initial_data_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] in dimensions_names:
                dimension_id = dimensions_names.index(row[1]) + 1
            else:
                dimensions_names.append(row[1])
                dimension_id = len(dimensions_names)

            foodstuff_to_create.append(
                Foodstuff(name=row[0], dimension_id=dimension_id)
            )

    Dimension.objects.bulk_create([
        Dimension(id=dimension_id, name=dimension_name)
        for dimension_id, dimension_name in enumerate(dimensions_names, start=1)
    ])
    Foodstuff.objects.bulk_create(foodstuff_to_create, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_foodstuffs),
    ]
