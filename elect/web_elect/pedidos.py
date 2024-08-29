from datetime import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.base import ContentFile
from .models import cuotas, usuarios, marcas, pedidos, productos
from django.conf import settings    
import os
from pathlib import Path
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib import messages

def ver(request):
    if request.method == 'GET':
        n_pedidos= pedidos.objects.all()  
        variables = {'request': request, 'n_pedidos': n_pedidos}
        print("Pedidos",variables)
        return render(request, 'ver_noticia.html', variables)

def verDetalle(request,id):
    if request.method == 'GET':
        n_pedidos = pedidos.objects.filter(id=id)
        print("n_pedidos: ",n_pedidos)
        return JsonResponse({'n_pedidos': n_pedidos}, status=201)


def verAprobados(request):
    orden = request.GET.get('orden', 'asc')
    print("orden: ",orden)
    if orden == 'desc':
        n_pedidos = pedidos.objects.all().filter(estado='aprobado').order_by('-fecha')
    else:
        n_pedidos = pedidos.objects.all().filter(estado='aprobado').order_by('fecha')
    if request.method == 'GET':
        variables = {'request': request, 'n_pedidos': n_pedidos}
        print("Pedidos",variables)
        return render(request, 'pedidos.html', variables)

def resumen(request):
    if request.method == 'GET':
        c_pedidos_aprobados = Pedidos.objects.filter(estado='aprobado').count()
        c_pedidos_pendientes = Pedidos.objects.filter(estado='pendiente').count()
        c_pedidos_desaprobados = Pedidos.objects.filter(estado='desaprobado').count()

        context = {
            'c_pedidos_aprobados': n_pedidos,
            'c_pedidos_pendientes': n_productos,
            'c_pedidos_desaprobados': c_pedidos_desaprobados,
        }
        return render(request, 'resumen.html', context)

def verPendientes(request):
    orden = request.GET.get('orden', 'asc')
    print("orden: ",orden)
    if orden == 'desc':
        n_pedidos = pedidos.objects.all().filter(estado='pendiente').order_by('-fecha')
    else:
        n_pedidos = pedidos.objects.all().filter(estado='pendiente').order_by('fecha')
    if request.method == 'GET':
        n_usuarios = usuarios.objects.all()
        n_productos = productos.objects.all()
        
        pedidos_list = []
        for pedido in n_pedidos:
            pedidos_list.append({
                'id': pedido.id,
                'fecha': pedido.fecha,
                'fecha_primera_cuota': pedido.fecha_primera_cuota,
                'cantidad_cuotas': pedido.cantidad_cuotas,
                'precio_cuota': pedido.precio_cuota,
                'usuario_cliente': pedido.usuario_cliente.username,  
                'producto': pedido.producto.descripcion, 
                'estado': pedido.estado,
                'fecha_aprobado': pedido.fecha_aprobado
            })
        print("pedidos_list: ",pedidos_list)
        context = {
            'n_pedidos': n_pedidos,
            'n_productos': n_productos,
            'n_usuarios': n_usuarios,
            'orden': orden
        }
        return render(request, 'pendientes.html', context)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# def verPendientes(request):
#     if request.method == 'GET':
#         n_pedidos = pedidos.objects.filter(estado='pendiente')
#         print("n_pedidos pendientes",n_pedidos)
#         return JsonResponse({'n_pedidos': n_pedidos}, status=201)

def verDesaprobados(request):
    if request.method == 'GET':
        if request.session['nivel_usuario']:
            n_pedidos = pedidos.objects.filter(estado='desaprobado')
            variables = {'request': request, 'n_pedidos': n_pedidos}
            print("Pedidos",variables)
            return render(request, 'pedidos.html', variables)
        else: 
            return render(request, 'acceder.html', {'m_error': 'Inicie sesión'}) 

def aprobar(request, pedido_id):
    if request.method == 'POST':
        print("Ingresa a def aprobar")
        try:
            pedido = pedidos.objects.get(id=pedido_id)
            v_producto = pedido.producto
            print("v_producto: ",v_producto)

            # Aprobar el pedido
            pedido.estado = 'aprobado'
            pedido.fecha_aprobado=datetime.now().date()
            pedido.fecha_primera_cuota = datetime.now().date() + relativedelta(days=30)
            pedido.save()
            
            # Actualizar el stock del producto vendido:
            v_id_producto = v_producto.id
            producto = productos.objects.get(id=v_id_producto)
            print("producto de la db por la id: ",producto)
            v_stock = producto.stock
            new_stock = v_stock -1
            producto.stock = new_stock
            producto.save()

            # Crear las cuotas
            fecha_vencimiento = pedido.fecha_primera_cuota
            for i in range(1, pedido.cantidad_cuotas + 1):
                cuotas.objects.create(
                    numero_cuota=i,
                    precio_cuota=pedido.precio_cuota,
                    estado_pago='0',
                    pedido=pedido
                )
                # Incrementar la fecha de vencimiento por 30 días para la próxima cuota
                fecha_vencimiento += relativedelta(days=30)
            
            messages.success(request, 'Producto aprobado.')
            return JsonResponse({'success': True})
        except pedidos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def desaprobar(request, pedido_id):
    if request.method == 'POST':
        try:
            pedido = pedidos.objects.get(id=pedido_id)
            pedido.estado = 'desaprobado'
            pedido.save()
            messages.warning(request, 'Producto desaprobado.')
            return JsonResponse({'success': True})
        except pedidos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def verAprobadosFecha(request):
    orden = request.GET.get('orden', 'asc')
    if orden == 'desc':
        n_pedidos = pedidos.objects.all().filter(estado='aprobado').order_by('-fecha_aprobado')
    else:
        n_pedidos = pedidos.objects.all().filter(estado='aprobado').order_by('fecha_aprobado')

    context = {
        'n_pedidos': n_pedidos,
        'orden': orden
    }
    return render(request, 'aprobados.html', context)


