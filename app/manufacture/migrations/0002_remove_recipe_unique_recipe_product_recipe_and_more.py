# Generated by Django 4.2.10 on 2024-03-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacture', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe_product_recipe',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='Name',
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('finish_product',), name='unique_recipe_product_recipe'),
        ),
    ]
