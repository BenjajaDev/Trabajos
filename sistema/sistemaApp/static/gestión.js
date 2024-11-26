//obtiene la url base del sitio actual
const baseUrl = window.location.origin;
async function cargarMovimientos() {
    //realiza una solicitud para obtener la lista de movimientos
    const response = await fetch(`${baseUrl}/movimientos/listar`);
    //convierte la respuesta a formato json
    const movimientos = await response.json();
    //obtiene la tabla donde se mostrarán los movimientos
    const tabla = document.getElementById("movimientosTabla");
    //limpia el contenido de la tabla
    tabla.innerHTML = "";

    //itera sobre cada movimiento y crea una fila en la tabla
    movimientos.forEach(mov => {
        const fila = `<tr>
            <td>${mov.codigo}</td> //código del movimiento
            <td>${mov.producto}</td> //nombre del producto
            <td>${mov.tipo}</td> //tipo de movimiento (entrada/salida)
            <td>${mov.cantidad}</td> //cantidad de producto movido
            <td>${mov.fecha}</td> //fecha del movimiento
            <td>${mov.descripcion || "Sin descripción"}</td> //descripción del movimiento o un texto por defecto
            <td>
                    <button class="btn btn-danger btn-sm" onclick="eliminar_movimiento('${mov.codigo}')">Eliminar</button>
                </td>
        </tr>`;
        tabla.innerHTML += fila; //agrega la nueva fila a la tabla
    });
}
cargarMovimientos(); //llama a la función para cargar los movimientos al iniciar

async function cargarProductos() {
    const response = await fetch("/productos/listar");
    const productos = await response.json();
    const selector = document.getElementById("producto_codigo");
    //establece la opción por defecto en el selector
    selector.innerHTML = '<option selected disabled>Seleccione un producto</option>';
    productos.forEach(prod => { //itera sobre cada producto y crea una opción en el selector
        const opcion = `<option value="${prod.codigo}">${prod.nombre}</option>`;
        //agrega la nueva opción al selector
        selector.innerHTML += opcion;
    });
}
//llamar a la función al cargar la página
cargarProductos();

//agrega un evento para manejar el envío del formulario de movimiento
document.getElementById("movimientoForm").addEventListener("submit", async (event) => {
    event.preventDefault(); //previene el comportamiento por defecto del formulario
    const data = { //crea un objeto con los datos del formulario
        producto_codigo: document.getElementById("producto_codigo").value,
        tipo: document.getElementById("tipo").value,
        cantidad: parseInt(document.getElementById("cantidad").value),
        descripcion: document.getElementById("descripcion").value,
        fecha: document.getElementById("fecha").value
    };
    
    //realiza una solicitud para registrar el movimiento
    const response = await fetch("/movimientos/registrar/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data) //convierte los datos a formato json
    });

    if (response.ok) {
        alert("Movimiento registrado exitosamente"); //notifica al usuario
        cargarMovimientos(); //vuelve a cargar los movimientos
        event.target.reset(); //resetea el formulario
    } else {
        const error = await response.json();
        alert("Error: " + error.error);
    }
});

cargarMovimientos();

async function eliminar_movimiento(codigo) {
    if (confirm("¿Estás seguro de eliminar este movimiento?")) {
        const response = await fetch(`/movimientos/eliminar/${codigo}/`, { 
            method: "DELETE", //metodo para eliminar
        });
        alert((await response.json()).mensaje); //notifica al usuario del resultado
        cargarMovimientos(); // Recargar tabla
    }
}