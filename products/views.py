from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductAPIView(APIView):
    def get(self, request):
        lst = Product.objects.all().values()
        return Response({'posts': list(lst)})

    def post(self, request):
        return Response({'hello': 'abacaba'})
# class ProductAPIView(generics.ListAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer
