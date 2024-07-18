from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password



from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # increased max length to 128 for hashed password
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, default="")
    pincode = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    role = models.CharField(default="customer", max_length=10)
    date = models.DateTimeField('date published', default=timezone.now)
    forgot_password_token = models.CharField(max_length=200, default="")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)

        





   

    
        



    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7},{8}".format(self.customer_id,self.name, self.email,self.password,self.mobile,self.address,self.status,self.role,self.date)

    # def __str__(self):
    #     return self.name


class ProductDetail(models.Model): 
    product_id = models.AutoField(primary_key=True)
    product_brand = models.CharField(max_length=200)
    product_price = models.FloatField(max_length=10)
    product_old_price = models.FloatField(max_length=10)
    product_discount = models.FloatField(max_length=10)
    product_size = models.CharField(max_length=20)
    product_description = models.CharField(max_length=200)
    product_quantity = models.IntegerField(default=1)
    product_availability = models.CharField(max_length=20)

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7},{8}".format(self.product_id,self.product_brand, self.product_price,self.product_old_price,self.product_discount,self.product_size,self.product_description,self.product_quantity,self.product_availability)

class ProductImage(models.Model):
    product_img_id = models.AutoField(primary_key=True)
    product_img = models.CharField(max_length=100)
    product_id = models.ForeignKey(
        ProductDetail,
        related_name='productdetail',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{0}, {1}, {2}, ".format(self.product_img_id,self.product_img, self.product_id)


class AddToCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product_img = models.CharField(max_length=200)
    product_brand = models.CharField(max_length=200)
    product_description = models.CharField(max_length=200)
    product_quantity = models.IntegerField(default=1)
    product_size = models.CharField(max_length=20)
    product_price = models.FloatField(max_length=10)
    product_total_price = models.FloatField(max_length=10)

    product_id = models.ForeignKey(
        ProductDetail,
        related_name='productdetails',
        on_delete=models.CASCADE,
    )

    customer_id = models.ForeignKey(
        Customer,
        related_name='customer',
        on_delete=models.CASCADE,
    )

    product_img_id = models.ForeignKey(
        ProductImage,
        related_name='productimage',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(self.cart_id,self.product_id,self.product_img, self.product_brand,self.product_description,self.product_quantity,self.product_size,self.product_price,self.product_total_price,self.customer_id,self.product_img_id)    
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product_brand = models.CharField(max_length=200)
    product_price = models.FloatField(max_length=10)
    product_size = models.CharField(max_length=20)
    product_description = models.CharField(max_length=200)
    product_quantity = models.IntegerField(default=1)
    product_img = models.CharField(max_length=100)
    
    product_img_id = models.ForeignKey(
        ProductImage,
        related_name='productimageorder',
        on_delete=models.CASCADE,
    )

    product_id = models.ForeignKey(
        ProductDetail,
        related_name='productdetailsorder',
        on_delete=models.CASCADE,
    )

    customer_id = models.ForeignKey(
        Customer,
        related_name='customerorder',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(self.order_id,self.product_brand,self.product_price, self.product_brand,self.product_size,self.product_description,self.product_quantity,self.product_img,self.customer_id,self.product_id,self.product_img_id)  
