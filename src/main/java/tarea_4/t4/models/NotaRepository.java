package tarea_4.t4.models;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Long> {
    Page<Nota> findAllByOrderByIdDesc(Pageable pageable);
    List<Nota> findByAviso_Id(long avisoId);
}
