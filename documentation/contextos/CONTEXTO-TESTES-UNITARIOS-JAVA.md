# Contexto: Testes Unitários Java Spring Boot — Bob Learning Hub

> **Uso deste documento**: Forneça este arquivo como contexto ao implementar testes unitários em projetos Java Spring Boot do Bob Learning Hub. Ele consolida os padrões de teste, configurações necessárias, templates de código e boas práticas para garantir qualidade e cobertura adequada.

---

## 1. Visão Geral

### 1.1. Estado Atual

O repositório `bff-bob-a-thon` **atualmente não possui testes implementados**. Não existe diretório `src/test/java` nem arquivos de teste. O projeto está configurado com as dependências de teste no `pom.xml`, mas nenhum teste foi criado ainda.

### 1.2. Objetivo deste Documento

Este documento define os **padrões e práticas** que devem ser seguidos ao implementar testes no projeto, incluindo:

- Configuração do ambiente de testes
- Estrutura e organização de arquivos de teste
- Templates de código para diferentes tipos de teste
- Padrões de nomenclatura e convenções
- Estratégias de mock e isolamento
- Configuração de cobertura de código

---

## 2. Stack de Testes

### 2.1. Ferramentas Atuais (pom.xml)

| Ferramenta | Versão | Propósito |
|------------|--------|-----------|
| **JUnit 5** | 5.10.x (via Spring Boot) | Framework de testes |
| **Mockito** | 5.7.x (via Spring Boot) | Framework de mocking |
| **Spring Boot Test** | 3.2.5 | Utilitários de teste Spring |
| **AssertJ** | 3.24.x (via Spring Boot) | Assertions fluentes |
| **JsonPath** | 2.9.x (via Spring Boot) | Testes de JSON |
| **Maven Surefire** | 3.0.0 | Execução de testes unitários |
| **JaCoCo** | 0.8.11 | Cobertura de código |

### 2.2. Dependências no pom.xml

```xml
<dependencies>
    <!-- Spring Boot Test Starter -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

    <!-- Mockito para JUnit 5 -->
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Nota**: `spring-boot-starter-test` já inclui:
- JUnit 5 (Jupiter)
- Mockito
- AssertJ
- Hamcrest
- JsonPath
- JSONassert

---

## 3. Configuração do Ambiente de Testes

### 3.1. Estrutura de Diretórios

```
src/
├── main/
│   └── java/
│       └── com/hackathon/bffbobathon/
│           ├── Application.java
│           ├── adapter/
│           ├── domain/
│           └── config/
└── test/
    ├── java/
    │   └── com/hackathon/bffbobathon/
    │       ├── ApplicationTest.java           # Smoke test
    │       ├── adapter/
    │       │   ├── input/
    │       │   │   └── controller/
    │       │   │       └── ContentControllerTest.java
    │       │   └── output/
    │       │       └── memory/
    │       │           └── ContentRepositoryTest.java
    │       └── domain/
    │           └── service/
    │               └── ContentServiceTest.java
    └── resources/
        └── application-test.yml               # Configurações de teste
```

### 3.2. Plugins Maven

```xml
<build>
    <plugins>
        <!-- Surefire: executa testes unitários -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0</version>
        </plugin>

        <!-- JaCoCo: cobertura de código -->
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.11</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
                <execution>
                    <id>jacoco-check</id>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <configuration>
                        <rules>
                            <rule>
                                <element>PACKAGE</element>
                                <limits>
                                    <limit>
                                        <counter>LINE</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.80</minimum>
                                    </limit>
                                </limits>
                            </rule>
                        </rules>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 3.3. Configuração de Teste (application-test.yml)

Criar arquivo `src/test/resources/application-test.yml`:

```yaml
spring:
  application:
    name: bff-bob-a-thon-test

logging:
  level:
    root: WARN
    com.hackathon.bffbobathon: DEBUG

# Desabilitar configurações desnecessárias em testes
management:
  endpoints:
    enabled-by-default: false
```

---

## 4. Convenções de Nomenclatura

### 4.1. Arquivos de Teste

| Tipo | Arquivo de Código | Arquivo de Teste |
|------|-------------------|------------------|
| Controller | `ContentController.java` | `ContentControllerTest.java` |
| Service | `ContentService.java` | `ContentServiceTest.java` |
| Repository | `ContentRepository.java` | `ContentRepositoryTest.java` |
| Mapper | `ContentMapper.java` | `ContentMapperTest.java` |
| Exception Handler | `GlobalExceptionHandler.java` | `GlobalExceptionHandlerTest.java` |

