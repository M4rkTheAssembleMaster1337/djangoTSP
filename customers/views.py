from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer

class CustomerAPIView(APIView):
    def post(self, request):
        post_new = Customer.objects.create(
            name=request.data['name'],
            email=request.data['email'],
            phone=request.data['phone'],
            address=request.data['address']

        )
        return Response({'post': model_to_dict(post_new)})


