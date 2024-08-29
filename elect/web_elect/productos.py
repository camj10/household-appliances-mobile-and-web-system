from django.shortcuts import render, redirect, get_object_or_404
from .models import usuarios, marcas, productos
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
import os
from django.conf import settings    
from django.core.files.base import ContentFile
from pathlib import Path
from django.http import JsonResponse
from django.contrib import messages

def navbarproductos(request):
    if request.method == 'GET':
        return render(request, 'navbarproductos.html')

def ver(request):
    if request.method == 'GET':
        productos_ver = productos.objects.filter(estado='1', stock__gt=0)
        productos_con_imagen = []
        for producto in productos_ver:
            if producto.imagen and hasattr(producto.imagen, 'path'):  # Verifica si producto.imagen es válido y tiene el atributo 'path'
                imagen_path = os.path.join(settings.MEDIA_ROOT, str(producto.imagen.path))
                print("producto.imagen.path: ",producto.imagen.path)
                if os.path.exists(imagen_path):
                    producto.imagen_url = os.path.join(settings.MEDIA_URL, producto.imagen)
                    print("producto.imagen_url: ",producto.imagen_url)
                else:
                    producto.imagen_url = None
            else:
                producto.imagen_url = None  # Si producto.imagen no es válido, establece None
            productos_con_imagen.append(producto)
        
        variables = {'request': request, 'productos': productos_con_imagen}
        return render(request, 'ver_producto.html', variables)


def buscar_productos(request):
    query = request.GET.get('q', '')
    productos_ver = productos.objects.filter(descripcion__icontains=query)
    productos_data = []
    for producto in productos_ver:
        productos_data.append({
            'descripcion': producto.descripcion,
            'marca': producto.marca.descripcion,
            'stock': producto.stock,
            'precio_total': producto.precio_total,
            'cantidad_cuotas': producto.cantidad_cuotas,
            'precio_cuota': producto.precio_cuota,
            'imagen_url': os.path.join(settings.MEDIA_URL, str(producto.imagen)) if producto.imagen else None,
        })
    return JsonResponse(productos_data, safe=False)


def detalle(request, id): #Verificar si producto detalle funciona 
    producto = get_object_or_404(productos, pk=id)
    n_marcas = marcas.objects.all()
    print("Id del producto",producto)
    if request.method == 'GET':
        productos_ver = producto
        productos_con_imagen = []
        if request.session['rol']:
            rol = request.session['rol']
            for producto in productos_ver:
                if producto.imagen and hasattr(producto.imagen, 'path'):  # Verifica si producto.imagen es válido y tiene el atributo 'path'
                    imagen_path = os.path.join(settings.MEDIA_ROOT, str(producto.imagen.path))
                    if os.path.exists(imagen_path):
                        producto.imagen_url = os.path.join(settings.MEDIA_URL, producto.imagen.name)
                    else:
                        producto.imagen_url = None
                else:
                    producto.imagen_url = None  # Si producto.imagen no es válido, establece None
                productos_con_imagen.append(producto)
                rol = request.session.get('rol')
            context = {
                'contex': productos_con_imagen,
                'rol': rol,
            }
            return render(request, 'producto_ver.html', context)
        else: return render(request, 'acceder.html', {'m_error': 'Inicie sesión'})

