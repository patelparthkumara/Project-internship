from django.shortcuts import render
from core.forms import  ProductForm
from django.contrib import messages
from core.models import *
from django.utils import timezone

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, "core/index.html", {"products": products})

def orderlist(request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, "core/orderlist.html", {"order": order})
    return render(request, "core/orderlist.html", {"message": "Your Cart is Empty"})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("True")
            form.save()
            print("Data Saved Successfully")
            messages.success(request, "Product Added Successfully")
            return redirect("/")
        else:
            print("Not Working")
            messages.info("Product is not Added, Try Again")
    else:
        form =ProductForm(),
    return render(request, "core/add_product.html", {"form": form})

def product_desc(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "core/product_desc.html", {"product": product})

def add_to_cart(request, pk):
    # Get that Partiuclar Product of id = pk
    product = Product.objects.get(pk=pk)

    # Create Order item
    order_item, created =OrderItems.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"Added Quantity item")
            return redirect("product_desc",pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("product_desc",pk=pk)

    else:
        ordered_date= timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"items added to cart")
        return redirect("product_desc",pk=pk)




class  Customer(models.Model):
    User=models.OneToOneField(User,null=False,blank=False, on_delete=models.CASCADE)
    phone_field=models.CharField(max_length=12,blank=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    Category_name=models.CharField(max_length=200)
    def __str__(self):
        return self.Category_name

class Product(models.Model):
    name = models.CharField(max_length=100)
    Category=models.ForeignKey('Category', on_delete=models.CASCADE)
    desc=models.TextField()
    price=models.FloatField(default=0.0)
    product_available_count=models.IntegerField(default=0)
    img=models.ImageField(upload_to='images/')

    def get_add_to_cart_url(self):
        return reversed("core:add-to-cart",kwargs={
            "pk":self.pk
        })
    def __str__(self):
        return self.name