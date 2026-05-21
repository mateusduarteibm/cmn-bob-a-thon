# Contexto: Testes Unitários Angular — Bob Learning Hub

> **Uso deste documento**: Forneça este arquivo como contexto ao implementar testes unitários em projetos Angular do Bob Learning Hub. Ele consolida os padrões de teste, configurações necessárias, templates de código e boas práticas para garantir qualidade e cobertura adequada.

---

## 1. Visão Geral

### 1.1. Estado Atual

O repositório `fed-bob-a-thon` **atualmente não possui testes implementados**. O `angular.json` está configurado com `skipTests: true` para todos os schematics, o que significa que novos componentes, serviços e outros artefatos são gerados sem arquivos `.spec.ts`.

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

### 2.1. Ferramentas Atuais (package.json)

| Ferramenta | Versão | Propósito |
|------------|--------|-----------|
| **Jasmine** | 5.1.0 | Framework de testes (BDD) |
| **Karma** | 6.4.0 | Test runner (executa testes no browser) |
| **karma-jasmine** | 5.1.0 | Adapter Jasmine para Karma |
| **karma-chrome-launcher** | 3.2.0 | Launcher para Chrome headless |
| **karma-coverage** | 2.2.0 | Relatórios de cobertura |
| **karma-jasmine-html-reporter** | 2.1.0 | Relatório HTML interativo |

### 2.2. Alternativa Recomendada: Jest

Para projetos novos ou refatoração, considere migrar para **Jest**:

**Vantagens do Jest**:
- ✅ Mais rápido (não precisa de browser real)
- ✅ Melhor experiência de desenvolvimento (watch mode, snapshots)
- ✅ Configuração mais simples
- ✅ Melhor integração com VS Code
- ✅ Suporte nativo a ES modules

**Migração para Jest** (opcional):
```bash
npm install --save-dev @angular-builders/jest jest @types/jest
npm uninstall karma karma-jasmine karma-chrome-launcher karma-coverage karma-jasmine-html-reporter
```

---

## 3. Configuração do Ambiente de Testes

### 3.1. Habilitar Geração de Testes

**Passo 1**: Editar `angular.json` para remover `skipTests: true`:

```json
{
  "schematics": {
    "@schematics/angular:component": {
      "style": "scss",
      "skipTests": false  // ← Alterar para false
    },
    "@schematics/angular:service": {
      "skipTests": false  // ← Alterar para false
    }
    // Repetir para todos os schematics
  }
}
```

### 3.2. Configuração do Karma (karma.conf.js)

Criar arquivo `karma.conf.js` na raiz do projeto:

```javascript
module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-jasmine-html-reporter'),
      require('karma-coverage'),
      require('@angular-devkit/build-angular/plugins/karma')
    ],
    client: {
      jasmine: {
        random: false  // Executar testes na ordem (útil para debug)
      },
      clearContext: false
    },
    jasmineHtmlReporter: {
      suppressAll: true
    },
    coverageReporter: {
      dir: require('path').join(__dirname, './coverage'),
      subdir: '.',
      reporters: [
        { type: 'html' },
        { type: 'text-summary' },
        { type: 'lcovonly' }
      ],
      check: {
        global: {
          statements: 80,
          branches: 80,
          functions: 80,
          lines: 80
        }
      }
    },
    reporters: ['progress', 'kjhtml'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['Chrome'],
    singleRun: false,
    restartOnFileChange: true,
    customLaunchers: {
      ChromeHeadlessCI: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox', '--disable-gpu']
      }
    }
  });
};
```

### 3.3. Scripts no package.json

Adicionar scripts de teste:

```json
{
  "scripts": {
    "test": "ng test",
    "test:ci": "ng test --no-watch --no-progress --browsers=ChromeHeadlessCI",
    "test:coverage": "ng test --no-watch --code-coverage",
    "test:watch": "ng test --watch"
  }
}
```

### 3.4. Configuração do TypeScript para Testes

