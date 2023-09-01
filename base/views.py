from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . forms import *
from .models import *

# Create your views here.

# New user registration
class UserRegister(View):
    def get(self,request):
        if self.request.user.is_authenticated:
            return redirect('/')
        form = UserRegistration()
        return render(request,'base/register.html',{'form':form})
    
    def post(self,request):
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,"A new user created!!")
            # a customer will be created with the new user
            Customer.objects.create(user=user,name=user.username)
        return render(request,'base/register.html',{'form':form})
    
    
#login
class UserLoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = UserLogin
    template_name = 'base/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

# Password Change 
class passwordChange(PasswordChangeView):
    template_name = 'base/password_change_form.html'
    form_class = passwordchange
    success_url = reverse_lazy('password-change-done')

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     messages.success(self.request,"Please login using new password.")
    #     return context

class passwordchangedone(PasswordChangeDoneView):
    template_name = 'base/password_change_done.html'  

# profile 
@method_decorator(login_required(login_url='login'),name='dispatch')
class Profile(View):
    def get(self,request):
        eml = request.user.email
        try:
            cus = Customer.objects.get(user=request.user)
            form = UserProfile(initial={'name':cus.name,'email':eml,'phone':cus.phone,'gender':cus.gender})
        except Exception as e:
            print(e)
            form = UserProfile(initial={'email':eml})
        return render(request,'base/profile.html',{'form':form,'active':'new btn-primary','cus':cus})
    
    def post(self,request):
        form = UserProfile(request.POST, request.FILES)
        # to update customer profile
        if Customer.objects.filter(user=request.user).exists():
            cus  = Customer.objects.get(user=request.user)
            if form.is_valid():
                cus.name = form.cleaned_data['name']
                cus.email = form.cleaned_data['email']
                cus.phone = form.cleaned_data['phone']
                cus.gender = form.cleaned_data['gender']
                if request.FILES:
                    cus.profile_pic = request.FILES.get('profile_pic') or ''
                cus.save()
            return redirect('address')
        else:
            # new info add to the customer profile first time
            if form.is_valid():
                # usr = request.user
                # name = form.cleaned_data['name']
                # email = form.cleaned_data['email']
                # phone = form.cleaned_data['phone']
                # gender = form.cleaned_data['gender']

                # info = Customer(user=usr,name=name,email=email,phone=phone,gender=gender)
                # info.save()
                form.save()
                messages.success(request,'Profile Updated Successfully!')
            return render(request,'base/profile.html',{'form':form,'active':'new btn-primary'})

# Address of customer 
@method_decorator(login_required(login_url='login'),name='dispatch') 
class AddressUser(View):
    def get(self,request):
        form = AddressForm()
        try:
            add = Address.objects.all().filter(user=request.user)
            print(len(add))
        except Exception as e:
            print(e)
            print('No address yet')
        return render(request,'base/address.html',{'form':form,'active':'new btn-primary','add':add})
    
    def post(self,request):
        add = Address.objects.all().filter(user=request.user)
        # a customer can add only 2 address at most
        if len(add) != 2:
            form = AddressForm(request.POST)
            if form.is_valid():
                usr = request.user
                division = form.cleaned_data['division']
                district = form.cleaned_data['district']
                thana = form.cleaned_data['thana']
                holding_street_village = form.cleaned_data['holding_street_village']
                zipcode = form.cleaned_data['zipcode']

                info = Address(user=usr,division=division,district=district,thana=thana,holding_street_village=holding_street_village,zipcode=zipcode)
                info.save()
            return redirect('address')
        
        else:
            messages.error(request,"Please delete address first. Max address 2.")
            return redirect('address')

# delete address
@method_decorator(login_required(login_url='login'),name='dispatch')
class DelAddress(View):
    def get(self,request,pk):
        add = Address.objects.get(id=pk)
        return render(request,'base/deleteaddress.html',{'add':add})
    
    def post(self,request,pk):
        add = Address.objects.get(id=pk)
        add.delete()
        return redirect('address')

# home page
def home(request):
    fooditem = FoodItem.objects.filter(special=True)
    breakfirst = FoodItem.objects.filter(category='breakfirst')
    lunch = FoodItem.objects.filter(category='lunch')
    dinner = FoodItem.objects.filter(category='dinner')
    snacks = FoodItem.objects.filter(category='snack')
    exclusive = FoodItem.objects.filter(category='exclusive')
    chefs = Chef.objects.all()
    li = []
    dic = {}
    
    # to find out to sell items based on "Delivered"
    for order in OrderPlaced.objects.all().filter(status='Delivered'):
        li.append(order.fooditem.id)
        dic[order.fooditem.id] = li.count(order.fooditem.id)
    dic_key = list(dic.keys())
    dic_val = list(dic.values())
    sell = []
    # top = list(dic.keys())[list(dic.values()).index(max(dic.values()))]
    for i in range(len(dic_key)):
        if i == 3:
            break
        inx = dic_val.index(max(dic_val))
        top = dic_key[inx]
        sell.append(top)
        dic_key.pop(inx)
        dic_val.pop(inx)
    top_sell = FoodItem.objects.filter(pk__in=sell)

    return render(request,'base/index.html',{'fooditem':fooditem,'breakfirst':breakfirst,'lunch':lunch,'dinner':dinner,'snacks':snacks,'exclusive':exclusive,'chefs':chefs,'top_sell':top_sell})

