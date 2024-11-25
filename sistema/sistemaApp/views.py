from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sistemaApp.models import Producto
from sistemaApp.models import Movimientos
from datetime import datetime
from bson import json_util
import json


def indexhtml(request):
    return render(request, 'index.html')

def productoshtml(request):
    return render(request, 'productos.html')

def movimientoshtml(request):
    return render(request, 'movimientos.html')

def gestionhtml(request):
    return render(request, 'gestion.html')

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
def registrar_movimiento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            producto = Producto.objects(codigo=data['producto_codigo']).first()

            if not producto:
                return JsonResponse({'error': 'Producto no encontrado'}, status=404)

            movimiento = Movimientos(
                producto_codigo=data['producto_codigo'],
                tipo=data['tipo'],
                cantidad=data['cantidad'],
                descripcion=data.get('descripcion', ''),
                fecha=datetime.utcnow()
            )
            movimiento.save()

            # Actualizar el stock del producto
            if data['tipo'] == 'entrada':
                producto.update(inc__stock=data['cantidad'])
            elif data['tipo'] == 'salida':
                if producto.stock < data['cantidad']:
                    return JsonResponse({'error': 'Stock insuficiente'}, status=400)
                producto.update(dec__stock=data['cantidad'])

            return JsonResponse({'mensaje': 'Movimiento registrado exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def listar_movimientos(request):
    if request.method == "GET":
        movimientos = Movimientos.objects()
        movimientos_json = [
            {
                "producto_codigo": m.producto_codigo,
                "tipo": m.tipo,
                "cantidad": m.cantidad,
                "fecha": m.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "descripcion": m.descripcion
            }
            for m in movimientos
        ]
        return JsonResponse(movimientos_json, safe=False)