**Regra**: Arquivo de teste sempre com sufixo `Test.java`.

### 4.2. Métodos de Teste

Use nomes descritivos em português que expliquem o comportamento:

```java
@Test
void deveRetornarListaDeConteudos() { }

@Test
void deveLancarExcecaoQuandoConteudoNaoEncontrado() { }

@Test
void deveCriarConteudoComSucesso() { }
```

**Padrão**: `deve{ComportamentoEsperado}Quando{Condicao}` (opcional)

---

## 5. Templates de Testes

### 5.1. Smoke Test da Aplicação

**Propósito**: Verificar que o contexto Spring carrega corretamente.

**ApplicationTest.java**:
```java
package com.hackathon.bffbobathon;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Smoke test para verificar que o contexto Spring carrega corretamente.
 */
@SpringBootTest
@ActiveProfiles("test")
class ApplicationTest {

    @Test
    void contextLoads() {
        // Se o contexto carregar sem erros, o teste passa
    }
}
```

### 5.2. Teste de Service (Lógica de Negócio)

**Propósito**: Testar lógica de negócio isoladamente com mocks.

**ContentServiceTest.java**:
```java
package com.hackathon.bffbobathon.domain.service;

import com.hackathon.bffbobathon.adapter.input.dto.CreateContentRequest;
import com.hackathon.bffbobathon.adapter.output.memory.ContentRepository;
import com.hackathon.bffbobathon.domain.entity.Content;
import com.hackathon.bffbobathon.domain.exception.ContentNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Testes unitários para ContentService.
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("ContentService")
class ContentServiceTest {

    @Mock
    private ContentRepository contentRepository;

    @InjectMocks
    private ContentService contentService;

    private Content content;
    private CreateContentRequest createRequest;

    @BeforeEach
    void setUp() {
        content = Content.builder()
                .id(1L)
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();

        createRequest = CreateContentRequest.builder()
                .name("New Content")
                .description("New Description")
                .imageUrl("http://example.com/new.jpg")
                .build();
    }

    @Test
    @DisplayName("Deve criar conteúdo com sucesso")
    void deveCriarConteudoComSucesso() {
        // Arrange
        when(contentRepository.save(any(Content.class))).thenReturn(content);

        // Act
        Content result = contentService.createContent(createRequest);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("Test Content");
        verify(contentRepository, times(1)).save(any(Content.class));
    }

    @Test
    @DisplayName("Deve buscar conteúdo por ID com sucesso")
    void deveBuscarConteudoPorIdComSucesso() {
        // Arrange
        when(contentRepository.findById(1L)).thenReturn(Optional.of(content));

        // Act
        Content result = contentService.getContentById(1L);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("Test Content");
        verify(contentRepository, times(1)).findById(1L);
    }

    @Test
    @DisplayName("Deve lançar exceção quando conteúdo não encontrado")
    void deveLancarExcecaoQuandoConteudoNaoEncontrado() {
        // Arrange
        when(contentRepository.findById(999L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> contentService.getContentById(999L))
                .isInstanceOf(ContentNotFoundException.class)
                .hasMessageContaining("999");

        verify(contentRepository, times(1)).findById(999L);
    }

    @Test
    @DisplayName("Deve listar todos os conteúdos")
    void deveListarTodosOsConteudos() {
        // Arrange
        Content content2 = Content.builder()
                .id(2L)
                .name("Content 2")
                .description("Description 2")
                .imageUrl("http://example.com/image2.jpg")
                .build();

        List<Content> contents = Arrays.asList(content, content2);
        when(contentRepository.findAll()).thenReturn(contents);

        // Act
        List<Content> result = contentService.getAllContents();

        // Assert
        assertThat(result).hasSize(2);
        assertThat(result).containsExactly(content, content2);
        verify(contentRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Deve deletar conteúdo com sucesso")
    void deveDeletarConteudoComSucesso() {
        // Arrange
        when(contentRepository.existsById(1L)).thenReturn(true);
        doNothing().when(contentRepository).deleteById(1L);

        // Act
        contentService.deleteContent(1L);

        // Assert
        verify(contentRepository, times(1)).existsById(1L);
        verify(contentRepository, times(1)).deleteById(1L);
    }

    @Test
    @DisplayName("Deve lançar exceção ao deletar conteúdo inexistente")
    void deveLancarExcecaoAoDeletarConteudoInexistente() {
        // Arrange
        when(contentRepository.existsById(999L)).thenReturn(false);

        // Act & Assert
        assertThatThrownBy(() -> contentService.deleteContent(999L))
                .isInstanceOf(ContentNotFoundException.class);

        verify(contentRepository, times(1)).existsById(999L);
        verify(contentRepository, never()).deleteById(anyLong());
    }
}
```

