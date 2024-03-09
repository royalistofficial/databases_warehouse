from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Product, Warehouse, WarehouseProducts


def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(product_id=int(product_id))
            product.delete()
        except Exception as e:
            return HttpResponse(f'Произошла ошибка: {e} ', status=404)


    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    warehouseProducts =  WarehouseProducts.objects.all()
    expiration_date = {}
    for WarPro in warehouseProducts:
        related_product = products.filter(product_id=WarPro.product_id).first()
        
        if related_product:
            expiration_date[WarPro.warehouseproducts_id] = WarPro.production_date + related_product.expiry_date
        else:
            expiration_date[WarPro.warehouseproducts_id] = None

    updated_warehouses = []
    updated_warehouse_products = []
    for warehouse in warehouses:
        updated_warehous = [warehouse.category, warehouse.max_warehouse_capacity, warehouse.max_warehouse_capacity]
        for warehouseProduct in warehouseProducts:
            product = Product.objects.get(product_id=int(warehouseProduct.product_id))
            if product.category == warehouse.category:
                updated_warehous[2] -= warehouseProduct.quantity

        updated_warehouses.append(updated_warehous)
    for warehouseProduct in warehouseProducts:
        product = Product.objects.get(product_id=int(warehouseProduct.product_id))
        updated_warehouse_product = [product.Name,warehouseProduct.quantity,warehouseProduct.production_date,warehouseProduct.production_date + product.expiry_date]
        updated_warehouse_products.append(updated_warehouse_product)


    outputDictionary = {}
    outputDictionary['products'] = products
    outputDictionary['warehouse'] = updated_warehouses
    outputDictionary['warehouseProducts'] = updated_warehouse_products
    return render(request, 'warehouse/index.html', outputDictionary)

def add_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('Name')
            category = request.POST.get('productcategory')
            cost_price = float(request.POST.get('cost_price'))
            selling_price = float(request.POST.get('selling_price'))
            expiry_time = request.POST.get('expiry_time')+ ' days'
            new_product = Product(Name=name, category=category, cost_price=cost_price, selling_price=selling_price, expiry_date=expiry_time)
            product = Product.objects.filter(Name=name).first()
            if product:
                return render(request, 'warehouse/add_product.html', {'error_message': "Продукт с таким именем уже существует"})
            new_product.full_clean()
            new_product.save()
            return  render(request, 'main/success.html')
        except Exception as e:
            render(request, 'warehouse/add_product.html', {'error_message': e})
        return render(request, 'warehouse/add_product.html')   
    else:
        return render(request, 'warehouse/add_product.html')
