from django.shortcuts import render
from .models import  Recipe, RecipeProducts, Product


def index(request):
    products = Product.objects.all()
    recipeProducts = RecipeProducts.objects.all()
    recipes = Recipe.objects.all()
    prints_recipes = []
    for recipe in recipes:
        print_arr = [[],[]]
        print_arr[0] = str(recipe.Name)
        for recipeProduct in recipeProducts:
            if recipeProduct.recipe_id == recipe.recipe_id:
                for product in products:
                    if product.product_id == recipeProduct.product_id:
                        print_arr[1] += f"{product.Name}   количество: {recipeProduct.quantity} \n"
        print_arr[1] = ''.join(print_arr[1])
        print_arr[1] = type(recipe.Name)(print_arr[1])
        prints_recipes.append(print_arr)

    return render(request, 'manufacture/index.html',{'prints_recipes': prints_recipes,})