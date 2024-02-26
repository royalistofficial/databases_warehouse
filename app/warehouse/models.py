from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

    RAW_MATERIAL = 'raw_material'
    SEMI_FINISHED_PRODUCTS = 'semi_finished_products'
    FINISHED_PRODUCTS = 'finished_products'
    CATEGORY_CHOICES = [
        (RAW_MATERIAL, 'Сырье'),
        (SEMI_FINISHED_PRODUCTS, 'Полуфабрикаты'),
        (FINISHED_PRODUCTS, 'Готовая продукция'),
    ]

    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    cost_price = models.FloatField(null=True)
    selling_price = models.FloatField(null=True)
    expiry_date = models.TimeField()
    objects = models.Manager()   

    class Meta:
        db_table = 'product'
