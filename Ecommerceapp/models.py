from django.db import models

# Create your models here.

# USER DATA MODELS

class UserLogin(models.Model):
    user_name = models.CharField(default="", max_length=1000)
    user_email = models.EmailField(default="", max_length=1000)
    user_password = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.user_name

class UserProfile(models.Model):
    # personal info
    user_name = models.CharField(max_length=1000, default="")
    user_gender = models.CharField(max_length=100, default="")
    user_email = models.EmailField(max_length=1000, default="")
    user_mob = models.CharField(max_length=12, default="")

    # delivery address 
    user_add = models.CharField(max_length=1000, default="")

    # pancard information
    pan_no = models.CharField(max_length=10, default="")
    pan_img = models.ImageField(upload_to="userPancardImg", default="")

    # payment method 
    payment_method = models.CharField(max_length=1000, default="c_o_d")

    def __str__(self):
        return self.user_name

class UserOrder(models.Model):
    product_name = models.CharField(default="", max_length=500) # -> order product stored by its id
    
    product_img = models.ImageField(upload_to="images", default="") # -> image of ordered product
    
    product_quantity = models.IntegerField(default=1) # -> how many products are ordered
    
    product_gross_price = models.IntegerField(default=0) # -> the total price of product paid by the user
    
    product_delivered_address = models.CharField(default="", max_length=500) # -> the delivery address of product
    
    is_order_delivered = models.BooleanField(default=False) # -> is the order delivered or not
    
    is_order_returned = models.BooleanField(default=False) # -> is the order returned or not

    def __str__(self):
        return self.product_name

# SELLER DATA MODELS
class SellerLogin(models.Model):
    seller_name = models.CharField(default = "", max_length = 1000)
    seller_email = models.EmailField(default = "", max_length=1000)
    seller_password = models.CharField(default = "", max_length = 100)

    def __str__(self) -> str:
        return self.seller_name
    
class SellerProfile(models.Model):
    """ model class for the seller profile for t-mart webiste. """

    # personal information
    seller_name = models.CharField(max_length=1000, default="")
    seller_email = models.EmailField(max_length=1000)
    seller_mob = models.CharField(max_length=11, default="")
    home_add = models.CharField(max_length=1000, default="")

    # business information
    business_name = models.CharField(max_length=1000, default="")
    business_regis_no = models.CharField(max_length=1000, default="")
    gst_no = models.CharField(max_length=100, default="")
    business_add = models.CharField(max_length=1000, default="")

    # payment information
    bank_name = models.CharField(max_length=1000, default="")
    account_no = models.CharField(max_length=100, default="")

    # shipping info
    ship_mode = models.CharField(max_length=1000, default="")
    ship_rate = models.IntegerField(default=0)

    seller_id = models.IntegerField(default=0) # unique id of t-mart account for the seller.

    def __str__(self) -> str:
        return self.seller_name
    

# PRODUCT DATA MODELS

class Product(models.Model):
    # Category choices:-
    category_choice = [
        ('Electronics', 'Electronics'),
        ('Food', 'Food'),
        ('Clothing', 'Clothing'),
        ('Fitness', 'Fitness'),
        ('Gardening', 'Gardening'),
        ('Furniture', 'Furniture'),
        ('Decoratives', 'Decoratives'),
        ('Home-Appliances', 'Home-Appliances'),
        ('Foot wear', 'Foot wear'),
        ('Health', 'Health'),
        ('Toys', 'Toys'),
        ('Other', 'Other')
    ]

    delivery_choice = [
        ('Free delivery', 'Free delivery'),
        ('Paid delivery', 'Paid delivery')
    ]

    product_id = models.AutoField # number of the product (sequence-wise)
    
    product_category = models.CharField(
        max_length=50,
        choices=category_choice,
        default='Clothing',    
    ) # category of the product
    
    product_name = models.CharField(max_length=200) # name of the product
    
    product_image = models.ImageField(upload_to="images", default="") # image of the product
    
    product_desc = models.CharField(max_length=3000) # description of the product
    
    product_pub_date = models.DateField() # the date on which the product is being published on our website
    
    product_price = models.IntegerField(default=0) # price of the product
    
    product_delivery = models.CharField(
        max_length=50,
        choices=delivery_choice,
        default="Free delivery"
    ) # delivery info of the product

    product_delivery_price = models.IntegerField(default=0) # price of the delivery of product

    seller_id = models.IntegerField(default=0) # unique T-mart id of the seller.

    # product rating attributes
    product_rating = models.IntegerField(default=3)
    product_purchases = models.IntegerField(default=0)


    def __str__(self):
        return self.product_name

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to="category_images", default="")
    category_id = models.AutoField

    def __str__(self):
        return self.category_name

class UserCart(models.Model):
     # Category choices:-
    category_choice = [
        ('Electronics', 'Electronics'),
        ('Food', 'Food'),
        ('Clothing', 'Clothing'),
        ('Fitness', 'Fitness'),
        ('Gardening', 'Gardening'),
        ('Furniture', 'Furniture'),
        ('Decoratives', 'Decoratives'),
        ('Home-Appliances', 'Home-Appliances'),
        ('Foot wear', 'Foot wear'),
        ('Health', 'Health'),
        ('Toys', 'Toys'),
        ('Other', 'Other')
    ]

    delivery_choice = [
        ('Free delivery', 'Free delivery'),
        ('Paid delivery', 'Paid delivery')
    ]


    product_category = models.CharField(
        max_length=50,
        choices=category_choice,
        default='Clothing',    
    ) # category of the product
    
    product_name = models.CharField(max_length=200) # name of the product
    
    product_image = models.ImageField(upload_to="images", default="") # image of the product
    
    product_desc = models.CharField(max_length=500) # description of the product
    
    product_pub_date = models.DateField() # the date on which the product is being published on our website
    
    product_price = models.IntegerField(default=0) # price of the product
    
    product_delivery = models.CharField(
        max_length=50,
        choices=delivery_choice,
        default="Free delivery"
    ) # delivery info of the product

    product_delivery_price = models.IntegerField(default=0) # price of the delivery of product

    
    # product rating attributes
    product_rating = models.IntegerField(default=3)
    product_purchases = models.IntegerField(default=0)


    def __str__(self):
        return self.product_name