### 5.3. Teste de Controller (REST API)

**Propósito**: Testar endpoints REST com MockMvc.

**ContentControllerTest.java**:
```java
package com.hackathon.bffbobathon.adapter.input.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.hackathon.bffbobathon.adapter.input.dto.ContentDTO;
import com.hackathon.bffbobathon.adapter.input.dto.CreateContentRequest;
import com.hackathon.bffbobathon.adapter.input.mapper.ContentMapper;
import com.hackathon.bffbobathon.domain.entity.Content;
import com.hackathon.bffbobathon.domain.exception.ContentNotFoundException;
import com.hackathon.bffbobathon.domain.service.ContentService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.List;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Testes de integração para ContentController.
 */
@WebMvcTest(ContentController.class)
@DisplayName("ContentController")
class ContentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ContentService contentService;

    @MockBean
    private ContentMapper contentMapper;

    private Content content;
    private ContentDTO contentDTO;
    private CreateContentRequest createRequest;

    @BeforeEach
    void setUp() {
        content = Content.builder()
                .id(1L)
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();

        contentDTO = ContentDTO.builder()
                .id(1L)
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();

        createRequest = CreateContentRequest.builder()
                .name("New Content")
                .description("New Description")
                .imageUrl("http://example.com/new.jpg")
                .build();
    }

    @Test
    @DisplayName("GET /contents - Deve retornar lista de conteúdos")
    void deveRetornarListaDeConteudos() throws Exception {
        // Arrange
        List<Content> contents = Arrays.asList(content);
        List<ContentDTO> contentDTOs = Arrays.asList(contentDTO);

        when(contentService.getAllContents()).thenReturn(contents);
        when(contentMapper.toDTOList(contents)).thenReturn(contentDTOs);

        // Act & Assert
        mockMvc.perform(get("/contents")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].id", is(1)))
                .andExpect(jsonPath("$[0].name", is("Test Content")));

        verify(contentService, times(1)).getAllContents();
        verify(contentMapper, times(1)).toDTOList(contents);
    }

    @Test
    @DisplayName("GET /contents/{id} - Deve retornar conteúdo por ID")
    void deveRetornarConteudoPorId() throws Exception {
        // Arrange
        when(contentService.getContentById(1L)).thenReturn(content);
        when(contentMapper.toDTO(content)).thenReturn(contentDTO);

        // Act & Assert
        mockMvc.perform(get("/contents/1")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Test Content")))
                .andExpect(jsonPath("$.description", is("Test Description")));

        verify(contentService, times(1)).getContentById(1L);
        verify(contentMapper, times(1)).toDTO(content);
    }

    @Test
    @DisplayName("GET /contents/{id} - Deve retornar 404 quando não encontrado")
    void deveRetornar404QuandoNaoEncontrado() throws Exception {
        // Arrange
        when(contentService.getContentById(999L))
                .thenThrow(new ContentNotFoundException(999L));

        // Act & Assert
        mockMvc.perform(get("/contents/999")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(404)))
                .andExpect(jsonPath("$.error", is("Not Found")));

        verify(contentService, times(1)).getContentById(999L);
    }

    @Test
    @DisplayName("POST /contents - Deve criar conteúdo com sucesso")
    void deveCriarConteudoComSucesso() throws Exception {
        // Arrange
        when(contentService.createContent(any(CreateContentRequest.class)))
                .thenReturn(content);
        when(contentMapper.toDTO(content)).thenReturn(contentDTO);

        // Act & Assert
        mockMvc.perform(post("/contents")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(createRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Test Content")));

        verify(contentService, times(1)).createContent(any(CreateContentRequest.class));
        verify(contentMapper, times(1)).toDTO(content);
    }

    @Test
    @DisplayName("POST /contents - Deve retornar 400 quando dados inválidos")
    void deveRetornar400QuandoDadosInvalidos() throws Exception {
        // Arrange
        CreateContentRequest invalidRequest = CreateContentRequest.builder()
                .name("") // Nome vazio (inválido)
                .description("Description")
                .imageUrl("http://example.com/image.jpg")
                .build();

        // Act & Assert
        mockMvc.perform(post("/contents")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest());

        verify(contentService, never()).createContent(any());
    }

    @Test
    @DisplayName("DELETE /contents/{id} - Deve deletar conteúdo com sucesso")
    void deveDeletarConteudoComSucesso() throws Exception {
        // Arrange
        doNothing().when(contentService).deleteContent(1L);

        // Act & Assert
        mockMvc.perform(delete("/contents/1")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNoContent());

        verify(contentService, times(1)).deleteContent(1L);
    }

    @Test
    @DisplayName("DELETE /contents/{id} - Deve retornar 404 quando não encontrado")
    void deveRetornar404AoDeletarConteudoInexistente() throws Exception {
        // Arrange
        doThrow(new ContentNotFoundException(999L))
                .when(contentService).deleteContent(999L);

        // Act & Assert
        mockMvc.perform(delete("/contents/999")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());

        verify(contentService, times(1)).deleteContent(999L);
    }
}
```

