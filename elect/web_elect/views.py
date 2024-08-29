from rest_framework import generics
from .serializador import SerialPedidos, SerialDetallePedidos, SerialMarcas, SerialUsuarios, SerialCuotas, SerialProductos, SerialDetalleProductos
from .models import pedidos, cuotas, marcas, productos, usuarios
# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import usuarios
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

def status_check(request):
    return JsonResponse({'status': 'ok'})

def get_csrf_token(request):
    token = get_token(request)
    print("token: ",token)
    return JsonResponse({'csrfToken': token})

@csrf_exempt
def login_c(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid input'}, status=400)

        print("username: ", username, "password: ", password)
        
        try:
            test=usuarios.objects.all()
            print("Los usuarios: ", test[0].username, " otro usuario ",test[1].username)

            user = usuarios.objects.get(username=username)
            print("user: ",user)
            print("user.username: ",user.username)
            print("user.id: ",user.id)
            user_data = {
                'username': user.username,
                'id': user.id,
            }
        except usuarios.DoesNotExist:
            print("Primer except")
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        if user is not None: 
            print("Antes del if chackpass - Variables: password: ",password, " user.password: ",user.password)
            if check_password(password, user.password):
                print("Ingresa al if")
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_data
                })
            else:
                print("else check_password")
        else:
            print("else user is not None")
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))  # Hashea la contraseña
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        rol = request.POST.get('rol')
        estado = request.POST.get('estado')
        
        # Crea el usuario en la base de datos
        user = usuarios.objects.create(
            nombre=nombre,
            apellido=apellido,
            username=username,
            password=password,
            telefono=telefono,
            email=email,
            direccion=direccion,
            rol=rol,
            estado=estado
        )
        
        # Puedes hacer otras operaciones después de crear el usuario, como enviar un email de confirmación, etc.
        
        return redirect('login')  # Redirige al usuario al formulario de login
        
    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid input'}, status=400)

        print("username: ", username, "password: ", password)
        
        try:
            user = usuarios.objects.get(username=username)
        except usuarios.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        if user is not None and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            userid = user.id
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'userId': userid,
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    print("No es método POST")
    return render(request, 'login.html')

def inicio(request):
    if request.GET.get('userId'):
        print("Ingresa a def inicio")
        userid = request.GET.get('userId')
        print("userid: ",userid)
        usuario = usuarios.objects.filter(id=userid)
        print("usuario[0].username: ",usuario[0].username)
        print("usuario[0].rol: ",usuario[0].rol)
        rolusuario = usuario[0].rol
        context = {
            'rolusuario': rolusuario 
        }
        return render(request, 'inicio.html', context)
    else:
        return render(request, 'inicio.html')

@csrf_exempt
@api_view(['GET'])
def get_products(request):
    print("Ingresa a get_products")
    user = request.user
    products = productos.objects.filter(estado='1', stock__gt=0)
    serializer = SerialProductos(products, many=True)
    print("serializer: ",serializer)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['GET'])