O arquivo `tsconfig.spec.json` já existe e está configurado corretamente:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./out-tsc/spec",
    "types": ["jasmine"]
  },
  "include": ["src/**/*.spec.ts", "src/**/*.d.ts"]
}
```

---

## 4. Estrutura de Arquivos de Teste

### 4.1. Convenção de Nomenclatura

| Tipo | Arquivo de Código | Arquivo de Teste |
|------|-------------------|------------------|
| Component | `app.component.ts` | `app.component.spec.ts` |
| Service | `content.service.ts` | `content.service.spec.ts` |
| Pipe | `format-date.pipe.ts` | `format-date.pipe.spec.ts` |
| Directive | `highlight.directive.ts` | `highlight.directive.spec.ts` |
| Guard | `auth.guard.ts` | `auth.guard.spec.ts` |

**Regra**: Arquivo de teste sempre no **mesmo diretório** do arquivo testado, com sufixo `.spec.ts`.

### 4.2. Estrutura de um Arquivo de Teste

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ComponentToTest } from './component-to-test';

describe('ComponentToTest', () => {
  let component: ComponentToTest;
  let fixture: ComponentFixture<ComponentToTest>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComponentToTest]  // Standalone component
    }).compileComponents();

    fixture = TestBed.createComponent(ComponentToTest);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Mais testes aqui...
});
```

---

## 5. Templates de Testes

### 5.1. Teste de Componente Standalone

**Cenário**: Testar o `AppComponent` do projeto.

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AppComponent } from './app.component';
import { RouterOutlet } from '@angular/router';

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        AppComponent,
        HttpClientTestingModule
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Verifica que não há requisições pendentes
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
  });

  it('should have title "Bob Learning Hub"', () => {
    expect(component.title).toBe('Bob Learning Hub');
  });

  it('should initialize with loading state', () => {
    expect(component.isLoading()).toBe(true);
  });

  it('should load courses on init', () => {
    const mockCourses = [
      { id: 1, name: 'Course 1', description: 'Desc 1', imageUrl: 'url1' }
    ];

    // Trigger ngOnInit (constructor já foi chamado)
    fixture.detectChanges();

    const req = httpMock.expectOne(url => url.includes('/contents'));
    expect(req.request.method).toBe('GET');
    req.flush(mockCourses);

    expect(component.courses().length).toBe(1);
    expect(component.isLoading()).toBe(false);
  });

  it('should handle error when loading courses fails', () => {
    fixture.detectChanges();

    const req = httpMock.expectOne(url => url.includes('/contents'));
    req.error(new ProgressEvent('error'));

    expect(component.errorMessage()).toBeTruthy();
    expect(component.isLoading()).toBe(false);
  });

  it('should filter courses by category', () => {
    component.courses.set([
      { id: 1, title: 'Course 1', category: 'Frontend', /* ... */ },
      { id: 2, title: 'Course 2', category: 'Backend', /* ... */ }
    ]);

    component.selectCategory('Frontend');

    expect(component.filteredCourses().length).toBe(1);
    expect(component.filteredCourses()[0].category).toBe('Frontend');
  });

  it('should show all courses when "All" category is selected', () => {
    component.courses.set([
      { id: 1, title: 'Course 1', category: 'Frontend', /* ... */ },
      { id: 2, title: 'Course 2', category: 'Backend', /* ... */ }
    ]);

    component.selectCategory('All');

    expect(component.filteredCourses().length).toBe(2);
  });

  it('should compute featured course as first course', () => {
    const courses = [
      { id: 1, title: 'Featured', category: 'Frontend', /* ... */ },
      { id: 2, title: 'Other', category: 'Backend', /* ... */ }
    ];
    component.courses.set(courses);

    expect(component.featuredCourse()?.title).toBe('Featured');
  });

  it('should return null for featured course when no courses', () => {
    component.courses.set([]);
    expect(component.featuredCourse()).toBeNull();
  });

  it('should compute unique categories from courses', () => {
    component.courses.set([
      { id: 1, title: 'C1', category: 'Frontend', /* ... */ },
      { id: 2, title: 'C2', category: 'Backend', /* ... */ },
      { id: 3, title: 'C3', category: 'Frontend', /* ... */ }
    ]);

    const categories = component.categories();
    expect(categories).toContain('All');
    expect(categories).toContain('Frontend');
    expect(categories).toContain('Backend');
    expect(categories.length).toBe(3); // All + 2 unique
  });
});
```

### 5.2. Teste de Serviço com HttpClient

**Cenário**: Criar um serviço `ContentService` e testá-lo.

**content.service.ts**:
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Content {
  id: number;
  name: string;
  description: string;
  imageUrl: string;
}

@Injectable({ providedIn: 'root' })
export class ContentService {
  #http = inject(HttpClient);
  #baseUrl = 'https://api.example.com/api/contents';

  getAll(): Observable<Content[]> {
    return this.#http.get<Content[]>(this.#baseUrl);
  }

  getById(id: number): Observable<Content> {
    return this.#http.get<Content>(`${this.#baseUrl}/${id}`);
  }

  create(content: Omit<Content, 'id'>): Observable<Content> {
    return this.#http.post<Content>(this.#baseUrl, content);
  }

  delete(id: number): Observable<void> {
    return this.#http.delete<void>(`${this.#baseUrl}/${id}`);
  }
}
```

**content.service.spec.ts**:
```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ContentService, Content } from './content.service';

