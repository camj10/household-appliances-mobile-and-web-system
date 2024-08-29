# from django.shortcuts import render, redirect, get_object_or_404
# # from .models import usuarios, grupos

# def ver(request):
#     if request.method=='GET':
#         if 'nivel_usuario' in request.session:
#             if request.session['nivel_usuario']=='ADMINISTRADOR':
#                 lista=grupos.objects.all()
#                 variables={}
#                 variables['request']=request
#                 variables['lista']=lista
#                 return render(request, 'grupo_ver.html', variables)
#             else:
#                 variables={}
#                 variables['m_error']='No tiene permisos para acceder al módulo de grupos'
#                 variables['nombre_usuario']= request.session['nombre_usuario']
#                 return render(request,'panel.html', variables)
#         else:
#             return redirect('acceder')
    
# def nuevo(request):
#     if request.method=='GET':
#         return render(request, 'grupo_nuevo.html')
    
#     if request.method=='POST':
#         f_grupo=request.POST.get('grupo')
#         nuevogrupo=grupos(
#             grupo=f_grupo
#         )        
#         nuevogrupo.save()
#         return redirect ('vergrupo')
    
# def modificar(request, id):
#     grupo_modificar = get_object_or_404(grupos, pk=id)
#     if request.method=='POST':    
#         grupo_modificar.grupo = request.POST.get('grupo')

#         grupo_modificar.save()
#         return redirect('vergrupo')
#     return render(request,'grupo_editar.html', {'grupo_modificar':grupo_modificar})
    
# def borrar(request, id):
#     para_borrar=grupos.objects.get(pk=id)
#     para_borrar.delete()
#     return redirect ('vergrupo')
 