### 5.4. Teste de Repository (In-Memory)

**Propósito**: Testar lógica de persistência.

**ContentRepositoryTest.java**:
```java
package com.hackathon.bffbobathon.adapter.output.memory;

import com.hackathon.bffbobathon.domain.entity.Content;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

/**
 * Testes unitários para ContentRepository.
 */
@DisplayName("ContentRepository")
class ContentRepositoryTest {

    private ContentRepository repository;

    @BeforeEach
    void setUp() {
        repository = new ContentRepository();
    }

    @Test
    @DisplayName("Deve salvar conteúdo e gerar ID automaticamente")
    void deveSalvarConteudoEGerarId() {
        // Arrange
        Content content = Content.builder()
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();

        // Act
        Content saved = repository.save(content);

        // Assert
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getName()).isEqualTo("Test Content");
    }

    @Test
    @DisplayName("Deve buscar conteúdo por ID")
    void deveBuscarConteudoPorId() {
        // Arrange
        Content content = Content.builder()
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();
        Content saved = repository.save(content);

        // Act
        Optional<Content> found = repository.findById(saved.getId());

        // Assert
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Test Content");
    }

    @Test
    @DisplayName("Deve retornar Optional vazio quando ID não existe")
    void deveRetornarOptionalVazioQuandoIdNaoExiste() {
        // Act
        Optional<Content> found = repository.findById(999L);

        // Assert
        assertThat(found).isEmpty();
    }

    @Test
    @DisplayName("Deve listar todos os conteúdos")
    void deveListarTodosOsConteudos() {
        // Arrange
        Content content1 = Content.builder()
                .name("Content 1")
                .description("Description 1")
                .imageUrl("http://example.com/1.jpg")
                .build();
        Content content2 = Content.builder()
                .name("Content 2")
                .description("Description 2")
                .imageUrl("http://example.com/2.jpg")
                .build();

        repository.save(content1);
        repository.save(content2);

        // Act
        List<Content> all = repository.findAll();

        // Assert
        assertThat(all).hasSizeGreaterThanOrEqualTo(2); // Inclui dados mockados do construtor
    }

    @Test
    @DisplayName("Deve deletar conteúdo por ID")
    void deveDeletarConteudoPorId() {
        // Arrange
        Content content = Content.builder()
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();
        Content saved = repository.save(content);
        Long id = saved.getId();

        // Act
        repository.deleteById(id);

        // Assert
        Optional<Content> found = repository.findById(id);
        assertThat(found).isEmpty();
    }

    @Test
    @DisplayName("Deve verificar se conteúdo existe por ID")
    void deveVerificarSeConteudoExiste() {
        // Arrange
        Content content = Content.builder()
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();
        Content saved = repository.save(content);

        // Act & Assert
        assertThat(repository.existsById(saved.getId())).isTrue();
        assertThat(repository.existsById(999L)).isFalse();
    }

    @Test
    @DisplayName("Deve atualizar conteúdo existente")
    void deveAtualizarConteudoExistente() {
        // Arrange
        Content content = Content.builder()
                .name("Original Name")
                .description("Original Description")
                .imageUrl("http://example.com/original.jpg")
                .build();
        Content saved = repository.save(content);

        // Act
        saved.setName("Updated Name");
        Content updated = repository.save(saved);

        // Assert
        assertThat(updated.getId()).isEqualTo(saved.getId());
        assertThat(updated.getName()).isEqualTo("Updated Name");
    }
}
```

