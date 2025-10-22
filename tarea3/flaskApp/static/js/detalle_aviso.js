
const imagenes = document.getElementsByClassName("imagen-animal")
console.log(imagenes)

const modal = document.getElementById("modal");
const modalImg = document.getElementById("modalImg");
const closeBtn = document.getElementById("closeBtn");

for (let i = 0; i < imagenes.length; i++) {
  imagenes[i].onclick = function() {
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
}

/*
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
*/
