from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from .models import Order
#from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProductInOrder
from .models import Customer
from django.forms import model_to_dict

class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        lst = Order.objects.all().values()
        return Response({'posts': list(lst)})

    def post(self, request):
        print(request.data['product_id'][0])
        print(request.user)
        print(type(request.user))
        #print(type(request.data))
        post_new = Order.objects.create(
            user=request.user,
            status_id=1,
            #customer_email=request.data['customer_email'],
            #customer_phone=request.data['customer_phone'],
            #customer_address=request.data['customer_address'],
            total_price=0
        )
        post_new_dict = model_to_dict(post_new)
        print(post_new_dict)
       #print(request.data['product_id'][0])
        for i in range(len(request.data['product_id'])):
            post_new2 = ProductInOrder.objects.create(
                product_id=request.data['product_id'][i],
                nmb=request.data['nmb'][i],
                order_id=post_new_dict['id']
            )

        return Response({'post_new2': 'Order created'})