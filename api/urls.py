from django.urls import path
from . import views
from .views import FriendsAPIView, MessageAPIView, GetFriendsAPIView, GroupAPIView, GroupMessageAPIView
from .views import ProductsAPIView, CountAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/register', views.register),
    path('api/login', views.login),
    path('friends', FriendsAPIView.as_view(), name='friends-list'),
    path('getfriends', GetFriendsAPIView.as_view(), name='get-friends-list'),
    path('message', MessageAPIView.as_view(), name='message'),
    path('message/<str:username>/<str:friendname>', MessageAPIView.as_view(), name='message'),
    path('addgroup', GroupAPIView.as_view(), name='addgroup'),
    path('addgroup/<str:username>', GroupAPIView.as_view(), name='addgroup'),
    path('groupmessage', GroupMessageAPIView.as_view(), name='addmessage'),
    path('groupmessage/<str:group_id>', GroupMessageAPIView.as_view(), name='addmessage'),
    path('products', ProductsAPIView.as_view(), name='products-api'),
    path('products/<str:product_id>', ProductsAPIView.as_view(), name='products-api-detail'),
    path('count/<int:product_id>', CountAPIView.as_view(), name='count')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
