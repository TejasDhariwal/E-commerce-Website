from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .seller_id_gen import generate_unique_number

# Create your views here.

# GLOBAL VARIABLES OF OUR T-MART WEBSITE.

# user variables
user_login_successful = False

are_orders_placed = False

user_profile_saved = False
userPancardNo = ""
userPancardImgUrl = ""
userEmailAddress = ""

# seller variables
seller_login_successful = False
seller_profile_saved = False
sellerEmailAddress = ""
seller_id = 0

tmart_address = "T-Mart, Ajmer, Rajasthan"

def home(request):
    """ View function for home page of our website. """

    # List of all the products as per the category
    
    allProds = [] # list of all the products
    cat_prods = Product.objects.values('product_category', 'id')

    cats = {item['product_category'] for item in cat_prods} # -> categories of the products.

    for cat in cats:
        products = Product.objects.filter(product_category=cat)
        allProds.append(products) # -> list of all the products as per the category


    # List of all the categories of the products.
    product_categories = ProductCategory.objects.all()
    global user_login_successful, seller_login_successful

    dict = {
        'allProds': allProds,
        'product_categories':product_categories,
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful,
    }

    return render(request, '02_home.html', dict)


# user / seller login
def sellerIntro(request):
    """ Intro to how and why to become a t-mart seller. """
    global user_login_successful, seller_login_successful
    
    context = {
        'seller_login_successful':seller_login_successful,
        'user_login_successful':user_login_successful
    }
    return render(request, "login/03_seller_intro.html", context)

def sellerLogin(request):
    """ View function for the seller login page. """

    global user_login_successful, seller_login_successful

    context = {
        'seller_login_successful':seller_login_successful,
        'user_login_successful':user_login_successful
    }

    return render(request, "login/02_sellerLogin.html", context)

def sellerLoginSubmit(request):
    """ will submit the seller's info and will register the user as a seller on t-mart """
    global seller_login_successful, sellerEmailAddress, user_login_successful

    # fetching the user info
    seller_name = request.POST.get('seller-name', '')
    seller_email = request.POST.get('seller-email', '')
    seller_password = request.POST.get('seller-password', '')

    # checking if the seller has already logged in or not
    if SellerLogin.objects.filter(seller_email=seller_email).exists():
        messages.success(request, "you have already logged in.")
        seller_login_successful = True
        sellerEmailAddress = seller_email
        return redirect('home') # -> telling the seller that he has already logged in and redirecting him/her to the home page.

    # if the seller has not logged in yet, then we will create a new t-mart id.
    else:
        newSeller = SellerLogin(seller_email=seller_email, seller_name=seller_name, seller_password=seller_password)
        newSeller.save() # -> saving the info in the database.

        seller_login_successful = True
        sellerEmailAddress = seller_email

        messages.success(request, 'Kindly fill out the following details to complete your T-Mart profile.') # -> giving message to the user.

        context = {
            'seller_login_successful':seller_login_successful,
            'user_login_successful':user_login_successful
        }
        
        return render(request, '09_seller_account.html',
        context) # -> redirecting to the make user profile page. 

def sellerAccount(request):
    """ view func to direct the seller to his / her seller account. """

    global user_login_successful, seller_login_successful, seller_profile_saved, sellerEmailAddress


    if seller_profile_saved:   
        seller = SellerProfile.objects.filter(seller_email = sellerEmailAddress).first()
        context = {
            'user_login_successful':user_login_successful,
            'seller_login_successful':seller_login_successful,
            'seller_profile_saved':seller_profile_saved,
            'seller':seller
        }
        return render(request, "09_seller_account.html", context)
    else:
        context = {
            'user_login_successful':user_login_successful,
            'seller_login_successful':seller_login_successful,
            'seller_profile_saved':seller_profile_saved,
        }
        return render(request, "09_seller_account.html", context)
    
