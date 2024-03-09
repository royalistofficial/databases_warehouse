from django.db import models
from warehouse.models import Product

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=32, null=True)
    finish_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    objects = models.Manager()
    
    class Meta:
        db_table = 'recipe'
        constraints = [
            models.UniqueConstraint(fields=['finish_product'], name='unique_recipe_product_recipe')
        ]


class RecipeProducts(models.Model):
    recipeproducts_id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    objects = models.Manager()
    class Meta:
        db_table = 'recipe_products'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'product'], name='unique_recipe_product')
        ]