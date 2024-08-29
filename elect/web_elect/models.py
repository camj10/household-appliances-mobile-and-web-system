from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class marcas(models.Model):
    descripcion = models.CharField(max_length=255)

class productos(models.Model):
    descripcion = models.CharField(max_length=255)
    stock = models.IntegerField()
    precio_total = models.IntegerField()
    cantidad_cuotas = models.IntegerField()
    precio_cuota = models.IntegerField()
    imagen = models.CharField(max_length=200)
    marca = models.ForeignKey(marcas,on_delete=models.RESTRICT)
    estado = models.CharField(max_length=5, null=True, blank=True)

class usuarios(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=128)  # Aumenta la longitud para almacenar contraseñas hasheadas
    telefono = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    rol = models.CharField(max_length=2)  # 1 CLIENTE 2 AUXILIAR 3 ADMINISTRADOR
    estado = models.CharField(max_length=25)

    def save(self, *args, **kwargs):
        # Hashea la contraseña antes de guardarla en la base de datos
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class pedidos(models.Model):
    fecha = models.DateField(auto_now_add=True)
    fecha_primera_cuota = models.DateField(null=True, blank=True)
    cantidad_cuotas = models.IntegerField()
    precio_cuota = models.IntegerField()
    usuario_cliente = models.ForeignKey(usuarios, on_delete=models.RESTRICT)
    producto = models.ForeignKey(productos, on_delete=models.RESTRICT)
    estado = models.CharField(max_length=30)
    fecha_aprobado = models.DateField(null=True, blank=True)

class cuotas(models.Model):
    numero_cuota = models.IntegerField()
    precio_cuota = models.IntegerField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado_pago = models.CharField(max_length=2)
    pedido = models.ForeignKey(pedidos, on_delete=models.RESTRICT)