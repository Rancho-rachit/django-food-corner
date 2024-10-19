from django.contrib import admin
from .models import Dish, Tag, Stats, Order

admin.site.register(Dish)
admin.site.register(Tag)
admin.site.register(Stats)
admin.site.register(Order)