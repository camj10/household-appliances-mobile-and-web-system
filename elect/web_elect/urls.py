from django.urls import path
from . import inicio, usuarios, views, pedidos, cuotas, marcas, productos
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

print("URLS.PY DE WEB")
urlpatterns = [
    path('status/', views.status_check, name='status_check'),
    path('', views.inicio, name=''),



     path('login/', views.login_view, name='login'),

     path('logout/', views.logout_view, name='logout'),
     path('register/', views.register, name='register'),
     path('verusuarios/', views.verusuarios, name='verusuarios'),
     path('hello_world/', views.hello_world, name='hello_world'),
     path('inicio/', views.inicio, name='inicio'),
     
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Movil
    path('clogin', views.login_c, name='clogin'),
    path('csrf-token/', views.get_csrf_token, name='csrf-token'),
    path('clogout/', views.logout_c, name='clogout'),

    #Usuarios
    # path('verusuario', usuarios.ver, name='verusuario'),
    # path('nueusuario', usuarios.nuevo, name='nueusuario'),
    # path('modusuario/<id>', usuarios.modificar, name='modusuario'),
    # path('borusuario/<id>', usuarios.borrar, name='borusuario'),
    # path('listausuarios', views.UsuariosAPILista.as_view(), name='listausuarios'),
    # # Acceder - salir
    # path('acceder', inicio.acceder, name='acceder'),
    # path('salir', inicio.salir, name='salir'),

    #Pedidos
    path('listapedidos', views.PedidosAPILista.as_view(), name='listapedidos'),
    path('detallepedido/<int:id>', views.PedidosAPIModificar.as_view(), name='detallepedido'),
    path('verpedido', pedidos.ver, name='verpedido'),
    path('pedidospendientes/', pedidos.verPendientes, name='pedidospendientes'),
    path('pedidosaprobados/', pedidos.verAprobados, name='pedidosaprobados'),
    path('aprobarpedido/<int:pedido_id>/', pedidos.aprobar, name='aprobarpedido'),
    path('desaprobarpedido/<int:pedido_id>/', pedidos.desaprobar, name='desaprobarpedido'),
    path('veraprobadosfecha/', pedidos.verAprobadosFecha, name='veraprobadosfecha'),
    #Movil
    path('crearpedido/', views.create_order, name='crearpedido'),
    path('pedidos/', pedidos.pedidosusuario, name='pedidos'),
    # path('nuepedido', pedidos.nuevo, name='nuepedido'),
    # path('modpedido/<int:id>', pedidos.modificar, name='modpedido'),
    # path('borpedido/<id>', pedidos.borrar, name='borpedido'),


    #Cuotas
    path('listacuotas', views.CuotasAPILista.as_view(), name='listacuotas'),
    path('borrarcuota/<int:id>', views.CuotasAPIBorrar.as_view(), name='borrarcuota'),
    path('modcuota/<int:id>', views.CuotasAPIModificar.as_view(), name='modcuota'),
    path('nuevacuota', views.CuotasAPINuevo.as_view(), name='nuevacuota'),
    path('vercuota', cuotas.ver, name='vercuota'),
    path('nuecuota', cuotas.nuevo, name='nuecuota'),
    path('modcuota/<id>', cuotas.modificar, name='modcuota'),
    path('borcuota/<id>', cuotas.borrar, name='borcuota'),


    path('vercuotas/<int:pedido_id>/', cuotas.vercuotas, name='vercuotas'), 
    path('pagarcuota/<int:cuota_id>/', cuotas.pagarcuota, name='pagarcuota'),
    #Movi
    path('estadocuenta/', cuotas.ver_estado_cuenta, name='verestadocuenta'),

    #Productos
    path('navbarproductos', productos.navbarproductos, name='navbarproductos'),
    path('verproductos/', productos.ver, name='verproductos'),
    path('buscar_productos/', productos.buscar_productos, name='buscar_productos'),
    path('detproducto/<id>', productos.detalle, name='detproducto'),
    path('nueproducto', productos.nuevo, name='nueproducto'),
    path('modproducto/<id>', productos.modificar, name='modproducto'),
    path('borproducto/<id>', productos.desactivar, name='borproducto'),
    #Movil
    path('nuevoproducto', views.ProductosAPINuevo.as_view(), name='nuevoproducto'),
    path('listaproductos', views.get_products, name='listaproductos'),
    path('listaproductos/', views.lista_productos, name='lista_productos'),
    path('detalleproducto/<int:id>/', views.product_detail_view, name='detalleproducto'),


    #Marcas
    path('listamarcas', marcas.ver, name='listamarcas'),
    path('nuevamarca', marcas.nuevo, name='nuevamarca'),
    path('modificarmarca/<int:id>', marcas.modificar, name='modificarmarca'),
    path('borrarmarca/<int:id>', marcas.borrar, name='borrarmarca'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)