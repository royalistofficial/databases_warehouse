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
    prints_warehouse = []
    for warehouse in warehouses:
        print_warehouse = [[],[],[]]
        print_warehouse[0] = warehouse.category
        print_warehouse[1] = warehouse.max_warehouse_capacity
        print_warehouse[2] = warehouse.max_warehouse_capacity
        for warehouseProduct in warehouseProducts:
            for product in products:
                if warehouseProduct.product_id == product.product_id:
                    if product.category == warehouse.category:
                        print_warehouse[2] -= warehouseProduct.quantity
        prints_warehouse.append(print_warehouse)
    return render(request, 'warehouse/index.html', 
                    {'products': products, 
                    'warehouse': prints_warehouse, 
                    'warehouseProducts': warehouses,})


def add_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('Name')
            category = request.POST.get('productcategory')
            cost_price = float(request.POST.get('cost_price'))
            selling_price = float(request.POST.get('selling_price'))
            expiry_time = request.POST.get('expiry_time')+ ' days'
            new_product = Product(Name=name, category=category, cost_price=cost_price, selling_price=selling_price, expiry_date=expiry_time)
            new_product.full_clean()
            new_product.save()
            return index(request)
        except Exception as e:
            # Обработка других неожиданных ошибок
            return HttpResponse(f'Произошла ошибка: {e} ')
    else:
        return render(request, 'warehouse/add_product.html')
