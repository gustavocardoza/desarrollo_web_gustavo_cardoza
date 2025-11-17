package tarea_4.t4.models;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table
public class Aviso_adopcion {
    @Id
    @SequenceGenerator(
        name= "aviso_sequence",
        sequenceName = "aviso_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "aviso_sequence"
    )
    private long id;

    @NotNull
    private LocalDateTime fecha_ingreso;
    
    @NotNull
    private Integer comuna_id;

    private String sector;

    @NotNull
    private String nombre;

    @NotNull
    private String email;

    private String celular;

    public enum TipoAnimal {
        gato,
        perro
    }

    @NotNull
    @Enumerated(EnumType.STRING)
    private TipoAnimal tipo;

    @NotNull
    private Integer cantidad;

    public enum UnidadMedidaEdad {
        a,
        m
    }

    @Enumerated(EnumType.STRING)
    private UnidadMedidaEdad unidad_medida;

    @NotNull
    private LocalDateTime fecha_entrega;

    private String descripcion;

    public Aviso_adopcion() {

    }

    public Aviso_adopcion(
        LocalDateTime fecha_ingreso,
        Integer comuna_id,
        String sector,
        String nombre,
        String email,
        String celular,
        TipoAnimal tipo,
        Integer cantidad,
        UnidadMedidaEdad unidad_medida,
        LocalDateTime fecha_entrega,
        String descripcion) {

            this.fecha_ingreso = fecha_ingreso;
            this.comuna_id = comuna_id;
            this.sector = sector;
            this.nombre = nombre;
            this.email = email;
            this.celular = celular;
            this.tipo = tipo;
            this.cantidad = cantidad;
            this.unidad_medida = unidad_medida;
            this.fecha_entrega = fecha_entrega;
            this.descripcion = descripcion;
    }

    public Long getId() {
        return id;
    }

    public LocalDateTime getFecha_ingreso() {
        return fecha_ingreso;
    }

    public Integer getComuna_id() {
        return comuna_id;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }
    
    public String getCelular() {
        return celular;
    }

    public TipoAnimal getTipo() {
        return tipo;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public UnidadMedidaEdad getUnidad_medida() {
        return unidad_medida;
    }

    public LocalDateTime getFecha_entrega() {
        return fecha_entrega;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public static Boolean validateAviso(
        Integer comuna_id,
        String sector,
        String nombre,
        String email,
        String celular,
        TipoAnimal tipo,
        Integer cantidad,
        UnidadMedidaEdad unidad_medida,
        LocalDateTime fecha_entrega,
        String descripcion) {

            return true;
    }




}
