from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Product
from datetime import datetime


def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        try:
            product = Product.objects.get(product_id=int(product_id))
        except Exception as e:
            return HttpResponse(f'Произошла ошибка: {e} ', status=404)

        product.delete()

    products = Product.objects.all()
    return render(request, 'warehouse/index.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('Name')
            category = request.POST.get('productcategory')
            cost_price = float(request.POST.get('cost_price'))
            selling_price = float(request.POST.get('selling_price'))
            expiry_time = request.POST.get('expiry_time')
            expiry_time = datetime.strptime(expiry_time, "%H:%M:%S").time()
            new_product = Product(Name=name, category=category, cost_price=cost_price, selling_price=selling_price, expiry_date=expiry_time)
            new_product.full_clean()
            new_product.save()
            return HttpResponse('Данные успешно получены и обработаны!')
        except Exception as e:
            # Обработка других неожиданных ошибок
            return HttpResponse(f'Произошла ошибка: {e} ')
    else:
        return render(request, 'warehouse/add_product.html')
