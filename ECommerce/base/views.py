from django.shortcuts import render, redirect
from .models import Type, Category, Product, Brand, Review, Wishlist, Cart
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q


def main(request):

    products = Product.objects.all()
    best_selling_products = Product.objects.filter(purchases__gte=10)
    sale_products = Product.objects.filter(discount__gte=10)

    for product in best_selling_products: 
        disc = product.price - ((product.price * product.discount)/100)
        product.final_price = disc

    for product in products: 
        disc = product.price - ((product.price * product.discount)/100)
        product.final_price = disc

    for product in sale_products: 
        disc = product.price - ((product.price * product.discount)/100)
        product.final_price = disc


    wishlist = Wishlist.objects.filter(user=request.user.id)
    wishlist_products = []

    for product in wishlist:
        wishlist_products.append(product.product)

    if request.method == "POST":
        print(request.POST)
    context = {'products': products, 
               'best_selling_products': best_selling_products, 
               'sale_products': sale_products, 
               'wishlist_products': wishlist_products}
    return render(request, 'index.html', context)

def product(request, pk):
    
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    best_selling_products = Product.objects.filter(purchases__gte=10)
    sale_products = Product.objects.filter(discount__gte=10)
    reviews = Review.objects.filter(product__id__icontains=product.id)
    review_count = reviews.count()
    
    
    wishlist = Wishlist.objects.filter(user=request.user.id)
    wishlist_products = []

    cart = Cart.objects.filter(user=request.user.id)
    cart_products = []
    
    for cproduct in cart:
        cart_products.append(cproduct.product)

    for wproduct in wishlist:
        wishlist_products.append(wproduct.product)
    
    
    similar_brand_products = Product.objects.filter(brand__contains=product.brand)
    similar_category_products = Product.objects.filter(category__name__contains=product.category)
    
    if request.method == "POST":
        if request.user:
            review = Review.objects.create(user=request.user, product=product, body=request.POST['product_review'])
        else:
            redirect('login')
        print(request.POST['product_review'], product.id, request.user.id)
        
    discounted_price = product.price - (product.price * (product.discount/100)) 
    
    context = {'product': product,
               'dis_price': discounted_price,
               'products': products, 
               'best_selling_products': best_selling_products, 
               'sale_products': sale_products, 
               'similar_brand_products': similar_brand_products,
               'similar_category_products': similar_category_products,
               'reviews': reviews[:5],
               'reviews_count': review_count,
               'wishlist_products': wishlist_products,
               'cart_products': cart_products,
               }
    
    return render(request, 'product.html', context)



def loginPage(request):
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}
    
    return render(request, 'login.html', context)



def registerPage(request):
    form = MyUserForm()
    
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    
    context = {'form': form}
    
    return render(request, 'register.html', context)



def logoutPage(request):
    logout(request)
    return redirect('home')



def collections(request):

    types = Type.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    wishlist = Wishlist.objects.filter(user=request.user.id)
    wishlist_products = []

    for product in wishlist:
        wishlist_products.append(product.product)


    if request.GET.get('q') != None:
        q = request.GET.get('q')
        products = Product.objects.filter(
        Q(brand__contains=q) | 
        Q(category__name__icontains=q) |
        Q(type__name__icontains=q))

    else:
        q = ""
        products = Product.objects.filter(
        Q(brand__icontains=q) | 
        Q(category__name__icontains=q) |
        Q(type__name__icontains=q))
    
    if request.GET.get('type') != None:
        type = request.GET.get('type')
        products = Product.objects.filter(type__name__contains=type)
    else:
        type = ""
        
    if request.GET.get('category') != None:
        category = request.GET.get('category')
        products = Product.objects.filter(category__name__contains=category)
    
    else:
        category = ""
    
    if request.GET.get('brand') != None:
        brand = request.GET.get('brand')
        products = Product.objects.filter(brand__contains=brand)
    
    else:
        brand = ""
    
    
    product_count = products.count()
    context = {'products': products, 'types': types, 'categories': categories, 'brands': brands, 'product_count': product_count, 'wishlist_products': wishlist_products}
    
    return render(request, 'collections.html', context)


def userProfile(request, pk):
    
    context = {'current_user': request.user}
    return render(request, 'userProfile.html', context)


def wishlist(request):

    page = 'Wishlist'

    full_wishlist = Wishlist.objects.all()
    wishlist = Wishlist.objects.filter(user=request.user.id)
    wishlist_products = []
    wishlist_products_prices = []
    wishlist_count = wishlist.count()

    for product in wishlist:
        price = product.product.price - ((product.product.price * product.product.discount ) / 100)
        product.product.actual_price = price
        wishlist_products.append(product.product)
        price = product.product.price - ((product.product.price * product.product.discount ) / 100)
        



    if request.GET.get('p') is not None:

        product_id = request.GET.get('p')
        operation = request.GET.get('q')
        
        wishlist_product = Product.objects.get(id=product_id)
        
        
        if operation == 'add':
            
            is_present = False    
            for product in full_wishlist:
                if product.user == request.user and product.product == wishlist_product:
                    is_present = True
            
            if is_present:
                pass
                
            else:
                Wishlist.objects.create(user=request.user, product=wishlist_product)
                redirect('home')

            
            
        else:
            Wishlist.objects.filter(user=request.user, product=wishlist_product).delete()
            redirect('home')


    context = {
        'page': page,
        'wishlist_products': wishlist_products, 
        'prices': wishlist_products_prices, 
        'wishlist_count': wishlist_count,
               }

    return render(request, 'wishlist.html', context)


def cart(request):

    page = 'Cart'


    full_wishlist = Cart.objects.all()
    wishlist = Cart.objects.filter(user=request.user.id)
    wishlist_products = []
    wishlist_products_prices = []
    wishlist_count = wishlist.count()
    discounted_total_price = 0
    actual_total_price = 0
    discount_price = 0

    for product in wishlist:
        price = product.product.price - ((product.product.price * product.product.discount ) / 100)
        actual_total_price += product.product.price
        product.product.actual_price = price
        wishlist_products.append(product.product)
        discounted_total_price += price
        
    discount_price = int(actual_total_price - discounted_total_price)


    if request.GET.get('p') is not None:
        product_id = request.GET.get('p')
        operation = request.GET.get('q')
        
        wishlist_product = Product.objects.get(id=product_id)
        
        
        if operation == 'add':
            
            is_present = False    
            for product in full_wishlist:
                if product.user == request.user and product.product == wishlist_product:
                    is_present = True
            
            if is_present:
                pass
                
            else:
                Cart.objects.create(user=request.user, product=wishlist_product)
                redirect('home')

            
            
        else:
            Cart.objects.filter(user=request.user, product=wishlist_product).delete()
            redirect('home')


    context = {
        'discount_price': float(discount_price),
        'total_price': float(discounted_total_price),
        'actual_price': float(actual_total_price),
        'page': page,
        'wishlist_products': wishlist_products, 
        'prices': wishlist_products_prices, 
        'wishlist_count': wishlist_count,
        }

    return render(request, 'wishlist.html', context)


def editProfile(request):
    form = MyUserForm(instance=request.user)
    
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    
    context = {'form': form}
    
    return render(request, 'register.html', context)