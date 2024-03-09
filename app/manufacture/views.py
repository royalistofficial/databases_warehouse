from tokenize import Name
from django.shortcuts import render
from .models import  Recipe, RecipeProducts, Product
from django import forms

def index(request):
    recipes = Recipe.objects.all()
    prints_recipes = []
    for recipe in recipes:
        print_arr = [recipe.Name,[]]
        recipeProducts = [RecipeProducts.objects.get(recipe_id=int(recipe.recipe_id))]
        for recipeProduct in recipeProducts:
            product = Product.objects.get(product_id=int(recipeProduct.product_id))
            print_arr[1] += f"{product.Name}   количество: {recipeProduct.quantity} \n"
        print_arr[1] = ''.join(print_arr[1])
        print_arr[1] = type(recipe.Name)(print_arr[1])
        prints_recipes.append(print_arr)

    return render(request, 'manufacture/index.html',{'prints_recipes': prints_recipes,})

class RecipeSlot(forms.Form):
    def __init__(self, products, *args, **kwargs):
        super(RecipeSlot, self).__init__(*args, **kwargs)
        choices = [(str(product['id']), product['name']) for product in products]
        self.fields['product_id'] = forms.ChoiceField(choices=choices)
        self.fields['quantity'] = forms.IntegerField()

print_add_recip_tables = []
def add_recip(request):
    form = RecipeSlot( [{'id': product.product_id, 'name': product.Name} for product in Product.objects.all()])
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "add":
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            if not any(item['product_id'] == product_id for item in print_add_recip_tables):
                print_add_recip_tables.append({
                    'name': Product.objects.get(product_id=product_id).Name,
                    'quantity': abs(int(quantity)),
                    'product_id': product_id
                })
            return render(request, 'manufacture/add_recip.html', {'form': form, 'print_add_recip_tables':print_add_recip_tables, 'products_names':  Product.objects.values('Name', 'product_id')})
        elif action == "send":

            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            if not any(item['product_id'] == product_id for item in print_add_recip_tables):
                print_add_recip_tables.append({
                    'name': Product.objects.get(product_id=product_id).Name,
                    'quantity': abs(int(quantity)),
                    'product_id': product_id
                })

            name = request.POST.get('Name')
            name_id = request.POST.get('finish_product')
            new_recipe = Recipe(Name= name, finish_product_id = name_id)
            new_recipe.full_clean()
            new_recipe.save()
            for recipeProduct in print_add_recip_tables:
                new_recipeProduct = RecipeProducts(recipe_id = new_recipe.recipe_id, 
                                                   product_id=recipeProduct['product_id'], 
                                                   quantity=recipeProduct['quantity'])
                new_recipeProduct.full_clean()
                new_recipeProduct.save()
            return render(request, 'main/success.html') 
        elif int(action):
            i = 0
            while i < len(print_add_recip_tables):
                if print_add_recip_tables[i]['product_id'] == action:
                    print_add_recip_tables.pop(i)
                else:
                    i += 1
            return render(request, 'manufacture/add_recip.html', {'form': form, 'print_add_recip_tables':print_add_recip_tables, 'products_names':  Product.objects.values('Name', 'product_id')})
    else:
        pass

    return render(request, 'manufacture/add_recip.html', {'form': form, 'products_names':  Product.objects.values('Name', 'product_id')})

