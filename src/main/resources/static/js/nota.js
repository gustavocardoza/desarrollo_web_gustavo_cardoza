// Validación de nota (1–7)
const validar_nota = (n) => {
    return n && Number.isInteger(n) && n >= 1 && n <= 7;
};

// Botones de evaluar
document.querySelectorAll(".btn-evaluar").forEach(btn => {
    btn.addEventListener("click", async () => {
        const idAviso = btn.dataset.id;

        let nota = prompt("Ingrese una nota entre 1 y 7:");
        if (nota === null) return;

        nota = parseInt(nota);

        if (!validar_nota(nota)) {
            alert("La nota debe ser un entero entre 1 y 7.");
            return;
        }

        try {
            const response = await fetch("/agregar_nota", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    id_aviso: idAviso,
                    nota: nota
                })
            });

            console.log("1")

            const data = await response.json();

            console.log("data:")
            console.log(data)

            if (data.error) {
                console.log(2)
                alert(data.error);
                return;
            }

            console.log(3)

            // Actualizar promedio en la tabla
            actualizar_promedio(idAviso, data.promedio);

        } catch (err) {
            console.error("Error enviando nota:", err);
        }
    });
});

// Actualiza el promedio en pantalla (SIN recargar)
function actualizar_promedio(id, promedio) {
    const td = document.getElementById("nota-promedio-" + id);
    td.textContent = promedio;
}
