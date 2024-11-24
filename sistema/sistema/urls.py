
from django.contrib import admin
from django.urls import path
from sistemaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/actualizar/<str:codigo_producto>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/eliminar/<str:codigo_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('movimientos/', views.listar_movimientos, name='listar_movimientos'),
    path('movimientos/registrar/', views.registrar_movimiento, name='registrar_movimiento'),
]

