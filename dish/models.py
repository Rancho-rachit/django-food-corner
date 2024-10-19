from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    badge = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=7.0)
    stock = models.IntegerField(default=0)  # New stock attribute
    last_modified = models.DateTimeField()

    def __str__(self):
        return self.name

class Stats(models.Model):
    revenue = models.IntegerField(default=0)
    dishes_served = models.IntegerField(default=0)

    def __str__(self):
        return f"Total Revenue: {self.revenue}"

class Order(models.Model):
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Item Cost: {self.amount}"
