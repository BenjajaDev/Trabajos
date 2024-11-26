# Sistema de Gestión de Inventarios

## Descripción
Este proyecto es un sistema para gestionar productos y movimientos en un inventario. Permite registrar productos, realizar movimientos de entrada y salida, y generar reportes sobre el estado del inventario.

## Uso
- Para iniciar el servidor, ejecute:
  ```bash
  python manage.py runserver
  Accede a la aplicación en http://localhost:8000

## Descripción de Archivos del Proyecto

1. **models.py**
   - Define los modelos de datos utilizados en la aplicación utilizando `mongoengine`.
   - **Producto**: Representa un producto en el inventario con los siguientes atributos:
     - `codigo`: Código único del producto.
     - `nombre`: Nombre del producto.
     - `precio`: Precio del producto.
     - `stock`: Cantidad de producto disponible en inventario.
   - **Movimientos**: Representa un movimiento de inventario con los siguientes atributos:
     - `codigo`: Código único del movimiento.
     - `tipo`: Tipo de movimiento (`entrada` o `salida`).
     - `cantidad`: Cantidad de producto movido.
     - `producto`: Código del producto asociado al movimiento.
     - `fecha`: Fecha del movimiento.
     - `descripcion`: Descripción del movimiento.

2. **views.py**
   - Contiene las vistas que manejan las solicitudes HTTP y devuelven respuestas.
   - Funciones para renderizar las páginas de inicio, productos, movimientos y reportes.
   - Maneja la creación, actualización, eliminación y listado de productos y movimientos.
   - Genera reportes sobre productos más vendidos, movimientos por tipo y stock actual.

3. **gestión.js**
   - Lógica del lado del cliente para la gestión de movimientos.
   - Carga movimientos y productos desde el servidor y permite registrar nuevos movimientos.
   - Interactúa con el DOM para mostrar los datos y manejar la eliminación de movimientos.

4. **reportes.js**
   - Lógica del lado del cliente para la generación de reportes.
   - Permite obtener y mostrar diferentes reportes, como productos más vendidos por mes, movimientos por tipo, stock actual de productos y productos bajo stock.

5. **productos.js**
   - Lógica del lado del cliente para la gestión de productos.
   - Carga productos desde el servidor y permite crear, actualizar y eliminar productos.
   - Interactúa con el DOM para mostrar los datos en la interfaz de usuario.

6. **pipelines.py**
   - Contiene funciones que implementan pipelines de agregación para consultar datos en MongoDB.
   - Funciones como `obtener_productos_mas_vendidos_por_mes`, `obtener_total_movimientos_por_tipo`, `obtener_stock_actual_productos` y `obtener_productos_bajo_stock` permiten obtener información específica sobre productos y movimientos.

7. **settings.py**
   - Configuración de la aplicación Django, incluyendo la conexión a la base de datos MongoDB.
   - Define los parámetros necesarios para establecer la conexión con MongoDB utilizando `mongoengine`.

8. **templates/movimientos.html**
   - Estructura HTML para la página de movimientos.
   - Incluye formularios para registrar nuevos movimientos y una tabla para listar los movimientos existentes.

9. **templates/reportes.html**
   - Estructura HTML para la página de reportes.
   - Incluye botones para generar diferentes tipos de reportes y un área para mostrar los resultados dinámicamente.

10. **templates/productos.html**
    - Estructura HTML para la página de gestión de productos.
    - Incluye formularios para crear y actualizar productos, así como una tabla para listar los productos existentes.

11. **index.html**
    - Página principal del sistema.
    - Presenta una vista general del sistema de inventario y enlaces a las secciones de gestión de productos, movimientos y reportes.

12. **apps.py**
    - Configuración de la aplicación en Django.
    - Especifica el nombre de la aplicación y otras configuraciones necesarias para su funcionamiento.