from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Inventory(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)  # Add this line to associate with the User model
    name = models.CharField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=9, decimal_places=2)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    quantity_sold = models.IntegerField(null=False, blank=False)
    sales = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def formatted_last_sales_date(self):
        return self.last_sales_date.strftime('%m/%d/%y')