def saveSellerProfile(request):
    """ this view function will save the info of seller to create his/her profile. """

    global seller_profile_saved, sellerEmailAddress, seller_id

    # fetching the seller info

    # personal info
    name = request.POST.get("name-input", "")
    add = request.POST.get("seller-add-input", "")
    email = request.POST.get("email-input", "")
    mob = request.POST.get("mob-input", "")

    # business info
    buss_name = request.POST.get("business-name-input", "")
    bus_reg_no = request.POST.get("bus-reg-no-input", "")
    gst_no = request.POST.get("gst-no-input", "")
    buss_add = request.POST.get("bus-add-input", "")

    # payment info
    bank_name = request.POST.get("bank-name-input", "")
    acc_no = request.POST.get("acc-no-input", "")

    # shipping info
    ship_mode = request.POST.get("ship-mode-input", "")
    ship_rate = request.POST.get("ship-rate-input", "")

    # checking if the seller has already made his/her profile or not.
    if SellerProfile.objects.filter(seller_email = email).exists():
        
        # updating profile if already made.
        old_seller = SellerProfile.objects.filter(seller_email = email).first()

        old_seller.seller_name = name
        old_seller.seller_email = email
        old_seller.seller_mob = mob
        old_seller.add = add
        
        old_seller.business_name = buss_name
        old_seller.business_regis_no = bus_reg_no
        old_seller.gst_no = gst_no
        old_seller.business_add = buss_add

        old_seller.bank_name = bank_name
        old_seller.account_no = acc_no

        old_seller.ship_mode = ship_mode
        old_seller.ship_rate = ship_rate


        old_seller.save() # updating the database.
        seller_id = old_seller.seller_id

        messages.success(request, "Your T-mart profile is updated.")

    else:
        # saving profile if seller is new.
        sel_id = generate_unique_number() # unique seller id for t-mart account
        seller_id = sel_id

        new_seller = SellerProfile(
            seller_name = name,
            seller_email = email,
            seller_mob = mob,
            home_add = add,
            
            business_name = buss_name,
            business_regis_no = bus_reg_no,
            gst_no = gst_no,
            business_add = buss_add,

            bank_name = bank_name,
            account_no = acc_no,

            ship_mode = ship_mode,
            ship_rate = ship_rate,

            seller_id = sel_id
        )


        new_seller.save()
        messages.success(request, "Your T-mart profile is created.")

    sellerEmailAddress = email
    seller_profile_saved = True
    return redirect('sellerAccount') # redirecting seller to saved profile page.

def sellerProducts(request):
    """ view function to allow seller add products to website and see the growth. """
    global user_login_successful, seller_login_successful, seller_id

    # fetching all the products published by a particular user.
    seller_products = Product.objects.filter(seller_id = seller_id)


    context = {
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful,
        'seller_products':seller_products
    }

    return render(request, "10_sellerProducts.html", context)

def seller_progress_Details(request, id):
    """ Will show the progress made by the seller in selling any of the product. """

    # fetching the product
    product = Product.objects.filter(id=id).first()
    
    global user_login_successful, seller_login_successful, seller_profile_saved
    
    earnings = int(product.product_purchases) * int(product.product_price)

    context={
        'product':product,
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful,
        'seller_profile_saved':seller_profile_saved,
        'earnings':earnings
    }

    return render(request, '11_sellerProgressDetail.html', context)

def addNewProduct(request):
    # this view function will allow the seller to add new products to the website.

    # fetching the info
    global seller_id

    if request.method == "POST":

        category = request.POST.get('cats', '')
        name = request.POST.get('name', '')
        desc = request.POST.get('desc', '')
        price = request.POST.get('price', '')
        delivery = request.POST.get('del', '')
        delPrice = request.POST.get('delPrice', '')

        if 'img' in request.FILES:
            uploadedImage = request.FILES['img']


    from datetime import date

    # adding the product to the database
    newProduct = Product(
        product_category = category,
        product_name = name,
        product_image = uploadedImage,
        product_desc = desc,
        product_pub_date = date.today(),
        product_price = price,
        product_delivery = delivery,
        product_delivery_price = delPrice,
        seller_id = seller_id
    )
    newProduct.save()

    messages.success(request, "Your product is added successfully.")
    return redirect("sellerProducts")



def userLogin(request):
    # This view function will let the user register him/her self on the website.
    global user_login_successful, seller_login_successful

    context = {
        'seller_login_successful':seller_login_successful,
        'user_login_successful':user_login_successful
    }

    return render(request, 'login/01_userLogin.html', 
    context)

def userLoginSubmit(request):
    """ View function for user login info submition. """

    # fetching the user information from the website.
    global user_login_successful, seller_login_successful
    global userEmailAddress
    user_email = request.POST.get('user-email', 'default')
    user_name = request.POST.get('user-name', 'default')
    user_password = request.POST.get('user-password', 'default')

    # checking if the user has already logged in or not
    if UserLogin.objects.filter(user_email=user_email).exists():
        messages.success(request, "you have already logged in.")
        user_login_successful = True
        userEmailAddress = user_email
        return redirect('home') # -> telling the user that he has already logged in and redirecting him/her to the home page.

    # if the user has not logged in yet, then we will create a new t-mart id.
    else:
        newUser = UserLogin(user_email=user_email, user_name=user_name, user_password=user_password)
        newUser.save() # -> saving the info in the database.

        user_login_successful = True
        userEmailAddress = user_email

        messages.success(request, 'Kindly fill out the following details to complete your T-Mart profile.') # -> giving message to the user.

        context = {
            'seller_login_successful':seller_login_successful,
            'user_login_successful':user_login_successful
        }
        
        return render(request, '00_my_account.html',
        context) # -> redirecting to the make user profile page.    

