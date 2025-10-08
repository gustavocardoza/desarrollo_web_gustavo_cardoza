const copito1 = document.getElementById("copito1");
const copito2 = document.getElementById("copito2");

const modal = document.getElementById("modal");
const modalImg = document.getElementById("modalImg");
const closeBtn = document.getElementById("closeBtn");

copito1.onclick = function() {
  modal.style.display = "block";
  modalImg.src = this.src;
}

closeBtn.onclick = function() {
  modal.style.display = "none";
}

modal.onclick = function(e) {
  if (e.target === modal) {
    modal.style.display = "none";
  }
}

copito2.onclick = function() {
  modal.style.display = "block";
  modalImg.src = this.src;
}

closeBtn.onclick = function() {
  modal.style.display = "none";
}

modal.onclick = function(e) {
  if (e.target === modal) {
    modal.style.display = "none";
  }
}

const btnVolverListado = document.getElementById("volver_listado_adopciones")
btnVolverListado.addEventListener("click", () => {
  window.location.href = "listado_aviso_adopcion.html"
})