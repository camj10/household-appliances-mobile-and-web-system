from django.shortcuts import render, redirect, get_object_or_404
from .models import usuarios, marcas

def ver(request):
    if request.method=='GET':
        if 'rol' in request.session:
            if request.session['rol']=='1':
                lista=marcas.objects.all()
                variables={}
                variables['request']=request
                variables['lista']=lista
                return render(request, 'marca_ver.html', variables)
            else:
                variables={}
                variables['m_error']='No tiene permisos para acceder al módulo de marcas'
                variables['nombre_usuario']= request.session['nombre_usuario']
                return render(request,'panel.html', variables)
        else:
            return redirect('acceder')
    
def nuevo(request):
    if request.method=='GET':
        return render(request, 'marca_nueva.html')
    
    if request.method=='POST':
        f_marca=request.POST.get('marca')
        nuevamarca=marcas(
            marca=f_marca
        )        
        nuevamarca.save()
        return redirect ('vermarca')
    
def modificar(request, id):
    marca_modificar = get_object_or_404(marcas, pk=id)
    if request.method=='POST':    
        marca_modificar.marca = request.POST.get('marca')

        marca_modificar.save()
        return redirect('vermarca')
    return render(request,'marca_editar.html', {'marca_modificar':marca_modificar})
    
def borrar(request, id):
    para_borrar=marcas.objects.get(pk=id)
    para_borrar.delete()
    return redirect ('vermarca')