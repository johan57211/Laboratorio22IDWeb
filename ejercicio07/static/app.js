// app.js
console.log("✅ JavaScript cargado correctamente");

const API_URL = 'http://localhost:8000';

/**
 * Muestra el resultado en el área de resultado
 */
function mostrarResultado(data, statusCode) {
    const resultadoDiv = document.getElementById('resultado');
    const statusDiv = document.getElementById('statusCode');
    
    // Mostrar código de estado
    statusDiv.textContent = `Status Code: ${statusCode}`;
    statusDiv.className = 'status-code status-' + statusCode;
    
    // Mostrar datos formateados
    resultadoDiv.textContent = JSON.stringify(data, null, 2);
}

/**
 * Muestra un error en el área de resultado
 */
function mostrarError(error, statusCode = 500) {
    const resultadoDiv = document.getElementById('resultado');
    const statusDiv = document.getElementById('statusCode');
    
    statusDiv.textContent = `Status Code: ${statusCode} - ERROR`;
    statusDiv.className = 'status-code status-' + statusCode;
    
    resultadoDiv.textContent = `❌ Error: ${error.message || error}`;
}

/**
 * GET /equipos - Listar todos los equipos
 */
async function listarEquipos() {
    try {
        console.log('📡 GET /equipos');
        
        const response = await fetch(`${API_URL}/equipos`);
        const data = await response.json();
        
        mostrarResultado(data, response.status);
        
        console.log('✅ Equipos obtenidos:', data);
    } catch (error) {
        console.error('❌ Error al listar equipos:', error);
        mostrarError(error);
    }
}

/**
 * POST /equipos - Agregar un nuevo equipo
 */
async function agregarEquipo(event) {
    event.preventDefault(); // Prevenir recarga de página
    
    try {
        // Obtener valores del formulario
        const nombre = document.getElementById('nombre').value;
        const ciudad = document.getElementById('ciudad').value;
        const nivelAtaque = parseInt(document.getElementById('nivelAtaque').value);
        const nivelDefensa = parseInt(document.getElementById('nivelDefensa').value);
        
        // Validar niveles
        if (nivelAtaque < 1 || nivelAtaque > 10 || nivelDefensa < 1 || nivelDefensa > 10) {
            alert('Los niveles deben estar entre 1 y 10');
            return;
        }
        
        // Crear objeto del equipo
        const nuevoEquipo = {
            nombre: nombre,
            ciudad: ciudad,
            nivelAtaque: nivelAtaque,
            nivelDefensa: nivelDefensa
        };
        
        console.log('📡 POST /equipos', nuevoEquipo);
        
        // Hacer la petición POST
        const response = await fetch(`${API_URL}/equipos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(nuevoEquipo)
        });
        
        const data = await response.json();
        
        mostrarResultado(data, response.status);
        
        if (response.ok) {
            console.log('✅ Equipo agregado:', data);
            // Limpiar formulario
            document.getElementById('formAgregar').reset();
            alert(`✅ Equipo "${data.nombre}" agregado con ID: ${data.id}`);
        } else {
            console.error('❌ Error al agregar equipo:', data);
            alert(`❌ Error: ${data.error}`);
        }
        
    } catch (error) {
        console.error('❌ Error al agregar equipo:', error);
        mostrarError(error);
        alert('❌ Error al conectar con el servidor');
    }
}

/**
 * GET /equipos/<id> - Buscar un equipo por ID
 */
async function buscarEquipo() {
    try {
        const id = document.getElementById('idBuscar').value;
        
        if (!id || id < 1) {
            alert('Por favor, ingresa un ID válido');
            return;
        }
        
        console.log(`📡 GET /equipos/${id}`);
        
        const response = await fetch(`${API_URL}/equipos/${id}`);
        const data = await response.json();
        
        mostrarResultado(data, response.status);
        
        if (response.ok) {
            console.log('✅ Equipo encontrado:', data);
        } else {
            console.log('❌ Equipo no encontrado');
        }
        
    } catch (error) {
        console.error('❌ Error al buscar equipo:', error);
        mostrarError(error);
    }
}

/**
 * Evento al cargar la página
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Aplicación iniciada');
    console.log('📍 API URL:', API_URL);
    
    // Cargar equipos iniciales automáticamente
    listarEquipos();
});