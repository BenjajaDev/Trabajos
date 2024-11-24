from pymongo import MongoClient
from datetime import datetime
client = MongoClient('mongodb://localhost:27017/')
db = client["inventario"]

productos = [
    {"codigo": "ff100", "nombre_producto": "Papas pre-fritas 1kg", "precio_unitario": 4000,
     "categoría": "congelados", "stock": 20},
    {"codigo": "ff101", "nombre_producto": "Hamburguesas King 200gr", "precio_unitario": 800,
     "categoría": "congelados", "stock": 15},
    {"codigo": "ff102", "nombre_producto": "Yogur Soprole 120gr", "precio_unitario": 270,
     "categoría": "lacteos", "stock": 40},
    {"codigo": "ff103", "nombre_producto": "Yogur Nestlé 130gr", "precio_unitario": 210,
     "categoría": "lacteos", "stock": 25},
    {"codigo": "ff104", "nombre_producto": "Atún lomito 120gr", "precio_unitario": 1200,
     "categoría": "conservas", "stock": 20},
    
]

movimientos = [
    {"codigo_movimiento": "mov1", "codigo_producto": "ff100", "tipo": "salida", "cantidad": 3, "fecha": datetime.now(),
     "motivo": "Venta/Reposición"},
    {"codigo_movimiento": "mov2", "codigo_producto": "ff101", "tipo": "entrada", "cantidad": 10,
     "fecha": datetime.now(), "motivo": "Compra/Recepción"},
    {"codigo_movimiento": "mov3", "codigo_producto": "ff102", "tipo": "salida", "cantidad": 2, "fecha": datetime.now(),
     "motivo": "Venta/Reposición"},
    {"codigo_movimiento": "mov4", "codigo_producto": "ff103", "tipo": "salida", "cantidad": 5, "fecha": datetime.now(),
     "motivo": "Venta/Reposición"},
    {"codigo_movimiento": "mov5", "codigo_producto": "ff104", "tipo": "salida", "cantidad": 4, "fecha": datetime.now(),
     "motivo": "Venta/Reposición"}
]

#db.productos.insert_many(productos)
#db.movimientos.insert_many(movimientos)

#db.productos.insert_one({"codigo": "ff105", "nombre_producto": "Duraznos en conservas 1kg", "precio_unitario": 3590, "categoría": "conservas", "stock": 8})

def obtener_movimientos_por_tipo():
    pipeline_cantidad_movimientos = [
    {
        "$group": {
            "_id": "$tipo",
            "total_movimientos": {"$sum": "$cantidad"}
        }
    }
    ]

    result = db.movimientos.aggregate(pipeline_cantidad_movimientos)

    print("\nCantidad de movimientos según el tipo: ")
    for doc in result:
        print(doc)


def obtener_productos_bajo_stock():
    pipeline_productos_bajo_stock = [
    {
        "$match": {
            "stock": {"$lt": 10}
        }
        },
    {
        "$project": {
            "_id": 0,
            "codigo": 1,
            "nombre_producto": 1,
            "stock": 1
            }
        }   
    ]

    result = db.productos.aggregate(pipeline_productos_bajo_stock)

    print("\nProductos bajo stock: ")
    for doc in result:
        print(doc)


def obtener_stock_por_categoria():
    pipeline_stock_por_categoria = [
    {
        "$group": {
            "_id": "$categoría",
            "total_stock": {"$sum": "$stock"}
        }
    }
    ]

    result = db.productos.aggregate(pipeline_stock_por_categoria)

    print("\nStock por categoría: ")
    for doc in result:
        print(doc)

def obtener_precio_promedio():
    pipeline_precio_promedio = [
    {
        "$group": {
            "_id": "$categoría",
            "precio_promedio": {"$avg": "$precio_unitario"}
        }},
    { "$sort": {"precio_promedio": -1}
       
    }
    ]

    result = db.productos.aggregate(pipeline_precio_promedio)

    print("\nPrecio promedio por categoría: ")
    for doc in result:
        print(doc)
        
        
obtener_movimientos_por_tipo()     
obtener_productos_bajo_stock()
obtener_stock_por_categoria()
obtener_precio_promedio()
    
    