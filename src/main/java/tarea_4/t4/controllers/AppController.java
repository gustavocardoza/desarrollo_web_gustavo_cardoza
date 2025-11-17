package tarea_4.t4.controllers;

import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import tarea_4.t4.services.AppService;

@Controller
public class AppController {
    private final AppService appService;
    public AppController(AppService appService) {
        this.appService = appService;
    }

    @GetMapping("/")
    public String indexRoute(Model model) {
        List<Map<String, String>> modelData = appService.getAviso_adopcionData(10);
        model.addAttribute("avisos", modelData);
        return "notas";
    }
}
