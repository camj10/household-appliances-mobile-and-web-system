from django.contrib import admin
from .models import usuarios, marcas, productos, pedidos, cuotas

admin.site.register(usuarios)
admin.site.register(marcas)
admin.site.register(productos)
admin.site.register(pedidos)
admin.site.register(cuotas)
# Register your models here.