def lista_productos(request):
    print("Ingresa a def lista_productos")
    productos_list = productos.objects.filter(estado='1', stock__gt=0)
    serializer = SerialProductos(productos_list, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def product_detail(request, id):
    producto = get_object_or_404(productos, id=id)
    data = {
        'id': producto.id,
        'descripcion': producto.descripcion,
        'marca': producto.marca,
        'precio_total': producto.precio_total,
        'precio_cuota': producto.precio_cuota,
        'cantidad_cuotas': producto.cantidad_cuotas,
        'stock': producto.stock,
    }
    return JsonResponse(data)


@csrf_exempt
def crear_pedido(request):
    print("Ingresa a def crear_pedido")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        producto = get_object_or_404(productos, id=data['producto'])
        print("request.user: ",request.user)
        usuario_cliente = request.user  # Obtén el usuario autenticado
        pedido = pedidos.objects.create( 
            fecha_primera_cuota=data.get('fecha_primera_cuota'),
            cantidad_cuotas=data.get('cantidad_cuotas', 1),
            precio_cuota=data.get('precio_cuota', producto.precio_total),
            usuario_cliente=usuario_cliente,
            producto=producto,
            estado='pendiente',
        )
        return JsonResponse({'message': 'Pedido creado exitosamente', 'pedido_id': pedido.id}, status=201)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import pedidos

User = get_user_model()

@csrf_exempt
def create_order(request):
    print("Ingresa a def create_order")
    if request.method == 'POST':
        try:
            # Obtener el token de acceso desde el encabezado Authorization
            auth_header = request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            access_token = auth_header.split(' ')[1]
            # Decodificar el token y obtener el usuario
            decoded_token = AccessToken(access_token)
            user_id = decoded_token['user_id']
            user = usuarios.objects.get(id=user_id)

            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            producto_id = data.get('producto')
            cantidad_cuotas = data.get('cantidad_cuotas')
            precio_cuota = data.get('precio_cuota')

            # Crear el pedido
            nuevo_pedido = pedidos.objects.create(
                usuario_cliente=user,
                producto_id=producto_id,
                cantidad_cuotas=cantidad_cuotas,
                precio_cuota=precio_cuota,
                estado='pendiente',  # Ajustar según sea necesario
                fecha_aprobado=None,  # Ajustar según sea necesario
            )
            return JsonResponse({'message': 'Pedido creado exitosamente'}, status=201)

        except (ValueError, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid token or user'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid input'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
@api_view(['GET'])

def product_detail_view(request, id):
    try:
        product = productos.objects.get(pk=id)
        data = {
            'descripcion': product.descripcion,
            'marca': product.marca.descripcion,  # Ajusta esto según tu modelo
            'precio_total': product.precio_total,
            'stock': product.stock,
            'cantidad_cuotas': product.cantidad_cuotas,
            'precio_cuota': product.precio_cuota,
            'imagen': product.imagen if product.imagen else None,
        }
        return JsonResponse(data)
    except productos.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)




@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World! This is a protected endpoint."})


def verusuarios(request):
    if request.method == 'GET':
        lista_usuarios = list(usuarios.objects.all().values())  # Obtén todos los usuarios como lista de diccionarios
        
        return JsonResponse({"lista": lista_usuarios})

class ProductosAPINuevo(generics.CreateAPIView):
    queryset=productos.objects.all()
    serializer_class=SerialProductos

# views.py
from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al usuario al formulario de login

def logout_c(request):
    logout(request)
    return JsonResponse({"Sesión cerrada"})

# Create your views here.
#PEDIDOS
class PedidosAPILista(generics.ListAPIView):
    queryset=pedidos.objects.all()
    serializer_class=SerialPedidos

class PedidosAPIModificar(generics.RetrieveAPIView):
    lookup_field='id'
    queryset=pedidos.objects.all()
    serializer_class=SerialDetallePedidos

class PedidosAPINuevo(generics.CreateAPIView):
    queryset=pedidos.objects.all()
    serializer_class=SerialPedidos

#MARCAS
class MarcasAPILista(generics.ListAPIView):
    queryset=marcas.objects.all()
    serializer_class=SerialMarcas

class MarcasAPINuevo(generics.CreateAPIView):
    queryset=marcas.objects.all()
    serializer_class=SerialMarcas

class MarcasAPIModificar(generics.RetrieveUpdateAPIView):
    lookup_field='id'
    queryset=marcas.objects.all()
    serializer_class=SerialMarcas

class MarcasAPIBorrar(generics.DestroyAPIView): # Borrar definitivamente.
    lookup_field='id'
    queryset=marcas.objects.all()

#USUARIOS
class UsuariosAPILista(generics.ListAPIView):
    queryset=usuarios.objects.all()
    serializer_class=SerialUsuarios

#CUOTAS
class CuotasAPILista(generics.ListAPIView):
    queryset=cuotas.objects.all()
    serializer_class=SerialCuotas

class CuotasAPIBorrar(generics.DestroyAPIView):  # Borrar definitivamente.
    lookup_field='id'
    queryset=cuotas.objects.all()

class CuotasAPIModificar(generics.RetrieveUpdateAPIView):
    lookup_field='id'
    queryset=cuotas.objects.all()
    serializer_class=SerialCuotas
    
class CuotasAPINuevo(generics.CreateAPIView):
    queryset=cuotas.objects.all()
    serializer_class=SerialProductos

#PRODUCTOS
class ProductosAPILista(generics.ListAPIView):
    queryset=productos.objects.all()
    serializer_class=SerialProductos

class ProductosAPIDetalle(generics.RetrieveAPIView):
    lookup_field='id'
    queryset=productos.objects.all()
    serializer_class=SerialDetalleProductos

class ProductosAPIBorrar(generics.DestroyAPIView):  # Borrar definitivamente.
    lookup_field='id'
    queryset=productos.objects.all()

class ProductosAPIModificar(generics.RetrieveUpdateAPIView):
    lookup_field='id'
    queryset=productos.objects.all()
    serializer_class=SerialProductos
    
class ProductosAPINuevo(generics.CreateAPIView):
    queryset=productos.objects.all()
    serializer_class=SerialProductos