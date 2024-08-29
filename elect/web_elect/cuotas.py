from datetime import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import cuotas, usuarios, marcas, pedidos, productos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def ver(request):
    if request.method=='GET':
        n_cuotas= cuotas.objects.all()  
        variables = {'request': request, 'n_cuotas': n_cuotas}
        print("Cuotas",variables)
        return render(request, 'cuotas.html', variables)


def nuevo(request):
    if request.method=='POST':
        if 'codigo_usuario' in request.session and 'nivel_usuario' in request.session:
            nivel_usuario = request.session['nivel_usuario']
            usuario_f= request.session['codigo_usuario']

            print("Nivel de usuario:",nivel_usuario)
            print("id del grupo","Codigo usuario:",usuario_f)
            if nivel_usuario in ['ADMINISTRADOR', 'EDITOR','LECTOR']: 
                f_numero_cuota = request.POST.get('numero_cuota')
                f_precio_cuota = request.POST.get('precio_cuota')
                f_fecha_vencimiento = request.POST.get('fecha_vencimiento')
                f_pedido = request.POST.get('pedido_id')
                pedido = pedidos.objects.get(pk=f_pedido)

                nuevacuota= cuotas(
                    numero_cuota= f_numero_cuota,
                    precio_cuota=precio_cuota,
                    fecha_vencimiento=fecha_vencimiento,
                    estado='0', #0 SIGNIFICA NO PAGADO - 1 SIGNIFICA PAGADO
                    pedido= pedido,
                )
                nuevacuota.save()
                # Verificar si el usuario es diferente de ADMINISTRADOR y EDITOR
                # if nivel_usuario in ['EDITOR','LECTOR']:
                #     messages.info(request, 'Su comentario está en revisión y será visible después de ser aprobado por un administrador ')

                return redirect('verpedido')
    
def borrar(request, id):
    if request.method == 'POST':
        comentario = get_object_or_404(cuotas, pk=id)
        pedido_id = cuota.pedido.id  # Guardar el ID de la pedido para redirigir después

        if 'codigo_usuario' in request.session and 'nivel_usuario' in request.session:
            usuario_f = request.session['codigo_usuario']
            nivel_usuario = request.session['nivel_usuario']

            if nivel_usuario in ['ADMINISTRADOR'] or cuota.autor.id == usuario_f:
                cuota.delete()
                messages.success(request, 'cuota eliminado exitosamente.')
                return redirect('verpedido')
            else:
                messages.error(request, 'No tiene permisos para eliminar este cuota.')
                return redirect('verpedido')
        else:
            messages.error(request, 'Debe estar autenticado para eliminar un cuota.')

        return redirect('verpedido', pedido_id=pedido_id)

    else:
        messages.error(request, 'Método no permitido.')
        return redirect('vernoticia', noticia_id=cuota.noticia.id)
    

def modificar(request, id):
    cuota = get_object_or_404(cuotas, pk=id)
    n_pedidos = pedidos.objects.all()
    print("Id de la cuota",cuota)
    if request.method == 'POST':
        f_numero_cuota = request.POST.get('numero_cuota')
        f_precio_cuota = request.POST.get('precio_cuota')
        f_fecha_vencimiento = request.POST.get('fecha_vencimiento')
        f_estado_pago = request.POST.get('estado_pago')
        f_pedido = request.POST.get('pedido')
        f_pedido_id = pedidos.objects.get(id=f_pedido)
        
        cuota.numero_cuota = f_numero_cuota
        cuota.precio_cuota = f_precio_cuota
        cuota.fecha_vencimiento = f_fecha_vencimiento
        cuota.estado_pago = f_estado_pago
        cuota.cantidad_cuotas = f_cantidad_cuotas
        cuota.pedido = get_object_or_404(pedidos, pk=f_pedido_id)
        cuota.save()
        return redirect('vercuota')

    return render(request, 'cuota_editar.html', {'cuota': cuota, 'n_pedidos': n_pedidos})


def vercuotas(request, pedido_id):
    estado_pago = request.GET.get('estado_pago', '')
    
    if estado_pago:
        cuotas_list = cuotas.objects.filter(pedido_id=pedido_id, estado_pago=estado_pago)
    else:
        cuotas_list = cuotas.objects.filter(pedido_id=pedido_id)
    
    contexto = {
        'pedido': pedido_id,
        'cuotas_list': cuotas_list
    }
    return render(request, 'cuotas.html', contexto)


# def vercuotas(request, pedido_id):
#     pedido = get_object_or_404(pedidos, id=pedido_id)
#     cuotas_list = cuotas.objects.filter(pedido=pedido)

#     context = {
#         'pedido': pedido,
#         'cuotas_list': cuotas_list,
#     }
#     return render(request, 'cuotas.html', context)

def pagarcuota(request, cuota_id):
    print("Ingresa a def pagarcuota")
    if request.method == 'POST':
        cuota = get_object_or_404(cuotas, id=cuota_id)
        print("cuota: ",cuota)
        cuota.estado_pago = '1'  # '1' representa pagado
        cuota.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)



