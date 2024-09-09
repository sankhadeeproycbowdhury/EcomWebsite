package com.sankhadeep.ecomApplication.repository;

import com.sankhadeep.ecomApplication.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductRepo extends JpaRepository<Product, Integer> {

    @Query("SELECT p FROM Product p WHERE LOWER(p.name) LIKE LOWER(%:keyword%) OR LOWER(p.description) LIKE LOWER(%:keyword%) OR LOWER(p.brand) LIKE LOWER(%:keyword%) OR LOWER(p.category) LIKE LOWER(%:keyword%)")
    List<Product> searchProducts(String keyword);

}
