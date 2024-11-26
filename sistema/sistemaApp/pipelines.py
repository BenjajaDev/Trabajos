from datetime import datetime, timedelta
from sistemaApp.models import Producto, Movimientos

def obtener_productos_mas_vendidos_por_mes():
    #obtener la fecha actual
    fecha_actual = datetime.now()

    #crear un pipeline de agregación para agrupar productos vendidos por mes y calcular el total vendido
    pipeline = [
        {
            "$group": { #agrupar por año, mes y producto
                "_id": {
                    "year": {"$year": "$fecha"},
                    "month": {"$month": "$fecha"},
                    "producto": "$producto"
                },
                "total_vendido": {"$sum": "$cantidad"} #sumar la cantidad vendida de cada producto
            }
        },
        {
            "$sort": { #ordenar resultados por año, mes y total vendido (descendente)
                "_id.year": 1,
                "_id.month": 1,
                "total_vendido": -1
            }
        }
    ]
    #ejecutar el pipeline y convertir los resultados en una lista
    resultados = list(Movimientos.objects.aggregate(pipeline))

    #organizar los resultados en un diccionario para facilitar el acceso
    productos_por_mes = {}
    for item in resultados:
        year = item["_id"]["year"]
        month = item["_id"]["month"]
        producto = str(item["_id"]["producto"])
        total_vendido = item["total_vendido"]

        #crear la clave del mes en formato año-mes
        mes_clave = f"{year}-{month:02d}"
        #si la clave del mes no existe, inicializar una lista vacía
        if mes_clave not in productos_por_mes:
            productos_por_mes[mes_clave] = []

        productos_por_mes[mes_clave].append({
            "producto": producto,
            "total_vendido": total_vendido
        })
    
    return productos_por_mes

def obtener_total_movimientos_por_tipo():
    #crear un pipeline de agregación para calcular el total de movimientos por tipo
    pipeline = [
        {
            "$group": { #agrupar movimientos por tipo
                "_id": "$tipo",
                "total": {"$sum": "$cantidad"} #sumar las cantidades de cada tipo
            }
        }
    ]
    #ejecutar el pipeline y convertir los resultados en una lista
    resultados = list(Movimientos.objects.aggregate(pipeline))
    #transformar los resultados en una lista de diccionarios con el formato deseado
    return [{"codigo": str(item["_id"]), "nombre": str(item["_id"]), "stock": item["total"]} for item in resultados]

def obtener_stock_actual_productos():
    #consultar todos los productos registrados en la base de datos
    productos = Producto.objects.all()
    #transformar los productos en una lista de diccionarios con sus atributos principales
    return [
        {
            "codigo": str(producto.codigo),
            "nombre": str(producto.nombre),
            "precio": float(producto.precio),
            "stock": int(producto.stock),
        }
        for producto in productos
    ]

def obtener_productos_bajo_stock():
    #crear un pipeline para filtrar productos con stock menor a un umbral específico
    pipeline = [
        {
            "$match": {"stock": {"$lt": 20}}  #filtra productos con stock menor a 20
        },
        {
            "$project": {  #selecciona solo los campos especificados
                "_id": 0,  #excluye el id del doc
                "codigo": 1,  #incluye el código
                "nombre": 1,  #incluye el nombre del producto
                "stock": 1  #incluye el stock
            }
        }
    ]
    #ejecutar el pipeline y convertir los resultados en una lista
    resultados = list(Producto.objects.aggregate(pipeline))
    return [{"codigo": item["codigo"], "nombre": item["nombre"], "stock": item["stock"]} for item in resultados]
