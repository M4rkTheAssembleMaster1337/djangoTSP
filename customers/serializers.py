#from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone', 'address')


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Customer
        fields = ('name', 'email', 'password1','password2')
        extra_kwargs = {
            'passwrod': {'write_only':True}
        }
