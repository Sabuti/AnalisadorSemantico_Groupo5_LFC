Arvore atribuida da Análise
------------------------------------------------------------

{
  "arquivo": "arq1.txt",
  "linhas_processadas": 17,
  "tabela_simbolos": {
    "MEM": {
      "tipo": "desconhecido",
      "inicializada": false,
      "valor": "X",
      "linha_declaracao": 4,
      "escopo": "global",
      "usada": false,
      "linhas_uso": []
    },
    "MEN": {
      "tipo": "int",
      "inicializada": true,
      "valor": 1,
      "linha_declaracao": 8,
      "escopo": "global",
      "usada": true,
      "linhas_uso": [
        14
      ]
    }
  },
  "total_erros": 10,
  "erros": [
    "ERRO SEMÂNTICO [Linha 2]: Operador '%' requer operandos inteiros\nContexto: (int float %)",
    "ERRO SEMÂNTICO [Linha 4]: Operador '/' requer operandos inteiros\nContexto: (float float /)",
    "ERRO SEMÂNTICO [Linha 4]: Variável 'MEM' usada sem declaração prévia\nContexto: (MEM)",
    "ERRO SEMÂNTICO [Linha 4]: RES(3) referencia linha inexistente",
    "Erro Léxico: token inválido -> 3.14.5",
    "Erro Léxico: token inválido -> erro",
    "ERRO SEMÂNTICO [Linha 11]: RES(10) referencia linha inexistente",
    "ERRO SEMÂNTICO [Linha 12]: Memória 'MEM' utilizada sem inicialização\nContexto: (MEM)",
    "Erro Sintático: parêntese aberto sem correspondente.",
    "ERRO SEMÂNTICO [Linha 16]: RES requer parâmetro inteiro, recebeu 'float'"
  ],
  "arvores": [
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 1,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 2.0,
          "linha": 1
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 1.0,
          "linha": 1
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "+",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "float"
          ],
          "linha": 1
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 5,
          "linha": 1
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "*",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "int"
          ],
          "linha": 1
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "int",
      "linha": 2,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 2,
          "linha": 2
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 1.5,
          "linha": 2
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "%",
          "tipo_inferido": "int",
          "operandos": [
            "int",
            "float"
          ],
          "linha": 2
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 3,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 3.0,
          "linha": 3
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 2,
          "linha": 3
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "|",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "int"
          ],
          "linha": 3
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "desconhecido",
      "linha": 4,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 23.5,
          "linha": 4
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 6.0,
          "linha": 4
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 2.0,
          "linha": 4
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "/",
          "tipo_inferido": "int",
          "operandos": [
            "float",
            "float"
          ],
          "linha": 4
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "-",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "int"
          ],
          "linha": 4
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 5,
          "linha": 4
        },
        {
          "tipo_no": "COMPARACAO",
          "operador": "!=",
          "tipo_inferido": "booleano",
          "operandos": [
            "float",
            "int"
          ],
          "linha": 4
        },
        {
          "tipo_no": "LEITURA_VARIAVEL",
          "tipo_inferido": "desconhecido",
          "nome": "MEM",
          "linha": 4
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 3,
          "linha": 4
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "desconhecido",
          "parametro": 3,
          "linha": 4
        },
        {
          "tipo_no": "CONDICIONAL_IF",
          "tipo_inferido": "desconhecido",
          "tipo_condicao": "booleano",
          "tipos_ramos": [
            "desconhecido",
            "desconhecido"
          ],
          "linha": 4
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 5,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 3.0,
          "linha": 5
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 2,
          "linha": 5
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "^",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "int"
          ],
          "linha": 5
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 6,
          "linha": 5
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 3,
          "linha": 5
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "/",
          "tipo_inferido": "int",
          "operandos": [
            "int",
            "int"
          ],
          "linha": 5
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "-",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "int"
          ],
          "linha": 5
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 7,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 2,
          "linha": 7
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 3,
          "linha": 7
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "+",
          "tipo_inferido": "int",
          "operandos": [
            "int",
            "int"
          ],
          "linha": 7
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 4,
          "linha": 7
        },
        {
          "tipo_no": "COMPARACAO",
          "operador": ">",
          "tipo_inferido": "booleano",
          "operandos": [
            "int",
            "int"
          ],
          "linha": 7
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 1,
          "linha": 7
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "desconhecido",
          "parametro": 1,
          "linha": 7
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 0,
          "linha": 7
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "float",
          "parametro": 0,
          "linha": 7
        },
        {
          "tipo_no": "CONDICIONAL_IF",
          "tipo_inferido": "float",
          "tipo_condicao": "booleano",
          "tipos_ramos": [
            "desconhecido",
            "float"
          ],
          "linha": 7
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "int",
      "linha": 8,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 1,
          "linha": 8
        },
        {
          "tipo_no": "ATRIBUICAO",
          "tipo_inferido": "desconhecido",
          "nome": "MEN",
          "valor": null,
          "linha": 8
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 9,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 2.5,
          "linha": 9
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 4.1,
          "linha": 9
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "+",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "float"
          ],
          "linha": 9
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 6.2,
          "linha": 9
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 1.6,
          "linha": 9
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "*",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "float"
          ],
          "linha": 9
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "-",
          "tipo_inferido": "float",
          "operandos": [
            "float",
            "float"
          ],
          "linha": 9
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 11,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 5,
          "linha": 11
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 3,
          "linha": 11
        },
        {
          "tipo_no": "COMPARACAO",
          "operador": ">",
          "tipo_inferido": "booleano",
          "operandos": [
            "int",
            "int"
          ],
          "linha": 11
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 10,
          "linha": 11
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "desconhecido",
          "parametro": 10,
          "linha": 11
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 0,
          "linha": 11
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "float",
          "parametro": 0,
          "linha": 11
        },
        {
          "tipo_no": "CONDICIONAL_IF",
          "tipo_inferido": "float",
          "tipo_condicao": "booleano",
          "tipos_ramos": [
            "desconhecido",
            "float"
          ],
          "linha": 11
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "desconhecido",
      "linha": 12,
      "filhos": [
        {
          "tipo_no": "LEITURA_VARIAVEL",
          "tipo_inferido": "desconhecido",
          "nome": "MEM",
          "linha": 12
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "float",
      "linha": 13,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 2,
          "linha": 13
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "float",
          "parametro": 2,
          "linha": 13
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "int",
      "linha": 14,
      "filhos": [
        {
          "tipo_no": "LEITURA_VARIAVEL",
          "tipo_inferido": "int",
          "nome": "MEN",
          "linha": 14
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "desconhecido",
      "linha": 16,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 5.2,
          "linha": 16
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "float",
          "valor": 3.5,
          "linha": 16
        },
        {
          "tipo_no": "RES",
          "tipo_inferido": "desconhecido",
          "parametro": 0,
          "linha": 16
        }
      ]
    },
    {
      "tipo_no": "PROGRAMA",
      "tipo_inferido": "int",
      "linha": 17,
      "filhos": [
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 5,
          "linha": 17
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 0,
          "linha": 17
        },
        {
          "tipo_no": "COMPARACAO",
          "operador": ">=",
          "tipo_inferido": "booleano",
          "operandos": [
            "int",
            "int"
          ],
          "linha": 17
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 5,
          "linha": 17
        },
        {
          "tipo_no": "LITERAL",
          "tipo_inferido": "int",
          "valor": 1,
          "linha": 17
        },
        {
          "tipo_no": "OPERACAO",
          "operador": "-",
          "tipo_inferido": "int",
          "operandos": [
            "int",
            "int"
          ],
          "linha": 17
        },
        {
          "tipo_no": "LOOP_WHILE",
          "tipo_inferido": "int",
          "tipo_condicao": "booleano",
          "tipo_corpo": "int",
          "linha": 17
        }
      ]
    }
  ]
}
