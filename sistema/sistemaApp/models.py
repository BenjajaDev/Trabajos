from django.db import models

from mongoengine import Document, StringField, FloatField, IntField

class Producto(Document):
    codigo = StringField(required=True)
    nombre = StringField(required=True)
    precio = FloatField(required=True)
    stock = IntField(required=True)


class Movimientos(Document):
    codigo = StringField(required=True)
    tipo = StringField(choices=['entrada', 'salida'], required=True)
    cantidad = IntField(required=True) #Cantidad ingresada
    producto = StringField(required=True)
    fecha = StringField(required=True)
    descripcion = StringField()

    