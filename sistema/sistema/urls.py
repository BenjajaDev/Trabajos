
from django.contrib import admin
from django.urls import path
from sistemaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('productos/', views.productoshtml, name='productoshtml'),
    path('productos/listar', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/actualizar/<str:codigo_producto>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/eliminar/<str:codigo_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('movimientos/', views.movimientoshtml, name='movimientoshtml'),
    path('movimientos/listar', views.listar_movimientos, name='listar_movimientos'),
    path('movimientos/registrar/', views.registrar_movimiento, name='registrar_movimiento'),
    path('movimientos/eliminar/<str:codigo_movimiento>/', views.eliminar_movimiento, name='eliminar_movimiento'),
    path('reportes/', views.reporteshtml, name='reporteshtml'),
    path('reportes/productos_mas_vendidos_por_mes/', views.reporte_productos_mas_vendidos_por_mes, name='reporte_productos_mas_vendidos_por_mes'),
    path('reportes/total_movimientos_por_tipo/', views.reporte_total_movimientos_por_tipo, name='reporte_total_movimientos_por_tipo'),
    path('reportes/stock_actual_productos/', views.reporte_stock_actual_productos, name='reporte_stock_actual_productos'),
    path('reportes/productos_bajo_stock/', views.reporte_productos_bajo_stock, name='reporte_productos_bajo_stock'),

]