package com.sankhadeep.ecomApplication.controller;

import com.sankhadeep.ecomApplication.model.Product;
import com.sankhadeep.ecomApplication.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api")
public class ProductController {

    @Autowired
    private ProductService service;


    @CrossOrigin(origins = "http://localhost:5173/")
    @RequestMapping("/")
    public String greet(){
        return "Hello World";
    }


    @CrossOrigin(origins = "http://localhost:5173/")
    @GetMapping("/products")
    public ResponseEntity<List<Product>> getProducts(){
        return new  ResponseEntity<>(service.getAllProducts(), HttpStatus.OK);
    }


    @CrossOrigin(origins = "http://localhost:5173/")
    @GetMapping("/products/{id}")
    public ResponseEntity<Product> getProductsById(@PathVariable int id){
        Product product = service.getProductsById(id);
        if(product != null){
            return new ResponseEntity<>(product, HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }


    @CrossOrigin(origins = "http://localhost:5173/")
    @GetMapping("/products/{id}/image")
    public ResponseEntity<byte[]> getImageByProductId(@PathVariable int id){
        Product product = service.getProductsById(id);
        byte[] image = product.getImageData();

        // ResponseEntity returns a statusCode of Ok, contentType, and image in body
        return ResponseEntity.ok().contentType(MediaType.valueOf(product.getImageType())).body(image);
    }


    @CrossOrigin(origins = "http://localhost:5173/")
    @PostMapping("/products")
    public ResponseEntity<?> addProduct(@RequestPart Product product, @RequestPart MultipartFile imageFile){
        try{
            Product product1 = service.addProduct(product, imageFile);
            return new ResponseEntity<>(product1, HttpStatus.CREATED);
        }
        catch (Exception e){
            return new ResponseEntity<>(e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @CrossOrigin(origins = "http://localhost:5173/")
    @PutMapping("/products/{id}")
    public ResponseEntity<String> updateProduct(@PathVariable int id, @RequestPart Product product,
                                                @RequestPart MultipartFile imageFile){
        Product product1 = null;
        try {
            product1 = service.updateProduct(id, product, imageFile);
        } catch (IOException e) {
            return new ResponseEntity<>("Failed to Update", HttpStatus.BAD_REQUEST);
        }

        if(product1 != null){
            return new ResponseEntity<>("Updated", HttpStatus.OK);
        }

        return new ResponseEntity<>("Failed to Update", HttpStatus.BAD_REQUEST);
    }


    @CrossOrigin(origins = "http://localhost:5173/")
    @DeleteMapping("/products/{id}")
    public ResponseEntity<String> deleteProduct(@PathVariable int id){
        Product product = service.getProductsById(id);
        if(product != null){
            service.deleteProduct(id);
            return new ResponseEntity<>("Deleted", HttpStatus.OK);
        }

        return new ResponseEntity<>("Product Not Found", HttpStatus.NOT_FOUND);
    }

    @CrossOrigin(origins = "http://localhost:5173/")
    @GetMapping("/products/search")
    public ResponseEntity<List<Product>> searchProduct(@RequestParam String keyword){
        List<Product> products = service.searchProducts(keyword);
        return new ResponseEntity<>(products, HttpStatus.OK);
    }
}
