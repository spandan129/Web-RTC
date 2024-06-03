from django.db.models import Q
from .models import Users
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Friends, Message, Group, GroupUser, GroupMessage
from django.core.paginator import Paginator, EmptyPage
from .models import Products
from .serializers import ProductsSerializer
from .serializers import FriendSerializer, UserSerializer, MessageSerializer, GroupSerializer, GroupMessageSerializer, GroupUserSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response({'sucess'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = Users.objects.get(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        payload = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username
        }
        return Response(payload)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductsAPIView(APIView):
    def get(self, request):
        unique_categories = Products.objects.values_list('product_category', flat=True).distinct()
        page_n = int(request.GET.get('page', 1))
        each_category_size = int(request.GET.get('page_size', 5))

        paginated_data = []
        next_page_numbers = {}
        previous_page_numbers = {}

        has_next = False  # Initialize has_next to False outside the loop

        for category in unique_categories:
            products = Products.objects.filter(product_category=category).order_by('product_id')
            p = Paginator(products, each_category_size)

            try:
                page = p.page(page_n)
            except EmptyPage:
                page = p.page(1)

            serializer = ProductsSerializer(page, many=True)
            paginated_data.extend(serializer.data)
            next_page_numbers[category] = page.next_page_number() if page.has_next() else None
            previous_page_numbers[category] = page.previous_page_number() if page.has_previous() else None


            has_next = has_next or page.has_next()

        # Return serialized data with pagination information for each category
        return Response({
            'results': paginated_data,
            'next': next_page_numbers,
            'previous': previous_page_numbers,
            'has_next': has_next,
        })

    def post(self, request):
        username = request.data.get('username')
        try:
            user_obj = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)
        
        try:
            product = Products.objects.create(
                product_id = request.data.get('product_id'),
                product_name = request.data.get('product_name'),
                product_price = request.data.get('product_price'),
                product_image = request.data.get('product_image'),
                product_description = request.data.get('product_description'),
                product_category = request.data.get('product_category'),
                product_link = request.data.get('product_link'),
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        user_obj.products.add(product)

        return Response('Success', status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            to_delete_product = Products.objects.get(product_id=product_id)
            if to_delete_product is not None:
                to_delete_product.delete()
                return Response(f'{product_id} deleted successfully')
        except Products.DoesNotExist:
            return Response(f'Product with ID {product_id} does not exist', status=status.HTTP_404_NOT_FOUND)
        
class CountAPIView(APIView):

    def put(self, request, product_id):
        print(product_id)
        try:
            product = Products.objects.get(product_id=product_id)
            product.product_view_count += 1
            product.save()
            return Response({'message': 'Product count incremented successfully'}, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred while updating product count'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FriendsAPIView(APIView):
    def post(self, request):
        try:
            friends_name = request.data.get('Friend_name')
            users_name = request.data.get('user')
            
            if not friends_name or not users_name:
                return Response("Friend_name and user fields are required.")
            
            if friends_name == users_name:
                return Response("Friend_name and user cannot be the same.")

            friend = Friends.objects.create(
                Friend_name=friends_name
            )
            user = Friends.objects.create(
                Friend_name=users_name
            )
            
            try:
                friend_obj = Users.objects.get(username=friends_name)
                friend_obj.friends.add(user)
            except ObjectDoesNotExist:
                return Response(f"No user found with the username '{friends_name}'.")
            
            try:
                user_obj = Users.objects.get(username=users_name)
                user_obj.friends.add(friend)
            except ObjectDoesNotExist:
                return Response(f"No user found with the username '{users_name}'.")
            
            return Response('Added successfully')
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetFriendsAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = Users.objects.get(username=username)
            print(user)
            friends = user.friends.all() 

            friend_data = []
            for friend in friends:
                friend_serializer = FriendSerializer(friend) 
                friend_data.append(friend_serializer.data)

            return Response(friend_data)
        except Users.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class MessageAPIView(APIView):
    def post(self, request):
        print(request.data)
        sender_username = request.data.get('sentby')
        receiver_username = request.data.get('sentto')
        message_content = request.data.get('message')
        try:
            sender_user = Users.objects.get(username=sender_username)
            receiver_user = Users.objects.get(username=receiver_username)
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        message = Message.objects.create(
            message=message_content,
            sent_by=sender_username,
            sent_to=receiver_username
        )
        sender = sender_user.friends.get(Friend_name=receiver_username)
        receiver = receiver_user.friends.get(Friend_name=sender_username)
        
        sender.message.add(message)
        receiver.message.add(message)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
    
    def get(self,request, username, friendname):
        user_obj = Users.objects.get(username=username)
        users_friend_obj = user_obj.friends.get(Friend_name=friendname)
        user_friend_messages = users_friend_obj.message.filter(Q(sent_by=username) | Q(sent_by=friendname))
        ordered_user_friend_messages = user_friend_messages.order_by('date')
        serializer = MessageSerializer(ordered_user_friend_messages, many=True)
        return Response(serializer.data) 

class GroupAPIView(APIView):
    def get(self, request, username):
        groups = Group.objects.filter(group_users__user_name=username)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        group_name = request.data.get('groupName')
        group_users = request.data.get('groupUser').get('id')
        
        group = Group.objects.create(group_name=group_name)
        group.save()
        for user in group_users:
            group_user = GroupUser.objects.create(user_name=user)
            group.group_users.add(group_user)

        return Response('Success')
    
class GroupMessageAPIView(APIView):
    def post(self, request):
        group_id = request.data.get('groupId')
        message = request.data.get('message')
        sent_by = request.data.get('sentBy')
        
        try:
            group_obj = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response("Group not found", status=404)
        
        try:
            group_user = GroupUser.objects.get(group=group_obj, user_name=sent_by)
        except GroupUser.DoesNotExist:
            return Response("Group user not found", status=404)
        
        add_message = GroupMessage.objects.create(
            message=message,
            sent_by=sent_by
        )

        group_user.messages.add(add_message)

        return Response('Message Saved')
    
    def get(self, request, group_id):
     group = Group.objects.get(group_id=group_id)
     group_users = group.group_users.all() 
     all_messages = []

     for user in group_users:
        messages = user.messages.all()  
        all_messages.extend(messages)

     sorted_messages = sorted(all_messages, key=lambda x: x.date) 
     serializer = GroupMessageSerializer(sorted_messages, many=True)
     return Response(serializer.data)

        