@csrf_exempt
@api_view(['GET'])
def pedidosusuario(request):
    # Obtener el token de autorización desde el header
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        return JsonResponse({'error': 'Authorization header missing'}, status=401)
    try:
        # Extraer el token del header
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['user_id']  
        user = usuarios.objects.get(id=user_id)  
    except Exception as e:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    try:
        pedidos_usuario = pedidos.objects.filter(usuario_cliente=user)
        pedidos_list = list(pedidos_usuario.values())
        return JsonResponse({'pedidos': pedidos_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



# def nuevo(request):
#     print("Ingresa nuevo pedido")
#     if request.method=='GET':
#         n_productos= productos.objects.all()  
#         n_usuarios= usuarios.objects.all()  
#         variables = {'request': request, 'n_productos': n_productos,'n_usuarios': n_usuarios}
#         print("Hola")
#         return render(request, 'pedido_nuevo.html', variables)
#     if request.method=='POST':
#         print("Hola")
#         if 'codigo_usuario' in request.session and 'nivel_usuario' in request.session:
#             nivel_usuario = request.session['nivel_usuario']
#             usuario_f= request.session['codigo_usuario']
           
#             print("Nivel de usuario:",nivel_usuario)
#             print("id del grupo","Codigo usuario:",usuario_f)
#             if nivel_usuario in ['ADMINISTRADOR', 'EDITOR']: 
#                 f_fecha = datetime.datetime.now()
#                 f_fecha_primera_cuota = f_fecha + relativedelta(days=30)
#                 f_cantidad_cuotas = request.POST.get('cantidad_cuotas')
#                 f_precio_cuota = request.POST.get('precio_cuota')
#                 id_producto = productos.objects.get(id=f_producto)
#                 f_estado = 'PENDIENTE'
#                 # Me falta guardar el cliente que solicitó
#                 nuevanoticia = noticias(
#                     fecha=f_fecha,
#                     fecha_primera_cuota=f_fecha_primera_cuota,
#                     cantidad_cuotas=f_cantidad_cuotas,
#                     precio_cuota=f_precio_cuota,
#                     estado=f_estado,
#                     producto=id_producto,
#                     usuario_cliente=
#                 )
#                 nuevanoticia.save()
                
#                 return redirect('vernoticia')
#             else:
#                 # Manejar el caso de que no se haya proporcionado una imagen
#                 return render(request, 'noticia_nueva.html', {'error': 'Debe proporcionar una imagen'})
#         else: return render(request, 'acceder.html', {'m_error': 'Inicie sesión'})

# def borrarno(request, id):
#     para_borrar =noticias.objects.get(pk=id)
#     para_borrar.delete()
#     return redirect('vernoticia')


# def modificarno(request, id):

#     noticia = get_object_or_404(noticias, pk=id)
#     n_grupos = grupos.objects.all()
#     print("Id de la noticia",noticia)
#     # Si se envió un formulario con datos para actualizar el usuario
#     if request.method == 'POST':
#         f_titulo = request.POST.get('titulo')
#         f_grupo_id = request.POST.get('grupo')
#         f_cuerpo = request.POST.get('cuerpo')
#         f_imagen = request.FILES.get('imagen')
#         print("Current imagen value:", noticia.imagen)
#         # Eliminar la imagen anterior si existe y se ha proporcionado una nueva imagen
#         if f_imagen:
#             if noticia.imagen :
#                 ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, str(noticia.imagen.path))
#                 print("Ruta de la imagen anterior:", ruta_imagen_anterior)
#                 if os.path.exists(ruta_imagen_anterior):
#                     os.remove(ruta_imagen_anterior)
#                     print(f"Imagen anterior eliminada: {ruta_imagen_anterior}")

#                 ruta_imagen = 'imagenes/' + f_imagen.name
#                 ruta_imagen_completa = os.path.join(settings.MEDIA_ROOT, ruta_imagen)
#                 print(ruta_imagen_completa)
#                 with open(ruta_imagen_completa, 'wb+') as destination:
#                     for chunk in f_imagen.chunks():
#                         destination.write(chunk)
#                 noticia.imagen = f_imagen
#         noticia.titulo = f_titulo
#         noticia.grupo = get_object_or_404(grupos, pk=f_grupo_id)
#         noticia.cuerpo = f_cuerpo
#         noticia.save()

#         return redirect('vernoticia')

#     return render(request, 'noticia_editar.html', {'noticia': noticia, 'n_grupos': n_grupos})