describe('ContentService', () => {
  let service: ContentService;
  let httpMock: HttpTestingController;
  const baseUrl = 'https://api.example.com/api/contents';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ContentService]
    });

    service = TestBed.inject(ContentService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getAll', () => {
    it('should return an array of contents', () => {
      const mockContents: Content[] = [
        { id: 1, name: 'Content 1', description: 'Desc 1', imageUrl: 'url1' },
        { id: 2, name: 'Content 2', description: 'Desc 2', imageUrl: 'url2' }
      ];

      service.getAll().subscribe(contents => {
        expect(contents.length).toBe(2);
        expect(contents).toEqual(mockContents);
      });

      const req = httpMock.expectOne(baseUrl);
      expect(req.request.method).toBe('GET');
      req.flush(mockContents);
    });

    it('should handle error when API fails', () => {
      service.getAll().subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(500);
        }
      });

      const req = httpMock.expectOne(baseUrl);
      req.flush('Server error', { status: 500, statusText: 'Internal Server Error' });
    });
  });

  describe('getById', () => {
    it('should return a single content', () => {
      const mockContent: Content = {
        id: 1,
        name: 'Content 1',
        description: 'Desc 1',
        imageUrl: 'url1'
      };

      service.getById(1).subscribe(content => {
        expect(content).toEqual(mockContent);
      });

      const req = httpMock.expectOne(`${baseUrl}/1`);
      expect(req.request.method).toBe('GET');
      req.flush(mockContent);
    });

    it('should handle 404 when content not found', () => {
      service.getById(999).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(404);
        }
      });

      const req = httpMock.expectOne(`${baseUrl}/999`);
      req.flush('Not found', { status: 404, statusText: 'Not Found' });
    });
  });

  describe('create', () => {
    it('should create a new content', () => {
      const newContent = {
        name: 'New Content',
        description: 'New Desc',
        imageUrl: 'new-url'
      };
      const createdContent: Content = { id: 3, ...newContent };

      service.create(newContent).subscribe(content => {
        expect(content.id).toBe(3);
        expect(content.name).toBe(newContent.name);
      });

      const req = httpMock.expectOne(baseUrl);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual(newContent);
      req.flush(createdContent);
    });
  });

  describe('delete', () => {
    it('should delete a content', () => {
      service.delete(1).subscribe(response => {
        expect(response).toBeUndefined();
      });

      const req = httpMock.expectOne(`${baseUrl}/1`);
      expect(req.request.method).toBe('DELETE');
      req.flush(null);
    });
  });
});
```

### 5.3. Teste de Pipe

**Cenário**: Criar um pipe para formatar datas.

**format-date.pipe.ts**:
```typescript
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatDate',
  standalone: true
})
export class FormatDatePipe implements PipeTransform {
  transform(value: string | Date): string {
    if (!value) return '';
    
    const date = typeof value === 'string' ? new Date(value) : value;
    return date.toLocaleDateString('pt-BR');
  }
}
```

**format-date.pipe.spec.ts**:
```typescript
import { FormatDatePipe } from './format-date.pipe';

describe('FormatDatePipe', () => {
  let pipe: FormatDatePipe;

  beforeEach(() => {
    pipe = new FormatDatePipe();
  });

  it('should create an instance', () => {
    expect(pipe).toBeTruthy();
  });

  it('should format Date object to pt-BR format', () => {
    const date = new Date('2024-01-15');
    const result = pipe.transform(date);
    expect(result).toMatch(/\d{2}\/\d{2}\/\d{4}/);
  });

  it('should format ISO string to pt-BR format', () => {
    const isoString = '2024-01-15T10:30:00Z';
    const result = pipe.transform(isoString);
    expect(result).toMatch(/\d{2}\/\d{2}\/\d{4}/);
  });

  it('should return empty string for null', () => {
    expect(pipe.transform(null as any)).toBe('');
  });

  it('should return empty string for undefined', () => {
    expect(pipe.transform(undefined as any)).toBe('');
  });

  it('should return empty string for empty string', () => {
    expect(pipe.transform('')).toBe('');
  });
});
```

### 5.4. Teste de Guard Funcional

**Cenário**: Criar um guard de autenticação.

**auth.guard.ts**:
```typescript
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = sessionStorage.getItem('auth_token');

  if (token) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};
