package tarea_4.t4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table
public class Region {

    @Id
    @SequenceGenerator(
        name= "region_sequence",
        sequenceName = "region_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "region_sequence"
    )
    private Integer id;

    @NotNull
    private String nombre;
}