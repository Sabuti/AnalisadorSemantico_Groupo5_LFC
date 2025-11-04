Relatório Completo da Análise — arq1

Arquivo processado: arq1.txt

------------------------------------------------------------

Linha 1
Código: ((2.0 1.0 +) 5 *)

Tokens: ['(', '(', 'float', 'float', '+', ')', 'int', '*', ')']

Derivação sintática: 22 produções.

Semântico: OK (tipo final: float)

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ OPERACAO (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ OPERACAO (tipo: float)
------------------------------------------------------------


Linha 2
Código: (2 1.5 %)

Tokens: ['(', 'int', 'float', '%', ')']

Derivação sintática: 12 produções.

Erros encontrados (1):
- ERRO SEMÂNTICO [Linha 2]: Operador '%' requer operandos inteiros
Contexto: (int float %)

Árvore atribuída:
PROGRAMA (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ LITERAL (tipo: float)
  ├─ OPERACAO (tipo: int)
------------------------------------------------------------


Linha 3
Código: (3.0 2 |)

Tokens: ['(', 'float', 'int', '|', ')']

Derivação sintática: 12 produções.

Semântico: OK (tipo final: float)

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ OPERACAO (tipo: float)
------------------------------------------------------------


Linha 4
Código: ((23.5 (6.0 2.0 /) -) 5 != (MEM) 3 RES IF)

Tokens: ['(', '(', 'float', '(', 'float', 'float', '/', ')', '-', ')', 'int', '!=', '(', 'ident', ')', 'int', 'res', 'if', ')']

Derivação sintática: 48 produções.

Erros encontrados (3):
- ERRO SEMÂNTICO [Linha 4]: Operador '/' requer operandos inteiros
Contexto: (float float /)
- ERRO SEMÂNTICO [Linha 4]: Variável 'MEM' usada sem declaração prévia
Contexto: (MEM)
- ERRO SEMÂNTICO [Linha 4]: RES(3) referencia linha inexistente

Árvore atribuída:
PROGRAMA (tipo: desconhecido)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ OPERACAO (tipo: int)
  ├─ OPERACAO (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ COMPARACAO (tipo: booleano)
  ├─ LEITURA_VARIAVEL (tipo: desconhecido)
  ├─ LITERAL (tipo: int)
  ├─ RES (tipo: desconhecido)
  ├─ CONDICIONAL_IF (tipo: desconhecido)
------------------------------------------------------------


Linha 5
Código: ((3.0 2 ^) (6 3 /) -)

Tokens: ['(', '(', 'float', 'int', '^', ')', '(', 'int', 'int', '/', ')', '-', ')']

Derivação sintática: 32 produções.

Semântico: OK (tipo final: float)

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ OPERACAO (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ OPERACAO (tipo: int)
  ├─ OPERACAO (tipo: float)
------------------------------------------------------------


Linha 6
Código: (3.14.5 2.0 +)

Erro Léxico: token inválido -> 3.14.5


Linha 7
Código: ((2 3 +) 4 > (1 RES) (0 RES) IF)

Tokens: ['(', '(', 'int', 'int', '+', ')', 'int', '>', '(', 'int', 'res', ')', '(', 'int', 'res', ')', 'if', ')']

Derivação sintática: 45 produções.

Semântico: OK (tipo final: float)

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ OPERACAO (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ COMPARACAO (tipo: booleano)
  ├─ LITERAL (tipo: int)
  ├─ RES (tipo: desconhecido)
  ├─ LITERAL (tipo: int)
  ├─ RES (tipo: float)
  ├─ CONDICIONAL_IF (tipo: float)
------------------------------------------------------------


Linha 8
Código: (1 MEN)

Tokens: ['(', 'int', 'ident', ')']

Derivação sintática: 9 produções.

Semântico: OK (tipo final: int)

Árvore atribuída:
PROGRAMA (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ ATRIBUICAO (tipo: desconhecido)
------------------------------------------------------------


Linha 9
Código: ((2.5 4.1 +) (6.2 1.6 *) -)

Tokens: ['(', '(', 'float', 'float', '+', ')', '(', 'float', 'float', '*', ')', '-', ')']

Derivação sintática: 32 produções.

Semântico: OK (tipo final: float)

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ OPERACAO (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ OPERACAO (tipo: float)
  ├─ OPERACAO (tipo: float)
------------------------------------------------------------


Linha 10
Código: (5 erro)

Erro Léxico: token inválido -> erro


Linha 11
Código: (5 3 > (10 RES) (0 RES) IF)

Tokens: ['(', 'int', 'int', '>', '(', 'int', 'res', ')', '(', 'int', 'res', ')', 'if', ')']

Derivação sintática: 35 produções.

Erros encontrados (1):
- ERRO SEMÂNTICO [Linha 11]: RES(10) referencia linha inexistente

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ COMPARACAO (tipo: booleano)
  ├─ LITERAL (tipo: int)
  ├─ RES (tipo: desconhecido)
  ├─ LITERAL (tipo: int)
  ├─ RES (tipo: float)
  ├─ CONDICIONAL_IF (tipo: float)
------------------------------------------------------------


Linha 12
Código: (MEM)

Tokens: ['(', 'ident', ')']

Derivação sintática: 6 produções.

Erros encontrados (1):
- ERRO SEMÂNTICO [Linha 12]: Memória 'MEM' utilizada sem inicialização
Contexto: (MEM)

Árvore atribuída:
PROGRAMA (tipo: desconhecido)
  ├─ LEITURA_VARIAVEL (tipo: desconhecido)
------------------------------------------------------------


Linha 13
Código: (2 RES)

Tokens: ['(', 'int', 'res', ')']

Derivação sintática: 9 produções.

Semântico: OK (tipo final: float)

Árvore atribuída:
PROGRAMA (tipo: float)
  ├─ LITERAL (tipo: int)
  ├─ RES (tipo: float)
------------------------------------------------------------


Linha 14
Código: (MEN)

Tokens: ['(', 'ident', ')']

Derivação sintática: 6 produções.

Semântico: OK (tipo final: int)

Árvore atribuída:
PROGRAMA (tipo: int)
  ├─ LEITURA_VARIAVEL (tipo: int)
------------------------------------------------------------


Linha 15
Código: (5.0 (3.0 1.5 /) *

Erro Sintático: parêntese aberto sem correspondente.


Linha 16
Código: (5.2 3.5 RES)

Tokens: ['(', 'float', 'float', 'res', ')']

Derivação sintática: 12 produções.

Erros encontrados (1):
- ERRO SEMÂNTICO [Linha 16]: RES requer parâmetro inteiro, recebeu 'float'

Árvore atribuída:
PROGRAMA (tipo: desconhecido)
  ├─ LITERAL (tipo: float)
  ├─ LITERAL (tipo: float)
  ├─ RES (tipo: desconhecido)
------------------------------------------------------------


Linha 17
Código: ( (5 0 >=) (5 1 -) WHILE)

Tokens: ['(', '(', 'int', 'int', '>=', ')', '(', 'int', 'int', '-', ')', 'while', ')']

Derivação sintática: 32 produções.

Semântico: OK (tipo final: int)

Árvore atribuída:
PROGRAMA (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ COMPARACAO (tipo: booleano)
  ├─ LITERAL (tipo: int)
  ├─ LITERAL (tipo: int)
  ├─ OPERACAO (tipo: int)
  ├─ LOOP_WHILE (tipo: int)
------------------------------------------------------------

Resumo Final
Linhas processadas: 17
Símbolos na tabela: 2
Total de erros: 10