def createUserProfile(request):
    """ View function to let the user create his/her t-mart profile. """
    global user_login_successful, seller_login_successful

    context = {
        'seller_login_successful':seller_login_successful,
        'user_login_successful':user_login_successful
    }

    return render(request, '00_my_account.html', context)

def saveUserProfile(request):
    """ View function for saving the user profile info. """

    # fetching the user profile information

    global user_profile_saved, userPancardNo, userPancardImgUrl
    global user_login_successful, seller_login_successful

    # USER'S PERSONAL INFO 
    userName = request.POST.get('name-input', '')
    userGender = request.POST.get('gender-input', '')
    userEmail = request.POST.get('email-input', '')
    userMob = request.POST.get('mob-input', '')

    # USER'S DELIVERY ADDRESS
    useradd = request.POST.get('delivery-input', '')
    
    # PANCARD INFO 
    userPanNo = request.POST.get('pancard-no-input', '')
    if userPanNo == '':
        userPanNo = userPancardNo
    userPanImg = request.POST.get('pancard-img-input', '')

    # PAYMENT METHOD
    userPaymentMethod = request.POST.get('payment-mode-input', '')

    # saving the user information in the database.

    if UserProfile.objects.filter(pan_no=userPanNo).exists():
        # if the user has already made his profile then we will just update it. 
        alreadyCreatedUser = UserProfile.objects.filter(pan_no=userPanNo).first()
        
        alreadyCreatedUser.user_name = userName
        alreadyCreatedUser.user_gender = userGender
        alreadyCreatedUser.user_email = userEmail
        alreadyCreatedUser.user_mob = userMob
        alreadyCreatedUser.user_add = useradd
        alreadyCreatedUser.pan_no = userPanNo
        alreadyCreatedUser.payment_method = userPaymentMethod
        
        # if the user hasn't given pancard's image so we will do nothing
        if userPanImg == '':
            alreadyCreatedUser.pan_img = userPancardImgUrl

        # else we will update the image
        else:
            alreadyCreatedUser.pan_img = userPanImg
            userPancardImgUrl = userPanImg

        alreadyCreatedUser.save() # -> saving profile info in database.

        userPancardNo = userPanNo
        userPancardImgUrl = userPanImg

        # giving message to the user that his / her profile is saved.
        messages.success(request, 'Your profile is being updated.')

    else:
        # if the user has not yet created the profile, then we will make a new profile in the database.
        newUserProfile = UserProfile(
            user_name=userName,
            user_gender=userGender,
            user_email=userEmail,
            user_mob=userMob,
            user_add=useradd,
            pan_no=userPanNo,
            pan_img=userPanImg,
            payment_method=userPaymentMethod
        ) 
        newUserProfile.save() # -> saving the user profile info in the database.

        # updating the global variables
        userPancardNo = userPanNo
        userPancardImgUrl = userPanImg

        # giving message to the user that his / her profile is created.
        messages.success(request, 'Your profile is being created.')
    
    # updating the global variables
    user_login_successful = True
    user_profile_saved = True

    return redirect('myaccount') # -> redirecting to the myaccount page.

def myaccount(request):
    """ View function for myaccount page. """

    global user_login_successful, seller_login_successful
    global user_profile_saved, userPancardNo

    if user_profile_saved:
        # if the user has already made his / her profile then we will show the profile information and edit button

        user = UserProfile.objects.filter(pan_no=userPancardNo).first()

        context = {
            'seller_login_successful':seller_login_successful,
            'user_login_successful':user_login_successful,
            'user':user,
            'user_profile_saved':user_login_successful
        }
        
        return render(request, '00_my_account.html', context)

    else:
        # else we will show the general account page where the user can make his/her profile.
        return render(request, '00_my_account.html', {'user_login_successful':user_login_successful, 'user_profile_saved':user_profile_saved})