### 5.5. Teste de Exception Handler

**Propósito**: Testar tratamento global de exceções.

**GlobalExceptionHandlerTest.java**:
```java
package com.hackathon.bffbobathon.adapter.input.exception;

import com.hackathon.bffbobathon.domain.exception.ContentNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;

import java.util.List;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Testes unitários para GlobalExceptionHandler.
 */
@DisplayName("GlobalExceptionHandler")
class GlobalExceptionHandlerTest {

    private GlobalExceptionHandler exceptionHandler;

    @BeforeEach
    void setUp() {
        exceptionHandler = new GlobalExceptionHandler();
    }

    @Test
    @DisplayName("Deve tratar ContentNotFoundException com status 404")
    void deveTratarContentNotFoundException() {
        // Arrange
        ContentNotFoundException exception = new ContentNotFoundException(1L);

        // Act
        ResponseEntity<ErrorResponse> response = 
            exceptionHandler.handleContentNotFound(exception);

        // Assert
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getStatus()).isEqualTo(404);
        assertThat(response.getBody().getError()).isEqualTo("Not Found");
        assertThat(response.getBody().getMessage()).contains("1");
    }

    @Test
    @DisplayName("Deve tratar MethodArgumentNotValidException com status 400")
    void deveTratarMethodArgumentNotValidException() {
        // Arrange
        BindingResult bindingResult = mock(BindingResult.class);
        FieldError fieldError = new FieldError("object", "name", "Nome é obrigatório");
        when(bindingResult.getAllErrors()).thenReturn(List.of(fieldError));

        MethodArgumentNotValidException exception = 
            new MethodArgumentNotValidException(null, bindingResult);

        // Act
        ResponseEntity<ValidationErrorResponse> response = 
            exceptionHandler.handleValidationErrors(exception);

        // Assert
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.BAD_REQUEST);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getStatus()).isEqualTo(400);
        assertThat(response.getBody().getErrors()).containsKey("name");
        assertThat(response.getBody().getErrors().get("name"))
            .isEqualTo("Nome é obrigatório");
    }

    @Test
    @DisplayName("Deve tratar Exception genérica com status 500")
    void deveTratarExceptionGenerica() {
        // Arrange
        Exception exception = new RuntimeException("Erro inesperado");

        // Act
        ResponseEntity<ErrorResponse> response = 
            exceptionHandler.handleGenericException(exception);

        // Assert
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getStatus()).isEqualTo(500);
        assertThat(response.getBody().getError()).isEqualTo("Internal Server Error");
    }
}
```

### 5.6. Teste de Mapper (MapStruct)

**Propósito**: Testar conversão entre DTOs e entidades.

**ContentMapperTest.java**:
```java
package com.hackathon.bffbobathon.adapter.input.mapper;

import com.hackathon.bffbobathon.adapter.input.dto.ContentDTO;
import com.hackathon.bffbobathon.domain.entity.Content;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mapstruct.factory.Mappers;

import java.util.Arrays;
import java.util.List;

import static org.assertj.core.api.Assertions.*;

/**
 * Testes unitários para ContentMapper.
 */
@DisplayName("ContentMapper")
class ContentMapperTest {

    private final ContentMapper mapper = Mappers.getMapper(ContentMapper.class);

    @Test
    @DisplayName("Deve converter Content para ContentDTO")
    void deveConverterContentParaDTO() {
        // Arrange
        Content content = Content.builder()
                .id(1L)
                .name("Test Content")
                .description("Test Description")
                .imageUrl("http://example.com/image.jpg")
                .build();

        // Act
        ContentDTO dto = mapper.toDTO(content);

        // Assert
        assertThat(dto).isNotNull();
        assertThat(dto.getId()).isEqualTo(1L);
        assertThat(dto.getName()).isEqualTo("Test Content");
        assertThat(dto.getDescription()).isEqualTo("Test Description");
        assertThat(dto.getImageUrl()).isEqualTo("http://example.com/image.jpg");
    }

    @Test
    @DisplayName("Deve converter lista de Content para lista de ContentDTO")
    void deveConverterListaDeContentParaListaDeDTO() {
        // Arrange
        Content content1 = Content.builder()
                .id(1L)
                .name("Content 1")
                .description("Description 1")
                .imageUrl("http://example.com/1.jpg")
                .build();

        Content content2 = Content.builder()
                .id(2L)
                .name("Content 2")
                .description("Description 2")
                .imageUrl("http://example.com/2.jpg")
                .build();

        List<Content> contents = Arrays.asList(content1, content2);

        // Act
        List<ContentDTO> dtos = mapper.toDTOList(contents);

        // Assert
        assertThat(dtos).hasSize(2);
        assertThat(dtos.get(0).getId()).isEqualTo(1L);
        assertThat(dtos.get(1).getId()).isEqualTo(2L);
    }

    @Test
    @DisplayName("Deve retornar null quando Content é null")
    void deveRetornarNullQuandoContentNull() {
        // Act
        ContentDTO dto = mapper.toDTO(null);

        // Assert
        assertThat(dto).isNull();
    }
}
```

