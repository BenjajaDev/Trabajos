from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sistemaApp.models import Producto
from sistemaApp.models import Movimientos
from sistemaApp.pipelines import obtener_productos_mas_vendidos_por_mes, obtener_total_movimientos_por_tipo, obtener_stock_actual_productos, obtener_productos_bajo_stock
import datetime
from bson import json_util
import random
import json


def indexhtml(request):
    return render(request, 'index.html')

def productoshtml(request):
    return render(request, 'productos.html')

def movimientoshtml(request):
    return render(request, 'movimientos.html')

def gestionhtml(request):
    return render(request, 'gestion.html')

def reporteshtml(request):
    return render(request, 'reportes.html')

@csrf_exempt
def crear_producto(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            producto = Producto(
                codigo=data['codigo'],
                nombre=data['nombre'],
                precio=data['precio'],
                stock=data['stock']
            )
            producto.save()
            return JsonResponse({'mensaje': 'Producto creado exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': f"Error al crear producto: {str(e)}"}, status=400)


@csrf_exempt
def listar_productos(request):
    if request.method == "GET":
        productos = Producto.objects()
        productos_json = [
            {
                "codigo": str(p.codigo),
                "nombre": str(p.nombre),
                "precio": float(p.precio),
                "stock": int(p.stock),
            }
            for p in productos
        ]
        return JsonResponse(productos_json, safe=False)

@csrf_exempt
def actualizar_producto(request, codigo_producto):
    if request.method == "PUT":
        data = json.loads(request.body)
        producto = Producto.objects(codigo=codigo_producto).first()
        if producto:
            producto.update(
                nombre=data.get('nombre', producto.nombre),
                precio=data.get('precio', producto.precio),
                stock=data.get('stock', producto.stock),
            )
            return JsonResponse({'mensaje': 'Producto actualizado correctamente'}, status=200)
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


@csrf_exempt
def eliminar_producto(request, codigo_producto):
    if request.method == "DELETE":
        producto = Producto.objects(codigo=codigo_producto).first()
        if producto:
            producto.delete()
            return JsonResponse({'mensaje': 'Producto eliminado correctamente'}, status=200)
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reporte_productos_mas_vendidos_por_mes(request):
    if request.method == "GET":
        resultados = obtener_productos_mas_vendidos_por_mes()
        return JsonResponse(resultados, safe=False)

@csrf_exempt
def reporte_total_movimientos_por_tipo(request):
    if request.method == "GET":
        resultados = obtener_total_movimientos_por_tipo()
        return JsonResponse(resultados, safe=False)
@csrf_exempt
def reporte_productos_bajo_stock(request):
    if request.method == "GET":
        resultados = obtener_productos_bajo_stock()
        return JsonResponse(resultados, safe=False)

@csrf_exempt
def reporte_stock_actual_productos(request):
    if request.method == "GET":
        resultados = obtener_stock_actual_productos()
        return JsonResponse(resultados, safe=False)
@csrf_exempt
def listar_movimientos(request):
    if request.method == "GET":
        movimientos = Movimientos.objects()
        movimientos_json = [
            {
                "codigo": str(m.codigo),
                "tipo": str(m.tipo),
                "cantidad": int(m.cantidad),
                "producto": str(m.producto),
                "fecha": str(m.fecha),
                "descripcion": str(m.descripcion),
            }
            for m in movimientos
        ]
        return JsonResponse(movimientos_json, safe=False)

@csrf_exempt
def registrar_movimiento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            codigo = str(random.randint(1000, 9999))  # Generar un codigo aleatorio
            producto = str(data.get("producto_codigo"))
            tipo = data.get("tipo").lower()
            cantidad = data.get("cantidad")
            descripcion = data.get("descripcion")
            fecha = data.get("fecha")
            # Verificar que el producto existe
            producto = Producto.objects.filter(codigo=producto).first()
            if tipo == "entrada" and producto:
                producto.stock += cantidad
                producto.save()
                print("Se le han ingresado: "+str(cantidad)+" unidades al producto: "+str(producto.nombre))
    
    # Crear el movimiento
            movimiento = Movimientos(
                codigo=codigo,
                producto=producto.nombre,
                tipo=tipo,
                cantidad=cantidad,
                descripcion=descripcion,
                fecha=fecha
            )
            movimiento.save()  # Guardar el movimiento

            return JsonResponse({'mensaje': 'Se registró el movimiento'}, status=200)
        
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_movimiento(request, codigo_movimiento):
    if request.method == "DELETE":
        Movimiento = Movimientos.objects(codigo=codigo_movimiento).first()
        if Movimiento:
            Movimiento.delete();
            return JsonResponse({'mensaje': 'Movimiento eliminado correctamente'}, status=200)
        return JsonResponse({'error': 'Movimiento no encontrado'}, status=404)