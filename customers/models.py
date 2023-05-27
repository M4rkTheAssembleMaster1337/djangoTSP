from django.db import models


# Create your models here.


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    password1 = models.CharField(max_length=36, blank=True, null=True, default=None)
    password2 = models.CharField(max_length=36, blank=True, null=True, default=None)

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.email)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