@csrf_exempt
def verestadocuenta(request):
    print("Ingresa a verestadocuenta")
    if request.method == 'GET':
        try:
            # Recuperar el usuario del token
            token = request.headers.get('Authorization', '').split(' ')[-1]
            if not token:
                return JsonResponse({'error': 'No token provided'}, status=401)

            # Validar el token
            user = TokenAuthentication().authenticate_credentials(token)
            
            if user:
                user = user[0]  # `user` es una tupla (user, token)
            else:
                raise AuthenticationFailed('Invalid token')

            # Obtener el estado de cuenta
            cuotas = Cuotas.objects.filter(pedido__usuario_cliente=user, estado_pago='0')
            data = list(cuotas.values())  # Convertir queryset a lista de diccionarios
            return JsonResponse({'cuotas': data})
        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from .models import cuotas


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from .models import cuotas, pedidos
from django.contrib.auth import get_user_model


@csrf_exempt
@api_view(['GET'])
def ver_estado_cuenta(request):
    # Obtener el token de autorización desde el header
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        return JsonResponse({'error': 'Authorization header missing'}, status=401)

    try:
        # Extraer el token del header
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['user_id']  # Extrae el ID del usuario desde el token
        user = usuarios.objects.get(id=user_id)  # Obtén el usuario basado en el ID
    except (AuthenticationFailed, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid token or user not found'}, status=401)

    # Filtrar los pedidos del usuario
    pedidos_del_usuario = pedidos.objects.filter(usuario_cliente=user)

    # Filtrar las cuotas asociadas a esos pedidos y cuyo estado de pago sea '0'
    cuotas_pendientes = cuotas.objects.filter(pedido__in=pedidos_del_usuario, estado_pago='0')

    # Serializar los datos
    cuotas_data = [{
        'numero_cuota': cuota.numero_cuota,
        'precio_cuota': cuota.precio_cuota,
        'fecha_vencimiento': cuota.fecha_vencimiento,
        'estado_pago': cuota.estado_pago
    } for cuota in cuotas_pendientes]

    return JsonResponse({'cuotas': cuotas_data})


# @csrf_exempt
# @api_view(['GET'])
# def ver_estado_cuenta(request):
#     print("Ingrea a ver_estado_cuenta")
#     # Obtener el token de autorización desde el header
#     auth_header = request.headers.get('Authorization', None)
#     print("auth_header: ",auth_header)
#     if auth_header is None:
#         return JsonResponse({'error': 'Authorization header missing'}, status=401)

#     try:
#         # Extraer el token del header
#         token = auth_header.split(' ')[1]
#         access_token = AccessToken(token)
#         print("access_token: ",access_token)
#         user_id = access_token['user_id']  # Extrae el ID del usuario desde el token
#         print("user_id: ",user_id)
#         #Verificar si al hacer login, estoy guardando el user id junto o solo el username
#         #Porque al tratar de recuperar según el user id, necesita estar guardado para que pueda recuperar.
#         user = usuarios.objects.get(id=user_id)  # Obtén el usuario basado en el ID
#         print("user: ",user)
#     except (AuthenticationFailed, User.DoesNotExist):
#         return JsonResponse({'error': 'Invalid token or user not found'}, status=401)

#     # Filtra las cuotas por estado_pago = '0' y usuario asociado al pedido
#     pedidos_usuario = pedidos.objects.filter(usuario_cliente=user, estado_pago='0')
#     # o debe ser user.id el filter --ver-- pedidos_usuario = pedidos.objects.filter(usuario_cliente=user.id, estado_pago='0')
#     cuotas_pendientes = cuotas.objects.filter(pedido=pedidos_usuario, estado_pago='0')
#     #Ver cómo recuperar las cuotas no pagadas por usuario- o si debe recorrerse un array o algo así
#     print("cuotas_pendientes: ",cuotas_pendientes)

#     # Serializa los datos
#     cuotas_data = [{
#         'numero_cuota': cuota.numero_cuota,
#         'precio_cuota': cuota.precio_cuota,
#         'fecha_vencimiento': cuota.fecha_vencimiento,
#         'estado_pago': cuota.estado_pago
#     } for cuota in cuotas_pendientes]

#     return JsonResponse({'cuotas': cuotas_data})


# @csrf_exempt
# def verestadocuenta(request):
#     if request.method == 'GET':
#         user = request.user
#         print("request: ",request)
#         print("user: ",user)
#         cuotas_pendientes = cuotas.objects.filter(
#             pedido__usuario_cliente=user,
#             estado_pago='0'
#         )
#         print("cuotas_pendientes: ",cuotas_pendientes)
#         print("cuotas_pendientes.values: ",cuotas_pendientes.values)
#         cuotas_list = list(cuotas_pendientes.values('id', 'numero_cuota', 'precio_cuota', 'fecha_vencimiento', 'estado_pago'))
#         print("cuotas_list: ",cuotas_list)
#         return JsonResponse({'cuotas': cuotas_list})
#     return JsonResponse({'error': 'Método no permitido'}, status=405)