def nuevo(request):
    print("Ingresa a def nuevo")
    if request.method == 'GET':
        print("Ingresa a GET nueproducto")
        n_marcas= marcas.objects.all()  
        variables = {'request': request, 'n_marcas': n_marcas}
        print("variables: ",variables)
        return render(request, 'producto_nuevo.html', variables)
        print("Luego del return")

    elif request.method == 'POST':
        print("Ingresa POST")
        print("request.POST.get('marca'): ",request.POST.get('marca'))
        f_descripcion = request.POST.get('descripcion')
        f_stock = request.POST.get('stock')
        f_precio_total = request.POST.get('precio_total')
        f_cantidad_cuotas = request.POST.get('cantidad_cuotas')
        print("f_precio_total: ",f_precio_total, "f_cantidad_cuotas: ",f_cantidad_cuotas)
        f_precio_cuota = int(f_precio_total)/int(f_cantidad_cuotas)
        f_marca = request.POST.get('marca')
        f_imagen = request.FILES.get('imagen')

        if f_imagen:
            print("if imagen")
            # Guardar la imagen en el sistema de archivos
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'imagenes', f_imagen.name)
            with open(ruta_imagen, 'wb+') as destination:
                for chunk in f_imagen.chunks():
                    destination.write(chunk)
            print("f_imagen: ",f_imagen)
            print("f_imagen.name: ",f_imagen.name)
            # Obtener la instancia de marca
            id_marca = marcas.objects.get(id=f_marca)

            # Crear y guardar el nuevo producto
            nuevoproducto = productos(
                descripcion=f_descripcion,
                stock=f_stock,
                precio_total=f_precio_total,
                cantidad_cuotas=f_cantidad_cuotas,
                precio_cuota=f_precio_cuota,
                marca=id_marca,
                imagen=f_imagen,  # Guardar el nombre de la imagen en el modelo
                estado='1'
            )
            nuevoproducto.save()
            print("Luego de nuevo producto.save")
            messages.success(request, 'Producto agregado.')
            return redirect('verproductos')
        else:
            return render(request, 'producto_nuevo.html', {'error': 'Debe proporcionar una imagen'})

def borrar(request, id):
    para_borrar = productos.objects.get(pk=id)
    para_borrar.delete()
    return redirect('verproductos')


def modificar(request, id):
    producto = get_object_or_404(productos, pk=id)
    n_marcas = marcas.objects.all()
    print("Id del producto",producto)
    print("request.method: ",request.method)
    # Si se envió un formulario con datos para actualizar el usuario
    if request.method == 'POST':
        f_descripcion = request.POST.get('descripcion')
        f_stock = request.POST.get('stock')
        f_precio_total = request.POST.get('precio_total')
        f_cantidad_cuotas = request.POST.get('cantidad_cuotas')
        f_precio_cuota = request.POST.get('precio_cuota')
        f_imagen = request.FILES.get('imagen')
        f_marca_id = request.POST.get('marca')
        
        print("Current imagen value:", producto.imagen)
        # Eliminar la imagen anterior si existe y se ha proporcionado una nueva imagen
        if f_imagen:
            if producto.imagen :
                ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, str(producto.imagen))
                print("Ruta de la imagen anterior:", ruta_imagen_anterior)
                if os.path.exists(ruta_imagen_anterior):
                    os.remove(ruta_imagen_anterior)
                    print(f"Imagen anterior eliminada: {ruta_imagen_anterior}")

                ruta_imagen = 'imagenes/' + f_imagen.name
                ruta_imagen_completa = os.path.join(settings.MEDIA_ROOT, ruta_imagen)
                print("ruta_imagen_completa: ",ruta_imagen_completa)
                print(ruta_imagen_completa)
                with open(ruta_imagen_completa, 'wb+') as destination:
                    for chunk in f_imagen.chunks():
                        destination.write(chunk)
                producto.imagen = f_imagen
        producto.descripcion = f_descripcion
        producto.stock = f_stock
        producto.precio_total = f_precio_total
        producto.cantidad_cuotas = f_cantidad_cuotas
        producto.precio_cuota = f_precio_cuota
        producto.marca = get_object_or_404(marcas, pk=f_marca_id)
        producto.save()

        return redirect('verproductos')
    else: 
        print("else")
        return render(request, 'producto_editar.html', {'producto': producto, 'n_marcas': n_marcas})
 
def desactivar(request, id):
    producto = get_object_or_404(productos, pk=id)
    print("Id del producto",producto)
    print("request.method: ",request.method)
    if request.method == 'GET':
        if producto.estado == '1':
            producto.estado = '0'
            producto.save()
            messages.success(request, 'Producto desactivado exitosamente.')
            return redirect('verproductos')
        else: 
            if producto.estado == '0':
                messages.success(request, 'No es posible desactivar. El producto ya está desactivado.')
                return redirect('verproductos')
    else: 
        print("else")
        return redirect('verproductos')