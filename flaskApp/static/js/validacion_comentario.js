const validar_comentario = () => {
    // Funciones de validación (front).
    const validar_nombre = (nombre) => {
        return (nombre) && (nombre.length >= 3) && (nombre.length <= 80) 
    }

    const validar_texto = (texto) => {
        return (texto) && (texto.length >= 5)
    }

    // Inputs del usuario.
    const nombre = document.getElementById("nombre_coment");
    const texto = document.getElementById("text_coment");

    // Validación del los inputs del usuario.
    let info_valida = true;
    let mensaje = "";

    if (!validar_nombre(nombre.value)) {
        info_valida = false;
        mensaje += "Su nombre es inválido, debe tener mínimo 3 carácteres y máximo 80. Intente nuevamente.\n";
        nombre.style.borderColor = "red";
    } else {
        nombre.style.borderColor = "";
    }

    if (!validar_texto(texto.value)) {
        info_valida = false;
        mensaje += "Su comentario es inválido, debe tener mínimo 5 carácteres. Intente nuevamente. \n";
        texto.style.borderColor = "red";
    } else {
        nombre.style.borderColor = "";
    }

    // Se entrega el respectivo mensaje.
    if (info_valida==false) {
        alert(mensaje);
    }

    return info_valida;
}

const btnAgregarComent = document.getElementById("boton_agregar_coment");
const formComentario = document.getElementById("form_comentario");
const id = document.getElementById("id_aviso").value;

async function cargar_comentarios() {
    try {
        const response = await fetch(`/get-comentarios-data?id_aviso=${id}`);
        const data = await response.json();

        const contenedor = document.getElementById("lista_comentarios");
        contenedor.innerHTML = "";

        data.forEach(comentario => {
            const section = document.createElement("section")
            section.innerHTML = `
                <p><strong>${comentario.nombre}</strong> (${comentario.fecha})</p>
                <p>${comentario.texto}</p>
                <hr>
            `;        
            contenedor.appendChild(section)    
        });
    } catch (err) {
        console.error("Error cargando comentarios:", err);
    }
};

btnAgregarComent.addEventListener("click", async () => {
    if (!validar_comentario()) {
        return;
    }

    const nombre = document.getElementById("nombre_coment").value;
    const texto = document.getElementById("text_coment").value;

    const response = await fetch("/agregar_comentario", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: new URLSearchParams({ id_aviso: id, nombre_coment: nombre, texto_coment: texto })
    });

    const data = await response.json();
    if (data.error) {
        alert(data.error)
    } else {
        alert("comentario agregado");
        cargar_comentarios();
        formComentario.reset();
    }
})

cargar_comentarios();


