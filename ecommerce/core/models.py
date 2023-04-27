from django.db import models
from django.contrib.auth.models import User
from core.views import *
from core.forms import *




# Create your models here.




class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price  
    
    def get_final_price(self):
        return self.get_total_item_price()

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItems)
    start_date=models.DateField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    order_id =models.CharField(max_length=100,unique=True,default=None,
    blank=True,null=True
    )
    datetime_ofpayment=models.DateTimeField(auto_now_add=True)
    order_delivered =models.BooleanField(default=False)
    order_received =models.BooleanField(default=False)

    razorpay_order_id=models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=500,null=True,blank=True)
    razorpay_signatur=models.CharField(max_length=500,null=True,blank=True)




def save(self,*args, **kwargs):
    if self.order_id is none and self.datetime_ofpayment and self.id:
        self.order_id = self.datetime_ofpayment.strftime('PAY2ME')+str(self.id)
        

    return super().save(*args,**kwargs)

def __str__(self):
    return self.user.usernamr


def get_total_price(self):
    total=0
    for order_items in self.items.all():
        total += order_item.get_final_price
    return total

def get_total_count(self):
    order= Order.object.get(pk=self.pk)
    return order.items.count

     

         
    
