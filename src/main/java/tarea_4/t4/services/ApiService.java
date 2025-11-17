package tarea_4.t4.services;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import org.springframework.stereotype.Service;

import tarea_4.t4.models.*;
import tarea_4.t4.services.*;

@Service
public class ApiService {
    private final Aviso_adopcionRepository aviso_adopcionRepository;
    private final NotaRepository notaRepository;
    public ApiService(Aviso_adopcionRepository aviso_adopcionRepository, NotaRepository notaRepository) {
        this.aviso_adopcionRepository = aviso_adopcionRepository;
        this.notaRepository = notaRepository;
    }

    public Integer getPromedio(Integer avisoId) {
        List<Nota> notas =  notaRepository.findByAviso_Id(avisoId);

        if (notas.isEmpty()) {
            return null;
        }

        Double suma = 0.;
        for (Nota nota : notas) {
            suma += nota.getNota();
        }

        Integer promedio = (int) Math.ceil(suma/notas.size());
        return promedio;
    }

    public Integer agregaNota(Integer idAviso, Integer nota) {

        // Validación
        if (nota < 1 || nota > 7)
            throw new IllegalArgumentException("La nota debe estar entre 1 y 7.");

        Aviso_adopcion aviso = aviso_adopcionRepository.findById(idAviso);

        Nota nuevaNota = new Nota(aviso, nota);
        notaRepository.save(nuevaNota);

        return getPromedio(idAviso);
    }
}

