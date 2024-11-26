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
    #renderiza la página principal del sistema
    #request: El objeto de solicitud HTTP
    #httpResponse: La página de inicio renderizada
    return render(request, 'index.html')

    #renderiza las vistas de la página
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
    #crea un nuevo producto en la base de datos
    #request: El objeto de solicitud HTTP que contiene los datos del producto
    #jsonResponse: Mensaje de éxito o error
    if request.method == "POST":
        try:
            data = json.loads(request.body)  #carga los datos del producto desde el cuerpo de la solicitud
            producto = Producto(
                codigo=data['codigo'],  #código del producto
                nombre=data['nombre'],  #nombre del producto
                precio=data['precio'],  #precio del producto
                stock=data['stock']  #stock del producto
            )
            producto.save()  #guarda el nuevo producto en la base de datos
            return JsonResponse({'mensaje': 'Producto creado exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': f"Error al crear producto: {str(e)}"}, status=400)


@csrf_exempt
def listar_productos(request):
    #lista todos los productos en la base de datos por el metodo get
    if request.method == "GET":
        productos = Producto.objects()  #obtiene todos los productos
        productos_json = [
            {
                "codigo": str(p.codigo),  #convierte el código del producto a cadena
                "nombre": str(p.nombre), 
                "precio": float(p.precio),  #convierte el precio a float
                "stock": int(p.stock),  #convierte el stock a entero
            }
            for p in productos
        ]
        return JsonResponse(productos_json, safe=False)


@csrf_exempt
def actualizar_producto(request, codigo_producto):
    #actualiza un producto existente en la base de datos
    #request: El objeto de solicitud HTTP que contiene los nuevos datos del producto
    if request.method == "PUT":
        data = json.loads(request.body)  #carga los nuevos datos del producto
        producto = Producto.objects(codigo=codigo_producto).first()
        if producto:
            producto.update(
                #actualiza los atributos si se proporcionan
                nombre=data.get('nombre', producto.nombre),
                precio=data.get('precio', producto.precio),
                stock=data.get('stock', producto.stock),
            )
            return JsonResponse({'mensaje': 'Producto actualizado correctamente'}, status=200)
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


@csrf_exempt
def eliminar_producto(request, codigo_producto):
    if request.method == "DELETE":
        producto = Producto.objects(codigo=codigo_producto).first() #busca el producto por código
        if producto:
            producto.delete() #elimina el producto
            return JsonResponse({'mensaje': 'Producto eliminado correctamente'}, status=200)
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def index(request):
    #renderiza la página principal del sistema
    return render(request, 'index.html')

@csrf_exempt
def reporte_productos_mas_vendidos_por_mes(request):
    if request.method == "GET":
        resultados = obtener_productos_mas_vendidos_por_mes() #obtiene los resultados de los productos más vendidos por mes
        return JsonResponse(resultados, safe=False)

@csrf_exempt
def reporte_total_movimientos_por_tipo(request):
    if request.method == "GET":
        resultados = obtener_total_movimientos_por_tipo() #obtiene los resultados de los movimientos por tipo
        return JsonResponse(resultados, safe=False)
@csrf_exempt
def reporte_productos_bajo_stock(request):
    if request.method == "GET":
        resultados = obtener_productos_bajo_stock() #obtiene los resultados de productos bajo stock
        return JsonResponse(resultados, safe=False)

@csrf_exempt
def reporte_stock_actual_productos(request):
    if request.method == "GET":
        resultados = obtener_stock_actual_productos() #obtiene los resultados del stock actual de productos
        return JsonResponse(resultados, safe=False)
@csrf_exempt
def listar_movimientos(request):
    if request.method == "GET":
        movimientos = Movimientos.objects()
        movimientos_json = [
            {
                #conversiones
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
            data = json.loads(request.body) #carga los datos del movimiento desde el cuerpo de la solicitud
            codigo = str(random.randint(1000, 9999))  #generar un codigo aleatorio
            producto = str(data.get("producto_codigo"))  #obtiene el código del producto
            tipo = data.get("tipo").lower() #obtiene el tipo de movimiento y lo convierte a minúsculas
            cantidad = data.get("cantidad") #obtiene la cantidad del movimiento
            descripcion = data.get("descripcion")
            fecha = data.get("fecha")
            #verificar que el producto existe
            producto = Producto.objects.filter(codigo=producto).first() #busca el producto por código
            if tipo == "entrada" and producto: #si es una entrada y el producto existe:
                producto.stock += cantidad #incrementa el stock del producto
                producto.save() #guarda el producto actualizado
                print("Se le han ingresado: "+str(cantidad)+" unidades al producto: "+str(producto.nombre))
    
    #crea el movimiento
            movimiento = Movimientos(
                codigo=codigo,
                producto=producto.nombre,
                tipo=tipo,
                cantidad=cantidad,
                descripcion=descripcion,
                fecha=fecha
            )
            movimiento.save()  #Guardar el movimiento

            return JsonResponse({'mensaje': 'Se registró el movimiento'}, status=200)
        
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_movimiento(request, codigo_movimiento):
    if request.method == "DELETE":
        Movimiento = Movimientos.objects(codigo=codigo_movimiento).first() #busca el movimiento por código
        if Movimiento:
            Movimiento.delete(); #elimina el movimiento
            return JsonResponse({'mensaje': 'Movimiento eliminado correctamente'}, status=200)
        return JsonResponse({'error': 'Movimiento no encontrado'}, status=404)