---

## 6. Estratégias de Mock

### 6.1. Mockito Annotations

```java
@ExtendWith(MockitoExtension.class)
class ServiceTest {
    @Mock
    private Repository repository;  // Mock automático

    @InjectMocks
    private Service service;  // Injeta mocks automaticamente

    @Captor
    private ArgumentCaptor<Entity> captor;  // Captura argumentos
}
```

### 6.2. Stubbing (Configurar comportamento)

```java
// Retornar valor
when(repository.findById(1L)).thenReturn(Optional.of(entity));

// Lançar exceção
when(repository.findById(999L)).thenThrow(new NotFoundException());

// Retornar valores diferentes em chamadas sucessivas
when(repository.count())
    .thenReturn(0L)
    .thenReturn(1L)
    .thenReturn(2L);

// Executar ação customizada
when(repository.save(any())).thenAnswer(invocation -> {
    Entity entity = invocation.getArgument(0);
    entity.setId(1L);
    return entity;
});
```

### 6.3. Verification (Verificar chamadas)

```java
// Verificar que método foi chamado
verify(repository).save(any());

// Verificar número de chamadas
verify(repository, times(2)).findAll();
verify(repository, never()).delete(any());
verify(repository, atLeastOnce()).save(any());

// Verificar ordem de chamadas
InOrder inOrder = inOrder(repository);
inOrder.verify(repository).findById(1L);
inOrder.verify(repository).save(any());

// Capturar argumentos
verify(repository).save(captor.capture());
Entity captured = captor.getValue();
assertThat(captured.getName()).isEqualTo("Expected");
```

### 6.4. ArgumentMatchers

```java
// Qualquer valor
when(repository.save(any(Entity.class))).thenReturn(entity);

// Valor específico
when(repository.findById(eq(1L))).thenReturn(Optional.of(entity));

// Null
when(repository.save(isNull())).thenThrow(new IllegalArgumentException());

// Predicado customizado
when(repository.findByName(argThat(name -> name.length() > 5)))
    .thenReturn(List.of(entity));
```

---

## 7. Boas Práticas

### 7.1. Padrão AAA (Arrange-Act-Assert)

```java
@Test
void deveCalcularTotalComDesconto() {
    // Arrange: preparar dados e mocks
    Order order = new Order(100.0);
    when(discountService.calculate()).thenReturn(10.0);
    
    // Act: executar ação
    double total = orderService.calculateTotal(order);
    
    // Assert: verificar resultado
    assertThat(total).isEqualTo(90.0);
    verify(discountService).calculate();
}
```

### 7.2. Usar AssertJ para Assertions Fluentes

```java
// Em vez de JUnit assertions
assertEquals(expected, actual);
assertTrue(condition);

// Use AssertJ
assertThat(actual).isEqualTo(expected);
assertThat(condition).isTrue();
assertThat(list).hasSize(3).contains("item1", "item2");
assertThat(exception).hasMessageContaining("error");
```

### 7.3. Usar @DisplayName para Descrições Claras

```java
@Test
@DisplayName("Deve retornar erro 404 quando conteúdo não encontrado")
void deveRetornar404QuandoConteudoNaoEncontrado() {
    // ...
}
```

### 7.4. Organizar Testes com @Nested

