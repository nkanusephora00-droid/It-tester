package com.itaccess.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TestRequest {
    
    private Long sessionId;
    private Long applicationId;
    private String applicationNom;
    private String version;
    private String environnement;
    
    @NotBlank(message = "La fonction est requise")
    private String fonction;
    
    private String precondition;
    private String etapes;
    private String resultatAttendu;
    private String resultatObtenu;
    
    @NotBlank(message = "Le statut est requis")
    private String statut;
    
    private String commentaires;
}