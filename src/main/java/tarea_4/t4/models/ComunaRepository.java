package tarea_4.t4.models;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ComunaRepository extends JpaRepository<Comuna, Long> {
    Page<Comuna> findAllByOrderByIdDesc(Pageable pageable);
    Comuna findById(Integer id);
}
