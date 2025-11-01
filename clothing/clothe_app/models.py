from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="image/")
    description = models.TextField()

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({self.rating} stars)"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sizes")
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.product.name} - {self.size.name} {self.stock}"

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.user.username} - {self.product_size.product.name} ({self.product_size.size.name}) x {self.quantity}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=50,default='not provided' )
    phone = models.IntegerField()
    payment_status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50, choices=(("Razorpay", "Razorpay"),
                                                              ("COD", "Cash on Delivery")))
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_size.product.name} ({self.product_size.size.name}) x {self.quantity}"

class PromoType(models.TextChoices):
    PERCENTAGE = 'percentage', 'Percentage'
    AMOUNT = 'amount','Amount'




class PromoCode(models.Model):
    code = models.CharField(max_length=15)
    description = models.TextField(blank=True,null=True,default=None)
    type = models.CharField(choices=PromoType.choices,max_length=50,default=PromoType.PERCENTAGE)
    value = models.DecimalField(max_digits=10,decimal_places=2)
    expire_date = models.DateTimeField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='user_promocode')
    created_at = models.DateTimeField(auto_now_add=True)
    issue_to = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='issued_promocode')
    redeem_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='redeemed_promocode')
    min_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)