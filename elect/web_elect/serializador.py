from rest_framework import serializers
from .models import pedidos, cuotas, marcas, productos, usuarios

class SerialPedidos(serializers.ModelSerializer):
    class Meta:
        model=pedidos
        fields = [
            'id',
            'fecha',
            'fecha_primera_cuota',
            'cantidad_cuotas',
            'precio_cuota',
            'usuario_cliente',
            'producto',
            'estado',
        ]

class SerialDetallePedidos(serializers.ModelSerializer):
    class Meta:
        model=pedidos
        fields=[
            'id',
            'fecha',
            'fecha_primera_cuota',
            'cantidad_cuotas',
            'precio_cuota',
            'usuario_cliente',
            'producto',
            'estado',
            'fecha_aprobado'
        ]

class SerialMarcas(serializers.ModelSerializer):
    class Meta:
        model=marcas
        fields=[
            'id',
            'descripcion',
        ]

class SerialUsuarios(serializers.ModelSerializer):
    class Meta:
        model=usuarios
        fields = [
            'id',
            'nombre',
            'apellido',
            'username',
            'password',
            'telefono',
            'email',
            'direccion',
            'rol',
            'estado',
        ]

class SerialCuotas(serializers.ModelSerializer):
    class Meta:
        model=cuotas
        fields = [
            'id',
            'numero_cuota',
            'precio_cuota',
            'fecha_vencimiento',
            'estado_pago',
            'pedido'
        ]

class SerialProductos(serializers.ModelSerializer):
    class Meta:
        model=productos
        fields = [
            'id',
            'descripcion',
            'stock',
            'precio_total',
            'cantidad_cuotas',
            'precio_cuota',
            'marca',
            'imagen'
        ]

class SerialDetalleProductos(serializers.ModelSerializer):
    class Meta:
        model=productos
        fields = [
            'id',
            'descripcion',
            'stock',
            'precio_total',
            'cantidad_cuotas',
            'precio_cuota',
            'marca',
            'imagen'
        ]