#  user / seller logout
def userLogout(request):
    """ This view function will remove the user from the database of the website. """
    
    #  fetching the object from the database with the help of the user email.
    global user_profile_saved, userPancardImgUrl, userPancardNo, userEmailAddress, seller_login_successful

    user_logging_out = UserLogin.objects.filter(user_email=userEmailAddress)
    user_logging_out_profile = UserProfile.objects.filter(pan_no=userPancardNo)
    
    # deleting the data from database
    user_logging_out.delete() 
    user_logging_out_profile.delete() 
    UserOrder.objects.all().delete()
    UserCart.objects.all().delete()

    userPancardImgUrl = ""
    userPancardNo = ""

    # giving message to the user.
    global user_login_successful
    user_login_successful = False
    messages.success(request, 'You have logged out of T-Mart.')

    context = {
        'seller_login_successful':seller_login_successful,
        'user_login_successful':user_login_successful
    }

    return render(request, '02_home.html', context) # -> redirecting to the home page.

def sellerLogout(request):
    """ will allow the seller to logout of the T-mart webiste. """

    # fetching the info

    global user_login_successful, seller_login_successful, seller_profile_saved, sellerEmailAddress

    seller = SellerLogin.objects.filter(seller_email = sellerEmailAddress)
    sellerProfile = SellerProfile.objects.filter(seller_email = sellerEmailAddress)

    # deleting all the seller info from the database
    seller.delete()
    sellerProfile.delete()

    seller_login_successful = False
    seller_profile_saved = False
    sellerEmailAddress = ""

    # giving message to the seller
    context = {
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful
    }

    messages.success(request, "You have successfully logged out of T-Mart.")
    return render(request, "02_home.html", context)


# product info
def category_Products(request, product_category):
    """ View function for displaying all the products of a particular category. """

    # fetching the products of the user's desired category
    global user_login_successful
    products = Product.objects.filter(product_category=product_category)
    context = {
        'products':products, 'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful
    }

    # displaying a message if the products do not exist
    if not products.exists():
        messages.success(request, 'We are extremely sorry ! No Products are available in this category.')
        return redirect('home') # -> redirectin to home page

    # displaying the products if they exist
    else: 
        return render(request, '05_category_Products.html', context)

def product_Details(request, id):
    """ View function for displaying a particular product with all the details. """

    # fetching the product
    product = Product.objects.filter(id=id).first()

    global user_login_successful, seller_login_successful
    context={
        'product':product,
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful,
    }

    return render(request, '06_product_Details.html', context)


# cart
def add_to_cart(request, product_name, product_desc):
    """ View function for adding a product in the cart. """

    # fetching the product.
    product_to_add_in_cart = Product.objects.get(product_name = product_name, product_desc = product_desc)

    # if the product is already present in the cart.
    if UserCart.objects.filter(product_name=product_to_add_in_cart.product_name, product_desc=product_to_add_in_cart.product_desc).exists():
        messages.success(request, 'You have already added the product in the cart.')
        return redirect('home') # -> give message and redirect to home page.

    # if the product doesn't exists then we will add it in cart.         
    else:
        product = UserCart(
            product_name = product_to_add_in_cart.product_name,
            product_image = product_to_add_in_cart.product_image,
            product_desc = product_to_add_in_cart.product_desc,
            product_pub_date = product_to_add_in_cart.product_pub_date,
            product_price = product_to_add_in_cart.product_price,
            product_delivery = product_to_add_in_cart.product_delivery,
            product_delivery_price = product_to_add_in_cart.product_delivery_price,
            product_category = product_to_add_in_cart.product_category,
            
            )
        product.save() # -> saving the info in the database.

        # displaying the updated cart.
        products = UserCart.objects.all()
        global user_login_successful, seller_login_successful

        context = {
            'products': products, 'seller_login_successful':seller_login_successful,'user_login_successful':user_login_successful, 'no_products':False
        }

        return render(request, '03_cart.html', context)
        
def cart(request):
    """ View function for displaying the user cart. """

    # fetching all the products in the cart
    products = UserCart.objects.all()
    global user_login_successful, seller_login_successful

    # if there are no products in the cart
    if len(products) == 0:
        context = {
            'products': products, 'user_login_successful':user_login_successful, 'no_products':True,
            'seller_login_successful': seller_login_successful
        }

    # if there are products in the cart
    else:
        context = {'products': products, 'user_login_successful':user_login_successful, 'no_products':False, 'seller_login_successful':seller_login_successful, 'seller_profile_saved':seller_profile_saved}
    return render(request, '03_cart.html', context)

def remove_Product(request, id):
    """ View function for removing the product from the cart. """

    # fetching the product
    product_to_be_removed = UserCart.objects.filter(id=id)
    product_to_be_removed.delete() # -> removing from the cart

    # displaying the updated cart
    products = UserCart.objects.all()
    global user_login_successful, seller_login_successful

    context = {
        'products': products, 'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful
    }
    return render(request, '03_cart.html', context)

