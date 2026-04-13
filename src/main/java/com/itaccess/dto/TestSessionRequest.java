package com.itaccess.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TestSessionRequest {
    
    @NotBlank(message = "Le nom est requis")
    private String nom;
    
    private String description;
    private Long applicationId;
    private String environnement;
    private String version;
    private String nomDocument;
    private String statut;
}