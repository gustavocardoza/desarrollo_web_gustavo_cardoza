package tarea_4.t4.models;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface Aviso_adopcionRepository extends JpaRepository<Aviso_adopcion, Long> {
    Page<Aviso_adopcion> findAllByOrderByIdDesc(Pageable pageable);
    Aviso_adopcion findById(long Id);
}
