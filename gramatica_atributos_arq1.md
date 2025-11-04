# Gramática de Atributos

## 1. Tipos de Dados

A linguagem suporta três tipos:
- `int`: Números inteiros
- `float`: Números de ponto flutuante
- `booleano`: Resultado de operações relacionais

## 2. Atributos

### Atributos Sintetizados (propagam de baixo para cima):
- `tipo`: O tipo da expressão (int, float, booleano)
- `valor`: O valor calculado da expressão

### Atributos Herdados (propagam de cima para baixo):
- `escopo`: Nível de escopo da variável
- `inicializada`: Para memórias, indica se foram inicializadas

## 3. Regras de Produção com Atributos

### 3.1. Operadores Aritméticos

#### Adição de Inteiros
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ +) : int
```

#### Adição com Promoção de Tipo
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂
─────────────────────────────────────
Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)
```

#### Divisão Real
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁,T₂ ∈ {int, float}
────────────────────────────────────────────────
              Γ ⊢ (e₁ e₂ |) : float
```

#### Divisão Inteira e Módulo
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
   Γ ⊢ (e₁ e₂ /) : int
   Γ ⊢ (e₁ e₂ %) : int
```

#### Potenciação
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : int    T₁ ∈ {int, float}
───────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ ^) : T₁
```

### 3.2. Operadores Relacionais

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁,T₂ ∈ {int, float}
────────────────────────────────────────────────
        Γ ⊢ (e₁ e₂ op) : booleano
```
onde `op ∈ {<, >, <=, >=, ==, !=}`

### 3.3. Estruturas de Controle

#### Condicional IF
```
Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : T    Γ ⊢ e₃ : T
────────────────────────────────────────────────
        Γ ⊢ (e₁ e₂ e₃ IF) : T
```

#### Laço WHILE
```
Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : T
───────────────────────────────
    Γ ⊢ (e₁ e₂ WHILE) : T
```

### 3.4. Comandos Especiais

#### Declaração de Variável (MEM)
```
Γ ⊢ e : T    Γ[x ↦ T] ⊢ x inicializada
────────────────────────────────────────
        Γ ⊢ (e x) : T
```

#### Leitura de Variável
```
Γ(x) = T    x inicializada
───────────────────────────
      Γ ⊢ (x) : T
```

#### Comando RES
```
Γ ⊢ n : int    n ≥ 0    resultado[n] : T
───────────────────────────────────────────
           Γ ⊢ (n RES) : T
```

## 4. Função de Promoção de Tipos

```
promover_tipo(int, int) = int
promover_tipo(int, float) = float
promover_tipo(float, int) = float
promover_tipo(float, float) = float
```

