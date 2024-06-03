from .models import Users
from rest_framework import serializers
from .models import Friends, Message, Group, GroupUser, GroupMessage
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id','message','sent_by','sent_to','date']

class FriendSerializer(serializers.ModelSerializer):
    message = MessageSerializer(required=False, allow_null=True, many=True)
    class Meta:
        model = Friends
        fields = ['Friend_id','Friend_name','message']

class UserSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(required=False, many=True)
    products = ProductsSerializer(required=False, many=True, allow_null=True,)
    class Meta:
        model = Users
        fields = '__all__'

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = '__all__'

class GroupUserSerializer(serializers.ModelSerializer):
    messages = GroupMessageSerializer(required=False, allow_null=True, many=True)
    class Meta:
        model = GroupUser
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    group_users = GroupUserSerializer(required=False, allow_null=True, many=True)
    class Meta:
        model = Group
        fields = '__all__'