```java
@DisplayName("ContentService")
class ContentServiceTest {

    @Nested
    @DisplayName("Criar conteúdo")
    class CreateContent {
        @Test
        void devecriarComSucesso() { }

        @Test
        void deveLancarExcecaoQuandoDadosInvalidos() { }
    }

    @Nested
    @DisplayName("Buscar conteúdo")
    class GetContent {
        @Test
        void deveBuscarPorId() { }

        @Test
        void deveLancarExcecaoQuandoNaoEncontrado() { }
    }
}
```

### 7.5. Usar @ParameterizedTest para Múltiplos Casos

```java
@ParameterizedTest
@ValueSource(strings = {"", "  ", "\t", "\n"})
void deveRejeitarNomesVazios(String nome) {
    assertThatThrownBy(() -> service.create(nome))
        .isInstanceOf(IllegalArgumentException.class);
}

@ParameterizedTest
@CsvSource({
    "1, 10, 11",
    "2, 20, 22",
    "3, 30, 33"
})
void deveSomarCorretamente(int a, int b, int expected) {
    assertThat(calculator.sum(a, b)).isEqualTo(expected);
}
```

---

## 8. Cobertura de Código

### 8.1. Configuração JaCoCo

O plugin JaCoCo já está configurado no `pom.xml` para:
- Gerar relatório após execução dos testes
- Verificar cobertura mínima de 80%
- Falhar o build se cobertura for insuficiente

### 8.2. Exclusões de Cobertura

Adicionar ao plugin JaCoCo:

```xml
<configuration>
    <excludes>
        <exclude>**/Application.class</exclude>
        <exclude>**/config/**</exclude>
        <exclude>**/dto/**</exclude>
        <exclude>**/exception/**</exclude>
    </excludes>
</configuration>
```

### 8.3. Visualizar Relatório

Após executar `mvn test`, abrir:
```
target/site/jacoco/index.html
```

---

## 9. Comandos Maven

### 9.1. Executar Testes

```bash
# Todos os testes
mvn test

# Testes específicos
mvn test -Dtest=ContentServiceTest

# Pular testes
mvn install -DskipTests
```

### 9.2. Gerar Relatório de Cobertura

```bash
mvn clean test jacoco:report
```

### 9.3. Verificar Cobertura Mínima

```bash
mvn clean verify
```

---

## 10. Integração com CI/CD

### 10.1. GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Run tests
        run: mvn clean verify
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./target/site/jacoco/jacoco.xml
```

### 10.2. Azure DevOps

```yaml
- task: Maven@3
  inputs:
    mavenPomFile: 'pom.xml'
    goals: 'clean verify'
    publishJUnitResults: true
    testResultsFiles: '**/surefire-reports/TEST-*.xml'
    codeCoverageToolOption: 'JaCoCo'
```

---

## 11. Troubleshooting

### 11.1. Erro: "No tests were executed"

**Causa**: Arquivos de teste não seguem convenção `*Test.java`

**Solução**: Renomear para `ClasseTest.java`

### 11.2. Erro: "MockitoException: Cannot mock final class"

**Causa**: Tentando mockar classe final

**Solução**: Usar interface ou adicionar `mockito-inline`:
```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-inline</artifactId>
    <scope>test</scope>
</dependency>
```

### 11.3. Erro: "UnnecessaryStubbingException"

**Causa**: Mock configurado mas não usado

**Solução**: Remover stub não utilizado ou usar `lenient()`:
```java
lenient().when(repository.findById(1L)).thenReturn(Optional.of(entity));
```

---

## 12. Checklist de Implementação

- [ ] Criar estrutura `src/test/java` espelhando `src/main/java`
- [ ] Criar `application-test.yml` em `src/test/resources`
- [ ] Configurar plugins Surefire e JaCoCo no `pom.xml`
- [ ] Criar smoke test `ApplicationTest`
- [ ] Criar testes para todos os Services
- [ ] Criar testes para todos os Controllers
- [ ] Criar testes para Repositories
- [ ] Criar testes para Exception Handlers
- [ ] Criar testes para Mappers
- [ ] Configurar cobertura mínima de 80%
- [ ] Integrar testes no pipeline de CI/CD
- [ ] Documentar casos de teste complexos

---

## 13. Recursos e Referências

### Documentação Oficial

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)
- [AssertJ Documentation](https://assertj.github.io/doc/)
- [Spring Boot Testing](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)

### Ferramentas

- [JaCoCo Maven Plugin](https://www.jacoco.org/jacoco/trunk/doc/maven.html)
- [Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)

---

**Última atualização**: 2026-05-21  
**Versão do documento**: 1.0.0