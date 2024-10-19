from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Dish, Stats, Order
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone

def home_view(request):
    dishes = Dish.objects.all().order_by('id')
    stat = Stats.objects.first()
    total_dishes = dishes.count()
    total_users = User.objects.count()

    twenty_four_hours_ago = timezone.now() - timezone.timedelta(days=1)
    todays_sales = Order.objects.filter(created_at__gte=twenty_four_hours_ago)
    todays_revenue = sum(order.amount for order in todays_sales)

    yesterday_start = timezone.now() - timezone.timedelta(days=2)
    yesterday_end = twenty_four_hours_ago
    yesterdays_sales = Order.objects.filter(created_at__gte=yesterday_start, created_at__lt=twenty_four_hours_ago)
    yesterdays_revenue = sum(order.amount for order in yesterdays_sales)

    # Calculate percentage change
    if yesterdays_revenue > 0:
        percentage_change = ((todays_revenue - yesterdays_revenue) / yesterdays_revenue) * 100
    else:
        percentage_change = 0 if todays_revenue == 0 else float('inf') 

    if percentage_change > 0:
        stonks = "↗︎"
    else:
        stonks = "↘︎"

    percentage_change = int(abs(percentage_change)) if percentage_change != float('inf') else "N/A"

    return render(request, 'home.html', {
        'dishes': dishes, 
        'total_dishes': total_dishes, 
        'stat': stat, 
        'total_users': total_users, 
        'todays_revenue': todays_revenue,
        'percentage_change': percentage_change,
        'stonks': stonks,
    })



@csrf_exempt
def buy_dish(request, dish_id):
    if request.method == 'POST':
        dish = get_object_or_404(Dish, id=dish_id)

        if dish.stock > 0:
            dish.stock -= 1
            dish.save()

            stat_object, created = Stats.objects.get_or_create(id=1)  
            stat_object.dishes_served += 1
            stat_object.revenue += dish.price 
            stat_object.save()

            order = Order(amount=dish.price)
            order.save()

            twenty_four_hours_ago = timezone.now() - timezone.timedelta(days=1)
            todays_sales = Order.objects.filter(created_at__gte=twenty_four_hours_ago)
            todays_revenue = sum(order.amount for order in todays_sales)

            yesterday_start = timezone.now() - timezone.timedelta(days=2)
            yesterday_end = twenty_four_hours_ago
            yesterdays_sales = Order.objects.filter(created_at__gte=yesterday_start, created_at__lt=twenty_four_hours_ago)
            yesterdays_revenue = sum(order.amount for order in yesterdays_sales)

            if yesterdays_revenue > 0:
                percentage_change = ((todays_revenue - yesterdays_revenue) / yesterdays_revenue) * 100
            else:
                percentage_change = 0 if todays_revenue == 0 else float('inf') 

            if percentage_change > 0:
                stonks = "↗︎"
            else:
                stonks = "↘︎"

            percentage_change = int(abs(percentage_change)) if percentage_change != float('inf') else "N/A"

        return render(request, 'partials/stat_value.html', {
            'stat': {'revenue': int(stat_object.revenue), 'dishes_served': stat_object.dishes_served},
            'dish': {'id': dish.id, 'stock': dish.stock},
            'todays': {'revenue': int(todays_revenue)},
            'change': {'percentage': percentage_change, 'stonks': stonks},
        }) 

    else:
        return HttpResponse(status=400)