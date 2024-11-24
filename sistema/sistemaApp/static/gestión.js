async function cargarMovimientos() {
    const response = await fetch("/movimientos/");
    const movimientos = await response.json();
    const tabla = document.getElementById("movimientosTabla");
    tabla.innerHTML = "";
    movimientos.forEach(mov => {
        const fila = `<tr>
            <td>${mov.producto_codigo}</td>
            <td>${mov.tipo}</td>
            <td>${mov.cantidad}</td>
            <td>${mov.fecha}</td>
            <td>${mov.descripcion || "Sin descripción"}</td>
        </tr>`;
        tabla.innerHTML += fila;
    });
}

document.getElementById("movimientoForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = {
        producto_codigo: document.getElementById("producto_codigo").value,
        tipo: document.getElementById("tipo").value,
        cantidad: parseInt(document.getElementById("cantidad").value),
        descripcion: document.getElementById("descripcion").value
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