from django.db import models
from mongoengine import Document, StringField, IntField, DateField

class Producto(Document):
    #modelo que representa un producto en el inventario
    codigo = StringField(required=True)
    nombre = StringField(required=True)
    precio = IntField(required=True)
    stock = IntField(required=True)


class Movimientos(Document):
    #modelo que representa un movimiento de inventario
    codigo = StringField(required=True)
    tipo = StringField(choices=['entrada', 'salida'], required=True)
    cantidad = IntField(required=True) #Cantidad ingresada
    producto = StringField(required=True)
    fecha = DateField(required=True)
    descripcion = StringField()

    