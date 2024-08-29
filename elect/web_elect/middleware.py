from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import usuarios
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import resolve
from django.contrib import messages
from django.shortcuts import redirect

# class CustomAuthMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Ignorar las rutas específicas
#         excluded_paths = ['/login/', '/register/','/api/login/']  # Agrega aquí las rutas que deseas excluir
#         current_path = request.path_info

#         if current_path in excluded_paths:
#             return None

#         auth_header = request.headers.get('Authorization')

#         if auth_header:
#             try:
#                 token = auth_header.split(' ')[1]  # Obtener el token del encabezado Authorization

#                 # Verificar el token
#                 user = self.verify_token(token)
#                 if user:
#                     request.user = user
#                 else:
#                     messages.error(request, 'Invalid token')
#                     return redirect('/login/')

#             except IndexError:
#                 messages.error(request, 'Token missing')
#                 return redirect('/login/')
#         else:
#             return messages.error(request, 'Authorization header missing')

#     def verify_token(self, token):
#         try:
#             # Implementa la lógica para verificar y decodificar tu token
#             access_token = AccessToken(token)
#             username = access_token['username']
#             user = usuarios.objects.get(username=username)
#             return user
#         except Exception:
#             return None

# middleware.py
class CustomAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ['/login/', '/register/', '/clogin','/csrf-token/','/estadocuenta/','/pedidos/','/listaproductos/','/listaproductos']  # Rutas que se excluyen
        current_path = request.path_info
        print("current_path: ",current_path) 
        if current_path in excluded_paths:
            print("current_path in excluded_paths")
            return None

        auth_header = request.headers.get('Authorization')
        print("auth_header: ",auth_header)
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Obtener el token del encabezado Authorization

                # Verificar el token
                user = self.verify_token(token)
                if user:
                    request.user = user
                else:
                    return messages.error(request, 'Invalid token')

            except IndexError:
                return messages.error(request, 'Token missing')
        else:
            return messages.error(request, 'Authorization header missing')

    def verify_token(self, token):
        try:
            # Implementa la lógica para verificar y decodificar tu token
            access_token = AccessToken(token)
            username = access_token['username']
            user = usuarios.objects.get(username=username)
            return user
        except Exception:
            return None
