package tarea_4.t4.services;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.security.MessageDigest;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Formatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;
import org.springframework.web.multipart.MultipartFile;

import tarea_4.t4.models.Aviso_adopcion;
import tarea_4.t4.models.Aviso_adopcionRepository;
import tarea_4.t4.models.Comuna;
import tarea_4.t4.models.ComunaRepository;
import tarea_4.t4.models.Nota;
import tarea_4.t4.models.NotaRepository;

@Service
public class AppService {
    private final String pathStatic;
    private final Aviso_adopcionRepository aviso_adopcionRepository;
    private final ComunaRepository comunaRepository;
    private final NotaRepository notaRepository;

    public AppService(Aviso_adopcionRepository aviso_adopcionRepository, ComunaRepository comunaRepository, NotaRepository notaRepository) 
    throws IOException {
        this.aviso_adopcionRepository = aviso_adopcionRepository;
        this.comunaRepository = comunaRepository;
        this.notaRepository = notaRepository;
        
        // Dynamically resolve the absolute path for the static directory
        Path staticDir = Paths.get(ResourceUtils.getFile("classpath:static").getAbsolutePath());
        this.pathStatic = staticDir.toString();
        //this.pathStatic = "C:\\Users\\gusta\\UChile\\6to_semestre\\APP_WEB\\t4\\src\\main\\resources\\static";
        System.out.println("Static path resolved to: " + this.pathStatic);
    }

    public List<Map<String, String>> getAviso_adopcionData(Integer pageSize) {
        List<Aviso_adopcion> avisos_adopcion = aviso_adopcionRepository.findAllByOrderByIdDesc(PageRequest.of(0, pageSize)).getContent();
        List<Map<String, String>> aviso_adopcionData = new ArrayList<>();

        for (Aviso_adopcion aviso : avisos_adopcion) {

            List<Nota> notas = notaRepository.findByAviso_Id(aviso.getId());
            
            Integer prom = -1;
            if (!notas.isEmpty()) {
                Integer suma = 0;
                for (Nota n : notas) {
                    suma += n.getNota();
                }
                prom = (int) Math.ceil(suma/notas.size());
            }

            Map<String, String> avisoData = new HashMap<>();
            avisoData.put("id", aviso.getId().toString());
            avisoData.put("fechaIngreso", aviso.getFecha_ingreso().toString());
            Comuna c = comunaRepository.findById(aviso.getComuna_id());
            avisoData.put("comuna_id", c.getNombre().toString());
            avisoData.put("sector", aviso.getSector().toString());
            avisoData.put("nombre", aviso.getNombre().toString());
            avisoData.put("email", aviso.getEmail().toString());
            avisoData.put("nombre", aviso.getNombre().toString());
            avisoData.put("celular", aviso.getCelular().toString());
            avisoData.put("tipoAnimal", aviso.getTipo().toString());
            avisoData.put("cantidad", aviso.getCantidad().toString());
            avisoData.put("unidadMedida", aviso.getUnidad_medida().toString());
            avisoData.put("fechaEntrega", aviso.getFecha_entrega().toString());
            avisoData.put("descripcion", aviso.getDescripcion().toString());
            avisoData.put("promedio", prom.toString());
            aviso_adopcionData.add(avisoData);
        }
        return aviso_adopcionData;
    }
}

