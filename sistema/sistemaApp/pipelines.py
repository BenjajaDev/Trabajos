from datetime import datetime, timedelta
from sistemaApp.models import Producto, Movimientos

def obtener_productos_mas_vendidos_por_mes():
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Crear un pipeline para agrupar por mes
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$fecha"},
                    "month": {"$month": "$fecha"},
                    "producto": "$producto"
                },
                "total_vendido": {"$sum": "$cantidad"}
            }
        },
        {
            "$sort": {
                "_id.year": 1,
                "_id.month": 1,
                "total_vendido": -1
            }
        }
    ]
    
    resultados = list(Movimientos.objects.aggregate(pipeline))

    # Organizar los resultados en un diccionario
    productos_por_mes = {}
    for item in resultados:
        year = item["_id"]["year"]
        month = item["_id"]["month"]
        producto = str(item["_id"]["producto"])
        total_vendido = item["total_vendido"]

        # Crear la clave del mes (año-mes)
        mes_clave = f"{year}-{month:02d}"

        if mes_clave not in productos_por_mes:
            productos_por_mes[mes_clave] = []

        productos_por_mes[mes_clave].append({
            "producto": producto,
            "total_vendido": total_vendido
        })

    return productos_por_mes

def obtener_total_movimientos_por_tipo():
    pipeline = [
        {
            "$group": {
                "_id": "$tipo",
                "total": {"$sum": "$cantidad"}
            }
        }
    ]
    resultados = list(Movimientos.objects.aggregate(pipeline))
    return [{"codigo": str(item["_id"]), "nombre": str(item["_id"]), "stock": item["total"]} for item in resultados]

def obtener_stock_actual_productos():
    productos = Producto.objects.all()
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
    pipeline = [
        {
            "$match": {"stock": {"$lt": 20}}  # Filtra productos con stock menor a 20
        },
        {
            "$project": {  # Selecciona solo los campos especificados
                "_id": 0,  # Excluye el id del doc
                "codigo": 1,  # Incluye el código
                "nombre": 1,  # Incluye el nombre del producto
                "stock": 1  # Incluye el stock
            }
        }
    ]
    resultados = list(Producto.objects.aggregate(pipeline))
    return [{"codigo": item["codigo"], "nombre": item["nombre"], "stock": item["stock"]} for item in resultados]