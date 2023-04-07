from django.contrib import admin

# Register your models here.

from .models import *


class SubscriberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subscriber._meta.fields]


admin.site.register(Subscriber, SubscriberAdmin)