# particular product details
def productDetail(request,pk):
    item = FoodItem.objects.get(id=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(Q(fooditem=item.id) & Q(user=request.user)).exists() 
    return render(request,'base/details.html',{'item':item,'exists':item_already_in_cart})

# Add to cart
@login_required(login_url='login')
def addtocart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = FoodItem.objects.get(id=product_id)
    Cart(user=user,fooditem=product).save()
    return redirect('cart')

# Buy now
@login_required(login_url='login')
def buy_now(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = FoodItem.objects.get(id=product_id)
 Cart(user=user,fooditem=product).save()
 return redirect('/checkout')

# Cart
@login_required(login_url='login')
def cart(request):
    cart_item = Cart.objects.all().filter(user=request.user)
    amount = 0.0
    shipping_cost = 100.0
    total_amount = 0.0
    if cart_item:
        for item in cart_item:
            temp_amount = (item.quantity * item.fooditem.price)
            amount += temp_amount
            total_amount = amount + shipping_cost
        return render(request,'base/cart.html',{'carts':cart_item,'amount':amount,'total_amount':total_amount,'shipping_cost':shipping_cost})
    else:
        return render(request,'base/empty_cart.html')

# increase quantity of an item
def plus_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(fooditem=prod_id) & Q(user=request.user))
      c.quantity += 1
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         tempamount = (p.quantity * p.fooditem.price)
         amount += tempamount
      data = {
         'quantity':c.quantity,
         'amount':amount,
         'totalamount': amount + shipping_amount
            }
      return JsonResponse(data)

# decrease quantity of an item
def minus_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(fooditem=prod_id) & Q(user=request.user))
      if c.quantity != 1:
        c.quantity -= 1
        c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         tempamount = (p.quantity * p.fooditem.price)
         amount += tempamount
      data = {
         'quantity':c.quantity,
         'amount':amount,
         'totalamount': amount + shipping_amount
            }
      return JsonResponse(data)

# Remove an item from the cart.  
def remove_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(fooditem=prod_id) & Q(user=request.user))
      c.delete()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         tempamount = (p.quantity * p.fooditem.price)
         amount += tempamount
      data = {
         'amount':amount,
         'totalamount': amount + shipping_amount
            }
      return JsonResponse(data)

# Checkout page
@login_required(login_url='login')
def checkout(request):
    cart_item = Cart.objects.all().filter(user=request.user)
    user_address = Address.objects.filter(user=request.user)
    len_ad = len(Address.objects.filter(user=request.user))
    name = Customer.objects.get(user= request.user)
    amount = 0.0
    shipping_amount = 100.0
    if cart_item:
        for p in cart_item:
            tempamount = (p.quantity * p.fooditem.price)
            amount += tempamount
        totalamount = amount + shipping_amount
        if len_ad == 0:
            messages.info(request,"You don't have any address. Please update your address first.")
            
        return render(request,'base/checkout.html',{'cart_items':cart_item,'add':user_address,'name':name,'totalamount':totalamount,'len_ad':len_ad})   
    else:
        return render(request,'base/empty_cart.html')
    
@login_required(login_url='login')
def payment_done(request):
    user = request.user
    add_id = request.GET.get('custid')
    customer = Customer.objects.get(user=user)
    add = Address.objects.get(id=add_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,add=add,fooditem=c.fooditem,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@login_required(login_url='login')
def orders(requst):
    op = OrderPlaced.objects.filter(user=requst.user)
    customer = Customer.objects.get(user=requst.user)
    return render(requst,'base/orders.html',{'orders':op,'customer':customer})


# Reserve table
class BookATable(View):
    def get(self,request):
        form = BookTableForm()
        return render(request,'base/book_a_table.html',{'form':form})
    
    def post(self,request):
        form = BookTableForm(request.POST)
        if form.is_valid():
            dt = form.cleaned_data['date']
            form.save()
            if len(BookTable.objects.filter(date=dt)) == 3:
                last = BookTable.objects.all().last()
                last.delete()
                messages.success(request,"No slot available.")
            else:
                messages.success(request,'Booking successfull')
            form = BookTableForm()
        return render(request,'base/book_a_table.html',{'form':form})

# Food Menu
def foodMenu(request):
    fooditem = FoodItem.objects.filter(special=True)
    breakfirst = FoodItem.objects.filter(category='breakfirst')
    lunch = FoodItem.objects.filter(category='lunch')
    dinner = FoodItem.objects.filter(category='dinner')
    snacks = FoodItem.objects.filter(category='snack')
    return render(request,'base/food_menu.html',{'fooditem':fooditem,'breakfirst':breakfirst,'lunch':lunch,'dinner':dinner,'snacks':snacks})

def search(request):
    if request.method == 'GET':
        query = request.GET.get('quary')
        if query:
            if FoodItem.objects.filter(title__icontains=query).exists():
                item = FoodItem.objects.filter(title__icontains=query)
                return render(request,'base/search.html',{'product':item,'query':query})
            else:
                messages.success(request,'Product not available.')
                return render(request,'base/search.html',{'query':query})
        else:
            return redirect('menu')
    

# Chefs
def chefs(request):
    chefs = Chef.objects.all()
    return render(request,'base/chefs.html',{'chefs':chefs})

def contactUS(request):
    if request.method == 'GET':
        return render(request,'base/contact.html')
    if request.method == 'POST':
        print(request.POST['name'])
        info = GetInTouch(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message']
        )
        info.save()
        return render(request,'base/contact.html')

def newsLetter(request):
    eml = request.GET.get('email')
    news = NewsLetter(email=eml)
    news.save()
    return redirect('/')