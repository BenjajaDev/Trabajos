

/* Obtener productos */

async function cargarProductos() {
    try {
        const response = await fetch("/productos/");
        const productos = await response.json();

        const tabla = document.querySelector("#productosTabla tbody");
        tabla.innerHTML = ""; // Limpia la tabla antes de cargar los datos

        productos.forEach((producto) => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${producto.codigo}</td>
                <td>${producto.nombre}</td>
                <td>${producto.precio.toFixed(2)}</td>
                <td>${producto.stock}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editarProducto('${producto.codigo}')">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="eliminarProducto('${producto.codigo}')">Eliminar</button>
                </td>
            `;
            tabla.appendChild(fila);
        });
    } catch (error) {
        console.error("Error al cargar los productos:", error);
    }
}

cargarProductos();


/* Crear o actualizar */

document.querySelector("#productoForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const operacion = document.getElementById("operacion").value;
    const codigo = document.getElementById("codigo").value;
    const data = {
        nombre: document.getElementById("nombre").value,
        precio: parseFloat(document.getElementById("precio").value),
        stock: parseInt(document.getElementById("stock").value),
    };

    if (operacion === "crear") {
        // Crear producto
        data.codigo = codigo; // Añadir código para crear
        const response = await fetch("/productos/crear/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        //Limpiar formulario
        document.getElementById("codigo").value = "";
        document.getElementById("nombre").value = "";
        document.getElementById("precio").value = "";
        document.getElementById("stock").value = "";
        alert((await response.json()).mensaje);
    } else if (operacion === "actualizar") {
        // Actualizar producto
        const response = await fetch(`/productos/actualizar/${codigo}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        document.getElementById("codigo").value = "";
        document.getElementById("nombre").value = "";
        document.getElementById("precio").value = "";
        document.getElementById("stock").value = "";
        alert((await response.json()).mensaje);
    }

    document.getElementById("operacion").value = "crear"; // Resetear formulario
    cargarProductos(); // Recargar tabla
    event.target.reset();
});

/* Eliminar producto */

async function eliminarProducto(codigo) {
    if (confirm("¿Estás seguro de eliminar este producto?")) {
        const response = await fetch(`/productos/eliminar/${codigo}/`, {
            method: "DELETE",
        });
        alert((await response.json()).mensaje);
        cargarProductos(); // Recargar tabla
    }
}

/* Editar producto */

async function editarProducto(codigo_producto) {
    const response = await fetch("/productos/");
    const productos = await response.json();
    const producto = productos.find((p) => p.codigo === codigo_producto);

    if (producto) {
        document.getElementById("codigo").value = producto.codigo;
        document.getElementById("nombre").value = producto.nombre;
        document.getElementById("precio").value = producto.precio;
        document.getElementById("stock").value = producto.stock;

        document.getElementById("operacion").value = "actualizar"; // Cambiar a operación de actualizar
    }
}

const limpiarFormulario = () => {
    document.getElementById("codigo").value = "";
    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("stock").value = "";
}
