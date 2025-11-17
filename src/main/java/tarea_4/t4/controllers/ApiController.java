package tarea_4.t4.controllers;

import org.springframework.web.bind.annotation.RestController;

import tarea_4.t4.models.*;
import tarea_4.t4.services.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
public class ApiController {
    private final ApiService apiService;
    public ApiController(ApiService apiService) {
        this.apiService = apiService;
    }

    @PostMapping("/agregar_nota")
    public Map<String, Object> agregarNota(@RequestParam("id_aviso") Integer idAviso, @RequestParam Integer nota) {
        Integer nuevoPromedio = apiService.agregaNota(idAviso, nota);
        Map<String, Object> resultado = new HashMap<>();
        resultado.put("promedio", nuevoPromedio);
        return resultado;
    }
}
