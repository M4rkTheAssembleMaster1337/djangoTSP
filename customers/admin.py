from django.contrib import admin

# Register your models here.
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]

    class Meta:
        model = Customer


admin.site.register(Customer, CustomerAdmin)
