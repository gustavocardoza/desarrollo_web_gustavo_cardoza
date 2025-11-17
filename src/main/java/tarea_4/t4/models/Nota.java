package tarea_4.t4.models;
import tarea_4.t4.models.Aviso_adopcion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table
public class Nota {

    @Id
    @SequenceGenerator(
        name= "nota_sequence",
        sequenceName = "nota_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "nota_sequence"
    )
    private long id;

    @ManyToOne
    @JoinColumn(name = "aviso_id", nullable = false)
    private Aviso_adopcion aviso;

    @NotNull
    private Integer nota;

    public Nota() {

    }

    public Nota(
        Aviso_adopcion aviso,
        Integer nota) {

            this.aviso = aviso;
            this.nota = nota;
    }

    public long getId() {
        return id;
    }

    public Aviso_adopcion getAviso_adopcion() {
        return aviso;
    }

    public Integer getNota() {
        return nota;
    }
}