def cart_product_detail(request, id):
    """ View function for showing complete info of a particular product. """

    # fetching the product
    product = UserCart.objects.filter(id=id).first()

    global user_login_successful, seller_login_successful
    context={
        'product':product,
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful
    }

    # sending the data to the template
    return render(request, '04_cart_product_details.html', context)


# product purchase
def purchase(request, product_desc, text):
    """ View function for purchasing a product. """

    global user_login_successful, tmart_address, userPancardNo, user_profile_saved, seller_login_successful

    # fetching the product 
    if text=="cart":
        product = UserCart.objects.filter(product_desc = product_desc).first() # -> from the cart
    else:
        product = Product.objects.filter(product_desc = product_desc).first() # -> directly from database

    # fetching the user info 
    userProfile = UserProfile.objects.filter(pan_no=userPancardNo).first()

    net_product_amount = int(product.product_price)+int(product.product_delivery_price)+10
    
    context = {
        'product': product,
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful,
        'tmart_address':tmart_address,
        'user':userProfile,
        'net_product_amount':net_product_amount,
        'has_user_logged_in_made_profile':True if(user_login_successful and user_profile_saved) else False
    }

    return render(request, '07_purchase.html', context)

def purchase_product(request, product_desc):
    """ View function for final transaction of product. """

    global are_orders_placed, user_login_successful, seller_login_successful

    # fetching the info
    product = Product.objects.filter(product_desc=product_desc).first()
    product_delivery_Add = request.POST.get('user-add-input', '')
    product_qn = int(request.POST.get('prod-quantity', '1'))

    net_product_amount = (product.product_price * product_qn) + product.product_delivery_price + 10

    new_order = UserOrder(
        product_name = product.product_name,
        product_img = product.product_image.url,
        product_quantity = int(product_qn),
        product_gross_price = net_product_amount,
        product_delivered_address = product_delivery_Add
    )
    new_order.save()
    are_orders_placed = True

    # allowing the user to rate the product
    context = {
        'seller_login_successful':seller_login_successful,
        'user_login_successful':user_login_successful,
        'product':product
    }
    messages.success(request, "Your order is placed successfully. You will get the order soon.")

    return render(request, "12_rate_prod.html", context)

# rate product
def product_rating(request, product_desc):
    # this function will take the user product rating as input and store it in the database.
    n = None
    rating = []

    # fetching the info

    if request.method == "POST":
        rating = [
            request.POST.get('rating1'),
            request.POST.get('rating2'),
            request.POST.get('rating3'),
            request.POST.get('rating4'),
            request.POST.get('rating5')
        ]
        new_rate = max([int(n) for n in rating if n is not None])

        # updating the rating of the product.
        product = Product.objects.filter(product_desc = product_desc).first()
        product.product_rating = new_rate
        product.product_purchases += 1
        product.save()

    messages.success(request, "Thanks for your support.")
    return redirect('home')

# orders' history
def myorders(request):
    """ View function for displaying history of all the products purchased by user. """
    global are_orders_placed, user_login_successful, user_profile_saved, seller_login_successful

    all_orders = UserOrder.objects.all() # -> all the orders
    orders_delivered = UserOrder.objects.filter(is_order_delivered = True) # -> orders that are delivered
    orders_not_delivered = UserOrder.objects.filter(is_order_delivered = False) # -> orders that aren't delivered
    orders_returned = UserOrder.objects.filter(is_order_returned = True) # -> orders that are returned
    
    context = {
        'all_orders':all_orders,
        'orders_delivered':orders_delivered,
        'orders_not_delivered':orders_not_delivered,
        'orders_returned':orders_returned,
        'are_orders_placed':are_orders_placed, 'user_login_successful':user_login_successful, 'user_profile_saved':user_profile_saved,
        'seller_login_successful':seller_login_successful
    }

    return render(request, '08_myorders.html', context)

def removeSellerProduct(request, product_desc):
    """ will allow the seller to remove his/her product from the webiste. """

    global user_login_successful, seller_login_successful, seller_id

    product = Product.objects.filter(product_desc = product_desc)
    product.delete()

    # fetching all the left out products.
    seller_products = Product.objects.filter(seller_id = seller_id)

    context = {
        'user_login_successful':user_login_successful,
        'seller_login_successful':seller_login_successful,
        'seller_products':seller_products
    }


    messages.success(request, "The product is removed successfully.")
    return render(request, "10_sellerProducts.html", context)