const baseUrl = window.location.origin;
async function cargarMovimientos() {
    const response = await fetch(`${baseUrl}/movimientos/listar`);
    const movimientos = await response.json();
    const tabla = document.getElementById("movimientosTabla");
    tabla.innerHTML = "";
    movimientos.forEach(mov => {
        const fila = `<tr>
            <td>${mov.codigo}</td>
            <td>${mov.producto}</td>
            <td>${mov.tipo}</td>
            <td>${mov.cantidad}</td>
            <td>${mov.fecha}</td>
            <td>${mov.descripcion || "Sin descripción"}</td>
             <td>
                    <button class="btn btn-danger btn-sm" onclick="eliminar_movimiento('${mov.codigo}')">Eliminar</button>
                </td>
        </tr>`;
        tabla.innerHTML += fila;
    });
}
cargarMovimientos();

async function cargarProductos() {
    const response = await fetch("/productos/listar");
    const productos = await response.json();
    const selector = document.getElementById("producto_codigo");
    selector.innerHTML = '<option selected disabled>Seleccione un producto</option>';
    productos.forEach(prod => {
        const opcion = `<option value="${prod.codigo}">${prod.nombre}</option>`;
        selector.innerHTML += opcion;
    });
}

// Llamar a la función al cargar la página
cargarProductos();


document.getElementById("movimientoForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = {
        producto_codigo: document.getElementById("producto_codigo").value,
        tipo: document.getElementById("tipo").value,
        cantidad: parseInt(document.getElementById("cantidad").value),
        descripcion: document.getElementById("descripcion").value,
        fecha: document.getElementById("fecha").value
    };

    const response = await fetch("/movimientos/registrar/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert("Movimiento registrado exitosamente");
        cargarMovimientos();
        event.target.reset();
    } else {
        const error = await response.json();
        alert("Error: " + error.error);
    }
});

cargarMovimientos();

async function eliminar_movimiento(codigo) {
    if (confirm("¿Estás seguro de eliminar este movimiento?")) {
        const response = await fetch(`/movimientos/eliminar/${codigo}/`, {
            method: "DELETE",
        });
        alert((await response.json()).mensaje);
        cargarMovimientos(); // Recargar tabla
    }
}