```

**auth.guard.spec.ts**:
```typescript
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { authGuard } from './auth.guard';

describe('authGuard', () => {
  let router: Router;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: Router,
          useValue: { navigate: jasmine.createSpy('navigate') }
        }
      ]
    });

    router = TestBed.inject(Router);
  });

  afterEach(() => {
    sessionStorage.clear();
  });

  it('should allow access when token exists', () => {
    sessionStorage.setItem('auth_token', 'valid-token');

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as any, {} as any)
    );

    expect(result).toBe(true);
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('should deny access and redirect to login when no token', () => {
    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as any, {} as any)
    );

    expect(result).toBe(false);
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });
});
```

### 5.5. Teste de Directive

**Cenário**: Criar uma diretiva de highlight.

**highlight.directive.ts**:
```typescript
import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  standalone: true
})
export class HighlightDirective {
  @Input() highlightColor = 'yellow';

  constructor(private el: ElementRef) {}

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight(this.highlightColor);
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight('');
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
}
```

**highlight.directive.spec.ts**:
```typescript
import { Component, DebugElement } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { HighlightDirective } from './highlight.directive';

@Component({
  standalone: true,
  imports: [HighlightDirective],
  template: `
    <div appHighlight>Default</div>
    <div appHighlight highlightColor="red">Custom</div>
  `
})
class TestComponent {}

describe('HighlightDirective', () => {
  let fixture: ComponentFixture<TestComponent>;
  let defaultDiv: DebugElement;
  let customDiv: DebugElement;

  beforeEach(() => {
    fixture = TestBed.configureTestingModule({
      imports: [TestComponent]
    }).createComponent(TestComponent);

    fixture.detectChanges();
    defaultDiv = fixture.debugElement.query(By.css('div:first-child'));
    customDiv = fixture.debugElement.query(By.css('div:last-child'));
  });

  it('should create directive instances', () => {
    const directives = fixture.debugElement.queryAll(By.directive(HighlightDirective));
    expect(directives.length).toBe(2);
  });

  it('should highlight with default color on mouseenter', () => {
    defaultDiv.nativeElement.dispatchEvent(new Event('mouseenter'));
    expect(defaultDiv.nativeElement.style.backgroundColor).toBe('yellow');
  });

  it('should highlight with custom color on mouseenter', () => {
    customDiv.nativeElement.dispatchEvent(new Event('mouseenter'));
    expect(customDiv.nativeElement.style.backgroundColor).toBe('red');
  });

  it('should remove highlight on mouseleave', () => {
    defaultDiv.nativeElement.dispatchEvent(new Event('mouseenter'));
    defaultDiv.nativeElement.dispatchEvent(new Event('mouseleave'));
    expect(defaultDiv.nativeElement.style.backgroundColor).toBe('');
  });
});
```

---

## 6. Estratégias de Mock

### 6.1. Mock de HttpClient

**Sempre use `HttpClientTestingModule`**:

```typescript
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

TestBed.configureTestingModule({
  imports: [HttpClientTestingModule]
});

const httpMock = TestBed.inject(HttpTestingController);
```

### 6.2. Mock de Serviços

**Opção 1: Jasmine Spy**:
```typescript
const mockService = jasmine.createSpyObj('ContentService', ['getAll', 'getById']);
mockService.getAll.and.returnValue(of([...]));

TestBed.configureTestingModule({
  providers: [
    { provide: ContentService, useValue: mockService }
  ]
});
```

**Opção 2: Classe Mock**:
```typescript
class MockContentService {
  getAll() {
    return of([...]);
  }
}

TestBed.configureTestingModule({
  providers: [
    { provide: ContentService, useClass: MockContentService }
  ]
});
```

### 6.3. Mock de Router

```typescript
const mockRouter = {
  navigate: jasmine.createSpy('navigate')
};

TestBed.configureTestingModule({
  providers: [
    { provide: Router, useValue: mockRouter }
  ]
});
```

### 6.4. Mock de ActivatedRoute

```typescript
import { of } from 'rxjs';

const mockActivatedRoute = {
  params: of({ id: '123' }),
  queryParams: of({ filter: 'active' })
};

