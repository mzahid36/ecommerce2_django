from django.db import models
from django.contrib.auth.models import User

# Create your models here.

gender_choice = (
    ('male','Male'),
    ('female','Female'),
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    gender = models.CharField(choices=gender_choice,max_length=30,null=True,blank=True)
    profile_pic = models.ImageField(default="profile_pic/profile1.png",upload_to='profile_pic',null=True,blank=True)

    def __str__(self):
        return str(self.id)

DIVISION_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    division = models.CharField(max_length=20,choices=DIVISION_CHOICES)
    district = models.CharField(max_length=30)
    thana = models.CharField(max_length=20)
    holding_street_village = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('breakfirst', 'breakfirst'),
    ('lunch', 'lunch'),
    ('dinner', 'dinner'),
    ('snack','snacks'),
    ('exclusive','exclusive')
)

class FoodItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    special = models.BooleanField(default=False)
    food_img = models.ImageField(upload_to='Food Image')
    
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    fooditem = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.fooditem.price
    
STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    add = models.ForeignKey(Address,on_delete=models.CASCADE, blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.fooditem.price
    

class Chef(models.Model):
    name = models.CharField(max_length=20)
    designation = models.CharField(max_length=30)
    fb_link = models.CharField(max_length=100,blank=True,null=True)
    tw_link = models.CharField(max_length=100,blank=True,null=True)
    ins_link = models.CharField(max_length=100,blank=True,null=True)
    chef_img = models.ImageField(upload_to='chefs',blank=True,null=True)

    def __str__(self):
        return str(self.id)
    
class NewsLetter(models.Model):
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email
    
class GetInTouch(models.Model):
    message = models.TextField(null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.CharField(max_length=50,null=True,blank=True)
    subject = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.name
    

PERSON_LIST = (
    ('1','Number of guests 1'),
    ('2','Number of guests 2'),
    ('3','Number of guests 3'),
    ('4','Number of guests 4'),
    ('5','Number of guests 5'),
)



class BookTable(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    persons = models.CharField(max_length=50,choices=PERSON_LIST)
    phone = models.CharField(max_length=14)
    note = models.TextField()

    date = models.DateField()

    def __str__(self):
        return self.name

    


