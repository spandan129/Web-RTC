from django.db import models
import uuid
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images/')
    product_description = models.CharField(max_length=1000)
    product_category = models.CharField(max_length = 30)
    product_link = models.URLField(max_length=200, default='http://localhost:3000/product')
    product_view_count = models.IntegerField(default=0, blank=True, null=True) 

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=1000)
    sent_by = models.CharField(max_length=50)
    sent_to = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

class Friends(models.Model):
    Friend_id = models.AutoField(primary_key=True)
    Friend_name = models.CharField(max_length=20)
    message = models.ManyToManyField(Message,  blank=True)

    def __str__(self):
        return self.Friend_name

class Users(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    products = models.ManyToManyField(Products)
    friends = models.ManyToManyField(Friends, blank=True)
    def __str__(self):
        return self.username

class GroupMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=1000)
    sent_by = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message

class GroupUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    messages = models.ManyToManyField(GroupMessage, blank=True)
    def __str__(self):
        return self.user_name

class Group(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    group_name = models.CharField(max_length=50)
    group_users =  models.ManyToManyField(GroupUser, blank=True)
    def __str__(self):
        return self.group_name
    
   