TestBed.configureTestingModule({
  providers: [
    { provide: ActivatedRoute, useValue: mockActivatedRoute }
  ]
});
```

---

## 7. Boas Práticas

### 7.1. Padrão AAA (Arrange-Act-Assert)

Sempre organize testes em três seções:

```typescript
it('should do something', () => {
  // Arrange: preparar dados e mocks
  const input = 'test';
  const expected = 'TEST';

  // Act: executar a ação
  const result = component.transform(input);

  // Assert: verificar resultado
  expect(result).toBe(expected);
});
```

### 7.2. Nomenclatura de Testes

Use nomes descritivos que expliquem o comportamento:

✅ **Bom**:
- `should load courses on initialization`
- `should filter courses by selected category`
- `should display error message when API fails`

❌ **Ruim**:
- `test1()`
- `testLoadCourses()`
- `works()`

### 7.3. Isolamento de Testes

- Cada teste deve ser independente
- Use `beforeEach` para setup comum
- Use `afterEach` para limpeza (ex: `httpMock.verify()`)
- Não compartilhe estado entre testes

### 7.4. Cobertura de Código

**Mínimo recomendado**: 80% de cobertura

**O que testar**:
- ✅ Lógica de negócio
- ✅ Transformações de dados
- ✅ Validações
- ✅ Tratamento de erros
- ✅ Computed signals
- ✅ Métodos públicos

**O que NÃO testar**:
- ❌ Getters/setters simples
- ❌ Interfaces/tipos
- ❌ Código gerado automaticamente

### 7.5. Testes Assíncronos

**Use `done` callback ou `async/await`**:

```typescript
it('should handle async operation', (done) => {
  service.getData().subscribe(data => {
    expect(data).toBeDefined();
    done();
  });
});

// Ou com async/await
it('should handle async operation', async () => {
  const data = await firstValueFrom(service.getData());
  expect(data).toBeDefined();
});
```

---

## 8. Comandos de Execução

### 8.1. Executar Todos os Testes

```bash
npm test
```

### 8.2. Executar com Cobertura

```bash
npm run test:coverage
```

Relatório gerado em: `coverage/index.html`

### 8.3. Executar em Modo Watch

```bash
npm run test:watch
```

### 8.4. Executar para CI/CD

```bash
npm run test:ci
```

---

## 9. Integração com CI/CD

### 9.1. GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:ci
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

### 9.2. Azure DevOps

```yaml
- task: Npm@1
  displayName: 'Install dependencies'
  inputs:
    command: 'ci'

- task: Npm@1
  displayName: 'Run tests'
  inputs:
    command: 'custom'
    customCommand: 'run test:ci'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: '**/TESTS-*.xml'

- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: '$(System.DefaultWorkingDirectory)/coverage/cobertura-coverage.xml'
```

---

## 10. Troubleshooting

### 10.1. Erro: "Cannot find module '@angular/core/testing'"

**Solução**: Instalar dependências de teste:
```bash
npm install --save-dev @angular/core @angular/common @angular/platform-browser-dynamic
```

### 10.2. Erro: "No provider for HttpClient"

**Solução**: Importar `HttpClientTestingModule`:
```typescript
TestBed.configureTestingModule({
  imports: [HttpClientTestingModule]
});
```

### 10.3. Erro: "Expected one matching request, found none"

**Solução**: Verificar URL da requisição e usar `httpMock.expectOne()` corretamente:
```typescript
const req = httpMock.expectOne(url => url.includes('/api/contents'));
```

### 10.4. Testes Lentos

**Soluções**:
- Usar `ChromeHeadless` em vez de `Chrome`
- Reduzir número de testes executados simultaneamente
- Considerar migração para Jest

---

## 11. Checklist de Implementação

Ao implementar testes no projeto, siga este checklist:

- [ ] Alterar `skipTests: false` no `angular.json`
- [ ] Criar `karma.conf.js` com configuração de cobertura
- [ ] Adicionar scripts de teste no `package.json`
- [ ] Criar pelo menos 1 teste para `AppComponent`
- [ ] Criar testes para todos os serviços
- [ ] Criar testes para pipes customizados
- [ ] Criar testes para guards (se existirem)
- [ ] Criar testes para directives (se existirem)
- [ ] Configurar threshold de cobertura mínima (80%)
- [ ] Integrar testes no pipeline de CI/CD
- [ ] Documentar casos de teste complexos

---

## 12. Recursos e Referências

### Documentação Oficial

- [Angular Testing Guide](https://angular.io/guide/testing)
- [Jasmine Documentation](https://jasmine.github.io/)
- [Karma Configuration](https://karma-runner.github.io/latest/config/configuration-file.html)

### Ferramentas

- [Angular Testing Library](https://testing-library.com/docs/angular-testing-library/intro/)
- [Jest for Angular](https://github.com/thymikee/jest-preset-angular)
- [Spectator](https://github.com/ngneat/spectator) (Testing utilities)

---

**Última atualização**: 2026-05-21  
**Versão do documento**: 1.0.0