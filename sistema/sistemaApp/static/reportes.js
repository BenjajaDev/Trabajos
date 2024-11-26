//escucha el evento cuando el contenido del documento ha sido completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    const tablaReportes = document.getElementById('tablaReportes');

    document.getElementById('reporteProductosMasVendidosPorMes').addEventListener('click', async () => {
    const response = await fetch('/reportes/productos_mas_vendidos_por_mes/');
    const data = await response.json();
    mostrarReportesPorMes(data);
});

    document.getElementById('reporteMovimientosPorTipo').addEventListener('click', async () => {
        const response = await fetch('/reportes/total_movimientos_por_tipo/');
        const data = await response.json();
        mostrarReporte(data, 'Movimientos por tipo');
    });

    document.getElementById('reporteStockActual').addEventListener('click', async () => {
        const response = await fetch('/reportes/stock_actual_productos/');
        const data = await response.json();
        mostrarReporte(data, 'Stock actual de productos');
    });

    document.getElementById('reporteProductosBajoStock').addEventListener('click', async () => {
        const response = await fetch('/reportes/productos_bajo_stock/');
        const data = await response.json();
        mostrarReporte(data, 'Productos Bajo Stock');
    });
    //función para mostrar un reporte general
    function mostrarReporte(data, titulo) {
        tablaReportes.innerHTML = `
            <h3>${titulo}</h3>
            <table class="table">
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Nombre</th>
                        <th>Stock</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(item => `
                        <tr>
                            <td>${item.codigo}</td>
                            <td>${item.nombre}</td>
                            <td>${item.stock}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
    //función para mostrar reportes por mes
    function mostrarReportesPorMes(data) {
        tablaReportes.innerHTML = ''; //limpiar la tabla anterior
        for (const mes in data) {
            //crear un encabezado para el mes
            const mesTitulo = document.createElement('h3');
            const [year, month] = mes.split('-'); //divide la clave del mes en año y mes
        const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
        mesTitulo.textContent = `Productos más vendidos en ${monthNames[parseInt(month) - 1]} ${year}`;
            tablaReportes.appendChild(mesTitulo);
    
            //crear la tabla
            const table = document.createElement('table');
            table.className = 'table';
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                    </tr>
                </thead>
                <tbody>
                    ${data[mes].map(item => `
                        <tr>
                            <td>${item.producto}</td>
                            <td>${item.total_vendido}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
            tablaReportes.appendChild(table);
        }
    }
});