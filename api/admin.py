from django.contrib import admin

# Register your models here.
from .models import Friends, Users, Message, Group, GroupMessage, GroupUser
# Register your models here.
from .models import Products
# Register your models here.
admin.site.register(Products)
admin.site.register(Friends)
admin.site.register(Users)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(GroupMessage)
