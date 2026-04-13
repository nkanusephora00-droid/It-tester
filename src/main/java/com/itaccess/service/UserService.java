package com.itaccess.service;

import com.itaccess.dto.UserDTO;
import com.itaccess.entity.User;
import com.itaccess.exception.ResourceNotFoundException;
import com.itaccess.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    public List<UserDTO> getAllUsers() {
        return userRepository.findAll().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }
    
    public UserDTO getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur non trouvé avec l'ID: " + id));
        return toDTO(user);
    }
    
    @Transactional
    public UserDTO createUser(UserDTO dto) {
        if (userRepository.existsByUsername(dto.getUsername())) {
            throw new IllegalArgumentException("Nom d'utilisateur déjà enregistré");
        }
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new IllegalArgumentException("Email déjà enregistré");
        }
        
        User user = User.builder()
                .username(dto.getUsername())
                .email(dto.getEmail())
                .hashedPassword(passwordEncoder.encode(dto.getPassword()))
                .role(dto.getRole() != null ? dto.getRole() : "user")
                .isActive(dto.getIsActive() != null ? dto.getIsActive() : true)
                .build();
        
        User savedUser = userRepository.save(user);
        return toDTO(savedUser);
    }
    
    @Transactional
    public UserDTO updateUser(Long id, UserDTO dto) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur non trouvé avec l'ID: " + id));
        
        if (dto.getEmail() != null && !dto.getEmail().equals(user.getEmail())) {
            if (userRepository.existsByEmail(dto.getEmail())) {
                throw new IllegalArgumentException("Email déjà enregistré");
            }
            user.setEmail(dto.getEmail());
        }
        
        if (dto.getRole() != null) {
            user.setRole(dto.getRole());
        }
        
        if (dto.getIsActive() != null) {
            user.setIsActive(dto.getIsActive());
        }
        
        if (dto.getPassword() != null && !dto.getPassword().isEmpty()) {
            user.setHashedPassword(passwordEncoder.encode(dto.getPassword()));
        }
        
        User updatedUser = userRepository.save(user);
        return toDTO(updatedUser);
    }
    
    @Transactional
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("Utilisateur non trouvé avec l'ID: " + id);
        }
        userRepository.deleteById(id);
    }
    
    public UserDTO toDTO(User user) {
        return UserDTO.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .role(user.getRole())
                .isActive(user.getIsActive())
                .createdAt(user.getCreatedAt() != null ? user.getCreatedAt().toString() : null)
                .build();
    }
}