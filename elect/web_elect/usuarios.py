from django.shortcuts import render, redirect, get_object_or_404
from .models import usuarios

def ver(request):
    if request.method=='GET':
        if 'nivel_usuario' in request.session:
            if request.session['nivel_usuario']=='ADMINISTRADOR':
                lista=usuarios.objects.all()
                variables={}
                variables['request']=request
                variables['lista']=lista
                return render(request, 'usuario_ver.html', variables)
            else:
                variables={}
                variables['m_error']='No tiene permisos para acceder al módulo de usuario'
                variables['nombre_usuario']= request.session['nombre_usuario']
                return render(request,'panel.html', variables)
        else: 
            return render(request, 'acceder.html', {'m_error': 'Inicie sesión'})
    
def nuevo(request):
    if request.method=='GET':
        return render(request, 'usuario_nuevo.html')
    if request.method=='POST':
        f_nombre=request.POST.get('nombre')
        f_apellido=request.POST.get('apellido')
        f_username=request.POST.get('username')
        f_password=request.POST.get('password')
        f_telefono=request.POST.get('telefono')
        f_email=request.POST.get('email')
        f_direccion=request.POST.get('direccion')
        f_rol=request.POST.get('rol')
        f_estado=request.POST.get('estado')
        nuevousuario=usuarios(
            nombre=f_nombre,
            username=f_username,
            password=f_password,
            telefono=f_telefono,
            email=f_email,
            direccion=f_direccion,
            rol=f_rol,
            estado=f_estado,
        )        
        nuevousuario.save()
        return redirect ('verusuario')
    
# def modificar(request,id):
#     print(id)
#     print("Hola")
#     if 'nivel_usuario' in request.session:
#         if request.session['nivel_usuario']=='ADMINISTRADOR':
#             print("Administrador")
#             usuario_modificar=usuarios.objects.filter(id=id).first()
#             print(usuario_modificar.nombre)
#             return render(request, 'usuario_editar.html')
#     return redirect ('verusuario')
def modificar(request, id):
    usuario_modificar = get_object_or_404(usuarios, pk=id)
    if request.method=='POST':    
        usuario_modificar.nombre = request.POST.get('nombre')
        usuario_modificar.apellido = request.POST.get('apellido')
        usuario_modificar.username = request.POST.get('username')
        usuario_modificar.password = request.POST.get('password')
        usuario_modificar.telefono = request.POST.get('telefono')
        usuario_modificar.email = request.POST.get('email')
        usuario_modificar.direccion = request.POST.get('direccion')
        usuario_modificar.rol = request.POST.get('rol')
        usuario_modificar.estado = request.POST.get('estado')

        usuario_modificar.save()
        return redirect('verusuario')
    return render(request,'usuario_editar.html', {'usuario_modificar':usuario_modificar})
    
def borrar(request, id):
    para_borrar=usuarios.objects.get(pk=id)
    para_borrar.delete()
    return redirect ('verusuario')