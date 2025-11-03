# Integrantes do grupo:
# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
#
# Nome do grupo no Canvas: RA3 5

import sys
import json

EPS = 'E'

# -------------------------
# Função para ler arquivo linha por linha
def lerArquivo(nomeArquivo):
    linhas = []
    try:
        with open(nomeArquivo, 'r', encoding='utf-8') as file:
            for linha in file:
                linha = linha.strip()
                if linha:
                    linhas.append(linha)
    except FileNotFoundError:
        print(f"Erro: arquivo '{nomeArquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None
    return linhas

# -------------------------
# Função para separar tokens em uma linha
def parseExpressao(linha, _tokens_):
    token = ""
    parenteses = 0
    i = 0
    while i < len(linha):
        char = linha[i]
        if char.isspace():
            if token:
                _tokens_.append(token)
                token = ""
        elif char in "()":
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)
            if char == "(":
                parenteses += 1
            else:
                parenteses -= 1
                if parenteses < 0:
                    raise ValueError("Erro Sintático: parêntese fechado sem correspondente.")
        elif char in "+-*/%^":
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)
        elif char == '|':
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)
        elif char in "><=!":
            if token:
                _tokens_.append(token)
                token = ""
            if i + 1 < len(linha) and linha[i + 1] == '=':
                _tokens_.append(char + '=')
                i += 1
            elif char == '<' and i + 1 < len(linha) and linha[i + 1] == '>':
                _tokens_.append('<>')
                i += 1
            else:
                _tokens_.append(char)
        else:
            token += char
        i += 1
    if token:
        _tokens_.append(token)
    if parenteses != 0:
        raise ValueError("Erro Sintático: parêntese aberto sem correspondente.")
    return True

# Funções de estado para o analisador léxico
def estadoNumero(token):
    if not token:
        return False

    if token.count(".") > 1:
        return False
    
    try:
        if token.count(".") == 1:
            float(token)
        else:
            int(token)
        return True
    except ValueError:
        return False

def estadoOperador(token):
    return token in ["+", "-", "*", "|", "/", "%", "^"]

def estadoParenteses(token):
    return token in ["(", ")"]

def estadoComparador(token):
    return token in ["<", ">", "<=", ">=", "==", "!=", "<>"]

def RESorMEM(token):
    if not token:
        return False
    estado = "Q0"
    for ch in token:
        if estado == "Q0":
            if ch.isalpha() and ch.isupper():
                estado = "QID"
            else:
                return False
        elif estado == "QID":
            if not (ch.isalpha() and ch.isupper()) and not ch.isdigit():
                return False
    return estado == "QID"

# -------------------------
# Analisador léxico
def analisadorLexico(tokens_originais):
    tokens_convertidos = []
    tokens_valores = []
    
    for token in tokens_originais:
        if estadoParenteses(token):
            tokens_convertidos.append(token)
            tokens_valores.append(token)
            continue
        if estadoOperador(token):
            tokens_convertidos.append(token)
            tokens_valores.append(token)
            continue
        if estadoComparador(token):
            tokens_convertidos.append(token)
            tokens_valores.append(token)
            continue
        if estadoNumero(token):
            if token.count(".") == 1:
                tokens_convertidos.append("float")
                tokens_valores.append(float(token))
            else:
                tokens_convertidos.append("int")
                tokens_valores.append(int(token))
            continue
        if RESorMEM(token):
            if token == "RES":
                tokens_convertidos.append("res")
                tokens_valores.append(token)
            elif token == "IF":
                tokens_convertidos.append("if")
                tokens_valores.append(token)
            elif token == "WHILE":
                tokens_convertidos.append("while")
                tokens_valores.append(token)
            else:
                tokens_convertidos.append("ident")
                tokens_valores.append(token)
            continue
        raise ValueError(f"Erro Léxico: token inválido -> {token}")
    
    return tokens_convertidos, tokens_valores

# -------------------------
# Funções auxiliares para Tabela de Símbolos
def inicializarTabelaSimbolos():
    return {}

def adicionarSimbolo(tabela, nome, tipo='desconhecido', inicializada=False, valor=None, linha=0, escopo='global'):
    if nome in tabela:
        tabela[nome]['tipo'] = tipo
        tabela[nome]['inicializada'] = inicializada
        tabela[nome]['valor'] = valor
        if not tabela[nome].get('linha_declaracao'):
            tabela[nome]['linha_declaracao'] = linha
    else:
        tabela[nome] = {
            'tipo': tipo,
            'inicializada': inicializada,
            'valor': valor,
            'linha_declaracao': linha,
            'escopo': escopo,
            'usada': False,
            'linhas_uso': [] # Lista para rastrear linhas onde o símbolo é usado
        }
    return tabela

def buscarSimbolo(tabela, nome):
    return tabela.get(nome, None)

def marcarSimboloUsado(tabela, nome, linha):
    if nome in tabela:
        tabela[nome]['usada'] = True
        if 'linhas_uso' not in tabela[nome]:
            tabela[nome]['linhas_uso'] = []
        if linha not in tabela[nome]['linhas_uso']:
            tabela[nome]['linhas_uso'].append(linha)

# -------------------------
# Definição da Gramática de Atributos
def definirGramaticaAtributos():
    regras_semanticas = {
        'operadores_aritmeticos': {
            '+': {'aceita': ['int', 'float'], 'retorna': 'promover'},
            '-': {'aceita': ['int', 'float'], 'retorna': 'promover'},
            '*': {'aceita': ['int', 'float'], 'retorna': 'promover'},
            '|': {'aceita': ['int', 'float'], 'retorna': 'float'},
            '/': {'aceita': ['int'], 'retorna': 'int'},
            '%': {'aceita': ['int'], 'retorna': 'int'},
            '^': {'aceita_base': ['int', 'float'], 'aceita_exp': ['int'], 'retorna': 'promover'}
        },
        'operadores_relacionais': {
            '<': {'aceita': ['int', 'float'], 'retorna': 'booleano'},
            '>': {'aceita': ['int', 'float'], 'retorna': 'booleano'},
            '<=': {'aceita': ['int', 'float'], 'retorna': 'booleano'},
            '>=': {'aceita': ['int', 'float'], 'retorna': 'booleano'},
            '==': {'aceita': ['int', 'float'], 'retorna': 'booleano'},
            '!=': {'aceita': ['int', 'float'], 'retorna': 'booleano'},
            '<>': {'aceita': ['int', 'float'], 'retorna': 'booleano'}
        },
        'estruturas_controle': {
            'if': {'condicao': 'booleano', 'retorna': 'tipo_ramos'},
            'while': {'condicao': 'booleano', 'retorna': 'tipo_corpo'}
        },
        'comandos_especiais': {
            'res': {'parametro': 'int', 'retorna': 'tipo_resultado'},
            'mem_atrib': {'valor': ['int', 'float'], 'retorna': 'tipo_valor'},
            'mem_leitura': {'retorna': 'tipo_memoria'}
        }
    }
    return regras_semanticas

def promoverTipo(tipo1, tipo2):
    if tipo1 == 'float' or tipo2 == 'float':
        return 'float'
    if tipo1 == 'int' and tipo2 == 'int':
        return 'int'
    if tipo1 == 'booleano' or tipo2 == 'booleano':
        return 'booleano'
    return 'desconhecido'

# -------------------------
# Construção da gramática LL(1)
def construirGramatica():
    def is_nonterminal(sym, G):
        return sym in G

    def calcularFirst(G):
        FIRST = {A: set() for A in G}
        changed = True
        while changed:
            changed = False
            for A in G:
                for prod in G[A]:
                    if len(prod) == 0:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS)
                            changed = True
                        continue
                    add_epsilon = True
                    for sym in prod:
                        if sym == EPS:
                            if EPS not in FIRST[A]:
                                FIRST[A].add(EPS)
                                changed = True
                            add_epsilon = False
                            break
                        if not is_nonterminal(sym, G):
                            if sym not in FIRST[A]:
                                FIRST[A].add(sym)
                                changed = True
                            add_epsilon = False
                            break
                        else:
                            before = len(FIRST[A])
                            FIRST[A].update(x for x in FIRST[sym] if x != EPS)
                            if len(FIRST[A]) != before:
                                changed = True
                            if EPS in FIRST[sym]:
                                add_epsilon = True
                            else:
                                add_epsilon = False
                                break
                    if add_epsilon:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS)
                            changed = True
        return FIRST

    def first_of_sequence(seq, FIRST, G):
        result = set()
        if len(seq) == 0:
            result.add(EPS)
            return result
        add_epsilon = True
        for sym in seq:
            if sym == EPS:
                result.add(EPS)
                add_epsilon = False
                break
            if not is_nonterminal(sym, G):
                result.add(sym)
                add_epsilon = False
                break
            else:
                result.update(x for x in FIRST[sym] if x != EPS)
                if EPS in FIRST[sym]:
                    add_epsilon = True
                else:
                    add_epsilon = False
                    break
        if add_epsilon:
            result.add(EPS)
        return result

    def calcularFollow(G, FIRST, start='LINHA'):
        FOLLOW = {A: set() for A in G}
        FOLLOW[start].add('$')
        changed = True
        while changed:
            changed = False
            for A in G:
                for prod in G[A]:
                    for i, B in enumerate(prod):
                        if not is_nonterminal(B, G):
                            continue
                        beta = prod[i+1:]
                        first_beta = first_of_sequence(beta, FIRST, G)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(x for x in first_beta if x != EPS)
                        if EPS in first_beta or len(beta) == 0:
                            FOLLOW[B].update(FOLLOW[A])
                        if len(FOLLOW[B]) != before:
                            changed = True
        return FOLLOW

    def construirTabelaLL1(G, FIRST, FOLLOW):
        table = {}
        conflicts = []
        for A in G:
            for prod in G[A]:
                first_prod = first_of_sequence(prod, FIRST, G)
                for a in (first_prod - {EPS}):
                    key = (A, a)
                    if key in table and table[key] != prod:
                        conflicts.append((key, table[key], prod))
                    else:
                        table[key] = prod
                if EPS in first_prod:
                    for b in FOLLOW[A]:
                        key = (A, b)
                        if key in table and table[key] != prod:
                            conflicts.append((key, table[key], prod))
                        else:
                            table[key] = prod
        return table, conflicts

    G = {}
    G['LINHA'] = [['EXPR']]
    G['EXPR'] = [['(', 'ITEMS', ')']]
    G['ITEMS'] = [['ITEM', 'ITEMS'], [EPS]]
    G['ITEM'] = [['NUMERO'], ['IDENT'], ['OPERADOR'], ['IFKW'], ['WHILEKW'], ['EXPR']]
    G['NUMERO'] = [['float'], ['int']]
    G['IDENT'] = [['ident'], ['res']]
    G['OPERADOR'] = [['+'], ['-'], ['*'], ['/'], ['%'], ['^'], ['|'], 
                     ['>'], ['<'], ['>='], ['<='], ['=='], ['!='], ['<>']]
    G['IFKW'] = [['if']]
    G['WHILEKW'] = [['while']]

    FIRST = calcularFirst(G)
    FOLLOW = calcularFollow(G, FIRST, start='LINHA')
    tabelaLL1, conflitos = construirTabelaLL1(G, FIRST, FOLLOW)

    if conflitos:
        print("Conflitos encontrados na tabela LL(1):")
        for (A, a), prod1, prod2 in conflitos:
            print(f"  Não determinismo para ({A}, {a}): {prod1} e {prod2}")
        raise ValueError("Gramática não é LL(1) devido a conflitos na tabela.")
    
    return G, FIRST, FOLLOW, tabelaLL1

# -------------------------
# Analisador sintático
def analisadorSintatico(tokens, tabelaLL1):
    stack = ['$', 'LINHA']
    derivation = []
    index = 0
    nonterminals = {A for (A, _) in tabelaLL1.keys()}

    def is_nonterminal(sym):
        return sym in nonterminals

    while stack:
        top = stack.pop()
        if index < len(tokens):
            current_token = tokens[index]
        else:
            current_token = '$'
        
        if top == current_token == '$':
            return derivation
        
        if not is_nonterminal(top):
            if top == current_token:
                index += 1
            else:
                raise ValueError(f"Erro Sintático: esperado '{top}', encontrado '{current_token}'")
        else:
            key = (top, current_token)
            if key in tabelaLL1:
                production = tabelaLL1[key]
                derivation.append((top, production))
                for sym in reversed(production):
                    if sym != EPS:
                        stack.append(sym)
            else:
                raise ValueError(f"Erro Sintático: não há produção para {top}, '{current_token}'")
    
    raise ValueError("Erro Sintático: pilha vazia antes do fim dos tokens")

# -------------------------
# Analisador Semântico - Verificação de Tipos
def analisarSemantica(derivacao, tokens_valores, tabela_simbolos, regras_semanticas, historico_resultados, numero_linha):
    erros = []
    arvore_anotada = []
    pilha_tipos = []
    pilha_valores = []
    elementos_expr = []
    idx_valor = 0
    profundidade = 0

    atribuicoes_nomes = set()

    for i, token in enumerate(tokens_valores):
        if token == '(':
            if profundidade == 0:
                elementos_expr = []
            elif profundidade == 1:
                sub_prof = 1
                i += 1
                while i < len(tokens_valores) and sub_prof > 0:
                    if tokens_valores[i] == '(':
                        sub_prof += 1
                    elif tokens_valores[i] == ')':
                        sub_prof -= 1
                    i += 1
                elementos_expr.append(('subexpr', None))
            profundidade += 1

        elif token == ')':
            profundidade -= 1
            if profundidade == 0:
                if len(elementos_expr) == 2: #verificar se é atribuição (len==2 e segundo é ident)
                    tipo1, val1 = elementos_expr[0]
                    tipo2, val2 = elementos_expr[1]
                    if tipo2 == 'ident' and val2 is not None:
                        if tipo1 in ['int', 'float', 'subexpr', 'ident', 'res']:
                            atribuicoes_nomes.add(val2)
                elementos_expr = []

        elif profundidade == 1 and token not in ['(', ')']:
            if isinstance(token, int):
                elementos_expr.append(('int', None))
            elif isinstance(token, float):
                elementos_expr.append(('float', None))
            elif token in ['+', '-', '*', '/', '%', '^', '|', '<', '>', '<=', '>=', '==', '!=', '<>']:
                elementos_expr.append(('op', token))
            elif token in ['RES', 'res']:
                elementos_expr.append(('res', None))
            elif token in ['IF', 'if']:
                elementos_expr.append(('if', None))
            elif token in ['WHILE', 'while']:
                elementos_expr.append(('while', None))
            elif isinstance(token, str):
                elementos_expr.append(('ident', token))
        i += 1

    tokens_processaveis = [v for v in tokens_valores if v not in ['(', ')']]
    memorias_declaradas_nesta_linha = set()
    
    for nao_terminal, producao in derivacao:
        if not producao or producao == [EPS]:
            continue
        
        for simbolo in producao:

            if simbolo in ['(', ')']:
                continue

            if simbolo == 'int':
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                tipo = 'int'
                valor = tokens_processaveis[idx_valor]
                idx_valor += 1

                pilha_tipos.append(tipo)
                pilha_valores.append(valor)
                arvore_anotada.append({
                    'tipo_no': 'LITERAL',
                    'tipo_inferido': tipo,
                    'valor': valor,
                    'linha': numero_linha
                })
            
            elif simbolo == 'float':
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                tipo = 'float'
                valor = tokens_processaveis[idx_valor]
                idx_valor += 1

                pilha_tipos.append(tipo)
                pilha_valores.append(valor)
                arvore_anotada.append({
                    'tipo_no': 'LITERAL',
                    'tipo_inferido': tipo,
                    'valor': valor,
                    'linha': numero_linha
                })
            
            elif simbolo == 'ident':
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                nome = tokens_processaveis[idx_valor]
                idx_valor += 1

                if nome in ['(', ')', '+', '-', '*', '/', '%', '^', '|',
                            '<', '>', '<=', '>=', '==', '!=', '<>', 'IF', 'WHILE', 'RES', 'res']:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: "
                                f"Token sintático '{nome}' tratado como identificador inválido")
                    continue

                eh_atribuicao = nome in atribuicoes_nomes

                if eh_atribuicao:
                    if len(pilha_tipos) < 1:
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Atribuição requer valor")
                        continue
                    tipo_valor = pilha_tipos.pop()
                    valor = pilha_valores.pop() if pilha_valores else None
                    tabela_simbolos = adicionarSimbolo(
                        tabela_simbolos, nome, tipo_valor, True, valor, numero_linha
                    )

                    memorias_declaradas_nesta_linha.add(nome)
                    pilha_tipos.append(tipo_valor)
                    pilha_valores.append(valor)

                    arvore_anotada.append({
                        'tipo_no': 'ATRIBUICAO',
                        'tipo_inferido': 'desconhecido',
                        'nome': nome,
                        'valor': None,
                        'linha': numero_linha
                    })

                else: # Leitura. Exemplo: (MEM)
                    info = buscarSimbolo(tabela_simbolos, nome)
                    if info is None:
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Variável '{nome}' usada sem declaração prévia\nContexto: ({nome})")
                        tipo = 'desconhecido'
                        valor = "X"
                        tipo_valor = 'desconhecido'

                        tabela_simbolos = adicionarSimbolo(
                        tabela_simbolos, nome, tipo_valor, False, valor, numero_linha
                    )
                    elif not info['inicializada']:
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Memória '{nome}' utilizada sem inicialização\nContexto: ({nome})")
                        tipo = info['tipo']
                        valor = "X"
                        tipo_valor = 'desconhecido'

                        tabela_simbolos = adicionarSimbolo(
                        tabela_simbolos, nome, tipo_valor, False, valor, numero_linha
                    )
                    else:
                        tipo = info['tipo']
                        valor = info['valor']
                        marcarSimboloUsado(tabela_simbolos, nome, numero_linha) # Marca o símbolo como usado
                    
                    pilha_tipos.append(tipo)
                    pilha_valores.append(valor)

                    arvore_anotada.append({
                        'tipo_no': 'LEITURA_VARIAVEL',
                        'tipo_inferido': tipo,
                        'nome': nome,
                        'linha': numero_linha
                    })
            
            elif simbolo == 'res':
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                if tokens_processaveis[idx_valor] not in ['RES', 'res']:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Esperado 'RES', encontrado '{tokens_processaveis[idx_valor]}'")
                    idx_valor += 1
                    continue
                    
                idx_valor += 1  # Consome o 'RES'

                if len(pilha_tipos) < 1:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES requer um parâmetro")
                    pilha_tipos.append('desconhecido')
                    pilha_valores.append(None)

                    arvore_anotada.append({
                        'tipo_no': 'RES',
                        'tipo_inferido': 'desconhecido',
                        'parametro': None,
                        'linha': numero_linha
                    })
                    continue

                tipo_param = pilha_tipos.pop()
                n_valor = pilha_valores.pop() if pilha_valores else None

                # Validação de tipo
                if tipo_param != 'int':
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES requer parâmetro inteiro, recebeu '{tipo_param}'")
                    pilha_tipos.append('desconhecido')
                    pilha_valores.append(None)

                    arvore_anotada.append({
                        'tipo_no': 'RES',
                        'tipo_inferido': 'desconhecido',
                        'parametro': 0,
                        'linha': numero_linha
                    })
                    continue

                # Verificação de valor
                if not isinstance(n_valor, int):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES com valor inválido: {n_valor}")
                    pilha_tipos.append('desconhecido')
                    pilha_valores.append(None)

                    arvore_anotada.append({
                        'tipo_no': 'RES',
                        'tipo_inferido': 'desconhecido',
                        'parametro': 0,
                        'linha': numero_linha
                    })
                    continue

                n = int(n_valor)
                if n < 0:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES requer N não negativo")
                    tipo_resultado = 'desconhecido'
                elif n >= len(historico_resultados):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES({n}) referencia linha inexistente")
                    tipo_resultado = 'desconhecido'
                else:
                    idx_resultado = len(historico_resultados) - 1 - n
                    tipo_resultado = historico_resultados[idx_resultado]['tipo']

                pilha_tipos.append(tipo_resultado)
                pilha_valores.append(None)

                arvore_anotada.append({
                    'tipo_no': 'RES',
                    'tipo_inferido': tipo_resultado,
                    'parametro': n,
                    'linha': numero_linha
                })

            elif simbolo in ['+', '-', '*', '/', '%', '^', '|']:
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                idx_valor += 1  # Avança o operador em tokens_valores

                if len(pilha_tipos) < 2:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: "
                                f"Operador '{simbolo}' requer dois operandos\nContexto: operação incompleta")
                    continue
                
                tipo2 = pilha_tipos.pop()
                tipo1 = pilha_tipos.pop()
                pilha_valores.pop()
                pilha_valores.pop()
                
                regra = regras_semanticas['operadores_aritmeticos'][simbolo]
                
                if simbolo == '^':
                    if tipo1 not in regra['aceita_base']:
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Potência requer base int ou float\nContexto: ({tipo1} {tipo2} ^)")
                    if tipo2 != 'int':
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Potência requer expoente inteiro\nContexto: ({tipo1} {tipo2} ^)")
                    tipo_resultado = promoverTipo(tipo1, 'int')
                
                elif simbolo in ['/', '%']:
                    if tipo1 != 'int' or tipo2 != 'int':
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Operador '{simbolo}' requer operandos inteiros\nContexto: ({tipo1} {tipo2} {simbolo})")
                    tipo_resultado = 'int' # retorna int para não causar cascata de erros
                
                elif simbolo == '|':
                    if tipo1 not in regra['aceita'] or tipo2 not in regra['aceita']:
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Divisão float requer operandos numéricos\nContexto: ({tipo1} {tipo2} |)")
                    tipo_resultado = 'float'
                
                else:
                    if tipo1 not in regra['aceita'] or tipo2 not in regra['aceita']:
                        erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Operador '{simbolo}' com tipos incompatíveis\nContexto: ({tipo1} {tipo2} {simbolo})")
                    tipo_resultado = promoverTipo(tipo1, tipo2)
                
                if tipo_resultado == 'desconhecido':
                    pilha_tipos.append('desconhecido')
                    pilha_valores.append(None)
                    continue

                pilha_tipos.append(tipo_resultado)
                pilha_valores.append(None)
                
                arvore_anotada.append({
                    'tipo_no': 'OPERACAO',
                    'operador': simbolo,
                    'tipo_inferido': tipo_resultado,
                    'operandos': [tipo1, tipo2],
                    'linha': numero_linha
                })
            
            elif simbolo in ['<', '>', '<=', '>=', '==', '!=']:
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                idx_valor += 1  # Avança o operador em tokens_valores

                if len(pilha_tipos) < 2:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Operador '{simbolo}' requer dois operandos\nContexto: comparação incompleta")
                    continue
                
                tipo2 = pilha_tipos.pop()
                tipo1 = pilha_tipos.pop()
                pilha_valores.pop()
                pilha_valores.pop()
                
                regra = regras_semanticas['operadores_relacionais'][simbolo]
                
                if tipo1 not in regra['aceita'] or tipo2 not in regra['aceita']:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Comparação '{simbolo}' com tipos incompatíveis\nContexto: ({tipo1} {tipo2} {simbolo})")
                
                tipo_resultado = 'booleano'
                pilha_tipos.append(tipo_resultado)
                pilha_valores.append(None)
                
                arvore_anotada.append({
                    'tipo_no': 'COMPARACAO',
                    'operador': simbolo,
                    'tipo_inferido': tipo_resultado,
                    'operandos': [tipo1, tipo2],
                    'linha': numero_linha
                })
            
            elif simbolo == 'if':
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue

                idx_valor += 1  # Avança o operador em tokens_valores

                if len(pilha_tipos) < 3:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: IF requer condição e dois ramos\nContexto: estrutura IF incompleta")
                    continue
                
                tipo_else = pilha_tipos.pop()
                tipo_then = pilha_tipos.pop()
                tipo_cond = pilha_tipos.pop()
                pilha_valores.pop()
                pilha_valores.pop()
                pilha_valores.pop()
                
                if tipo_cond != 'booleano':
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: IF sem condição de comparação válida\nContexto: condição tipo '{tipo_cond}'")
                
                tipo_resultado = promoverTipo(tipo_then, tipo_else)
                pilha_tipos.append(tipo_resultado)
                pilha_valores.append(None)
                
                arvore_anotada.append({
                    'tipo_no': 'CONDICIONAL_IF',
                    'tipo_inferido': tipo_resultado,
                    'tipo_condicao': tipo_cond,
                    'tipos_ramos': [tipo_then, tipo_else],
                    'linha': numero_linha
                })
            
            elif simbolo == 'while':
                if idx_valor >= len(tokens_processaveis):
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Token inesperado")
                    continue
                
                idx_valor += 1  # Avança o operador em tokens_valores

                if len(pilha_tipos) < 2:
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: WHILE requer condição e corpo\nContexto: estrutura WHILE incompleta")
                    continue
                
                tipo_corpo = pilha_tipos.pop()
                tipo_cond = pilha_tipos.pop()
                pilha_valores.pop()
                pilha_valores.pop()
                
                if tipo_cond != 'booleano':
                    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: WHILE sem condição de comparação válida\nContexto: condição tipo '{tipo_cond}'")
                
                tipo_resultado = tipo_corpo
                pilha_tipos.append(tipo_resultado)
                pilha_valores.append(None)
                
                arvore_anotada.append({
                    'tipo_no': 'LOOP_WHILE',
                    'tipo_inferido': tipo_resultado,
                    'tipo_condicao': tipo_cond,
                    'tipo_corpo': tipo_corpo,
                    'linha': numero_linha
                })

    tipo_final = pilha_tipos[-1] if pilha_tipos else 'desconhecido'
    
    return tabela_simbolos, erros, arvore_anotada, tipo_final, memorias_declaradas_nesta_linha

# -------------------------
# Analisador Semântico - Validação de Memória
def analisarSemanticaMemoria(tabela_simbolos, numero_linha, memorias_declaradas_nesta_linha):
    erros = []
    for nome in memorias_declaradas_nesta_linha:
        if nome in ['(', ')', '+', '-', '*', '/', '%', '^', '|', '<', '>', '<=', '>=', '==', '!=', '<>']:
            continue

        info = tabela_simbolos.get(nome)
        if not info:
            continue

        # 🔹 Se foi uma atribuição (linha de declaração == linha atual), ignora
        if info['linha_declaracao'] == numero_linha:
            continue

        # 🔹 Se foi inicializada, mas nunca usada depois # é pra dar erro?
        #if info['inicializada'] and not info['usada']:
        #    erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: Memória '{nome}' declarada mas não utilizada")

    return erros

# -------------------------
# Analisador Semântico - Validação de Estruturas de Controle
def analisarSemanticaControle(arvore_anotada, numero_linha):
    erros = []
    for no in arvore_anotada:
        if no['tipo_no'] == 'CONDICIONAL_IF':
            if no['tipo_condicao'] != 'booleano':
                erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: IF com condição não booleana")
        elif no['tipo_no'] == 'LOOP_WHILE':
            if no['tipo_condicao'] != 'booleano':
                erros.append(f"ERRO SEMÂNTICO [Linha {numero_linha}]: WHILE com condição não booleana")
    return erros

# -------------------------
# Geração da Árvore Atribuída
def gerarArvoreAtribuida(arvore_anotada, tipo_final, numero_linha):
    arvore_atribuida = {
        'tipo_no': 'PROGRAMA',
        'tipo_inferido': tipo_final,
        'linha': numero_linha,
        'filhos': arvore_anotada
    }
    return arvore_atribuida

# -------------------------
# Geração de Documentação - Gramática de Atributos
def gerarDocGramaticaAtributos(nome_arquivo):
    with open(f"gramatica_atributos_{nome_arquivo}.md", "w", encoding="utf-8") as doc:
        doc.write("# Gramática de Atributos\n\n")
        doc.write("## 1. Tipos de Dados\n\n")
        doc.write("A linguagem suporta três tipos:\n")
        doc.write("- `int`: Números inteiros\n")
        doc.write("- `float`: Números de ponto flutuante\n")
        doc.write("- `booleano`: Resultado de operações relacionais\n\n")
        
        doc.write("## 2. Atributos\n\n")
        doc.write("### Atributos Sintetizados (propagam de baixo para cima):\n")
        doc.write("- `tipo`: O tipo da expressão (int, float, booleano)\n")
        doc.write("- `valor`: O valor calculado da expressão\n\n")
        
        doc.write("### Atributos Herdados (propagam de cima para baixo):\n")
        doc.write("- `escopo`: Nível de escopo da variável\n")
        doc.write("- `inicializada`: Para memórias, indica se foram inicializadas\n\n")
        
        doc.write("## 3. Regras de Produção com Atributos\n\n")
        
        doc.write("### 3.1. Operadores Aritméticos\n\n")
        doc.write("#### Adição de Inteiros\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : int    Γ ⊢ e₂ : int\n")
        doc.write("─────────────────────────────\n")
        doc.write("    Γ ⊢ (e₁ e₂ +) : int\n")
        doc.write("```\n\n")
        
        doc.write("#### Adição com Promoção de Tipo\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂\n")
        doc.write("─────────────────────────────────────\n")
        doc.write("Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)\n")
        doc.write("```\n\n")
        
        doc.write("#### Divisão Real\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁,T₂ ∈ {int, float}\n")
        doc.write("────────────────────────────────────────────────\n")
        doc.write("              Γ ⊢ (e₁ e₂ |) : float\n")
        doc.write("```\n\n")
        
        doc.write("#### Divisão Inteira e Módulo\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : int    Γ ⊢ e₂ : int\n")
        doc.write("─────────────────────────────\n")
        doc.write("   Γ ⊢ (e₁ e₂ /) : int\n")
        doc.write("   Γ ⊢ (e₁ e₂ %) : int\n")
        doc.write("```\n\n")
        
        doc.write("#### Potenciação\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : int    T₁ ∈ {int, float}\n")
        doc.write("───────────────────────────────────────────────\n")
        doc.write("           Γ ⊢ (e₁ e₂ ^) : T₁\n")
        doc.write("```\n\n")
        
        doc.write("### 3.2. Operadores Relacionais\n\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁,T₂ ∈ {int, float}\n")
        doc.write("────────────────────────────────────────────────\n")
        doc.write("        Γ ⊢ (e₁ e₂ op) : booleano\n")
        doc.write("```\n")
        doc.write("onde `op ∈ {<, >, <=, >=, ==, !=}`\n\n")
        
        doc.write("### 3.3. Estruturas de Controle\n\n")
        doc.write("#### Condicional IF\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : T    Γ ⊢ e₃ : T\n")
        doc.write("────────────────────────────────────────────────\n")
        doc.write("        Γ ⊢ (e₁ e₂ e₃ IF) : T\n")
        doc.write("```\n\n")
        
        doc.write("#### Laço WHILE\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : T\n")
        doc.write("───────────────────────────────\n")
        doc.write("    Γ ⊢ (e₁ e₂ WHILE) : T\n")
        doc.write("```\n\n")
        
        doc.write("### 3.4. Comandos Especiais\n\n")
        doc.write("#### Declaração de Variável (MEM)\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e : T    Γ[x ↦ T] ⊢ x inicializada\n")
        doc.write("────────────────────────────────────────\n")
        doc.write("        Γ ⊢ (e x) : T\n")
        doc.write("```\n\n")
        
        doc.write("#### Leitura de Variável\n")
        doc.write("```\n")
        doc.write("Γ(x) = T    x inicializada\n")
        doc.write("───────────────────────────\n")
        doc.write("      Γ ⊢ (x) : T\n")
        doc.write("```\n\n")
        
        doc.write("#### Comando RES\n")
        doc.write("```\n")
        doc.write("Γ ⊢ n : int    n ≥ 0    resultado[n] : T\n")
        doc.write("───────────────────────────────────────────\n")
        doc.write("           Γ ⊢ (n RES) : T\n")
        doc.write("```\n\n")
        
        doc.write("## 4. Função de Promoção de Tipos\n\n")
        doc.write("```\n")
        doc.write("promover_tipo(int, int) = int\n")
        doc.write("promover_tipo(int, float) = float\n")
        doc.write("promover_tipo(float, int) = float\n")
        doc.write("promover_tipo(float, float) = float\n")
        doc.write("```\n\n")

# -------------------------
# Geração de Documentação - Julgamento de Tipos
def gerarDocJulgamentoTipos(arvore_anotada, tipo_final, numero_linha, nome_arquivo):
    with open(f"julgamento_tipos_{nome_arquivo}.md", "w", encoding="utf-8") as doc:
        doc.write("# Julgamento de Tipos\n\n")
        doc.write(f"## Linha {numero_linha}\n\n")
        doc.write(f"**Tipo Final da Expressão:** `{tipo_final}`\n\n")
        
        doc.write("### Derivação de Tipos (passo a passo):\n\n")
        
        for i, no in enumerate(arvore_anotada, 1):
            doc.write(f"**Passo {i}:** {no['tipo_no']}\n")
            doc.write(f"- Tipo inferido: `{no['tipo_inferido']}`\n")
            
            if no['tipo_no'] == 'LITERAL':
                doc.write(f"- Valor: `{no['valor']}`\n")
                doc.write(f"- Regra aplicada: Literal {no['tipo_inferido']}\n")
            
            elif no['tipo_no'] == 'IDENT':
                doc.write(f"- Nome: `{no['nome']}`\n")
                doc.write(f"- Regra aplicada: Leitura de variável\n")
            
            elif no['tipo_no'] == 'ATRIBUICAO':
                doc.write(f"- Nome: `{no['nome']}`\n")
                doc.write(f"- Valor: `{no.get('valor', 'N/A')}`\n")
                doc.write(f"- Regra aplicada: Declaração/Atribuição de variável\n")
            
            elif no['tipo_no'] == 'OPERACAO':
                doc.write(f"- Operador: `{no['operador']}`\n")
                doc.write(f"- Operandos: `{no['operandos'][0]}`, `{no['operandos'][1]}`\n")
                doc.write(f"- Regra aplicada: Operação aritmética ")
                if no['operador'] == '|':
                    doc.write("(divisão float → float)\n")
                elif no['operador'] in ['/', '%']:
                    doc.write("(operação inteira → int)\n")
                elif no['operador'] == '^':
                    doc.write("(potência, expoente int)\n")
                else:
                    doc.write("(promoção de tipos)\n")
            
            elif no['tipo_no'] == 'COMPARACAO':
                doc.write(f"- Operador: `{no['operador']}`\n")
                doc.write(f"- Operandos: `{no['operandos'][0]}`, `{no['operandos'][1]}`\n")
                doc.write(f"- Regra aplicada: Comparação → booleano\n")
            
            elif no['tipo_no'] == 'CONDICIONAL_IF':
                doc.write(f"- Tipo condição: `{no['tipo_condicao']}`\n")
                doc.write(f"- Tipos dos ramos: `{no['tipos_ramos'][0]}`, `{no['tipos_ramos'][1]}`\n")
                doc.write(f"- Regra aplicada: Estrutura condicional IF\n")
            
            elif no['tipo_no'] == 'LOOP_WHILE':
                doc.write(f"- Tipo condição: `{no['tipo_condicao']}`\n")
                doc.write(f"- Tipo corpo: `{no['tipo_corpo']}`\n")
                doc.write(f"- Regra aplicada: Laço WHILE\n")
            
            elif no['tipo_no'] == 'RES':
                doc.write(f"- Parâmetro: `{no['parametro']}`\n")
                doc.write(f"- Regra aplicada: Comando RES (referência a resultado anterior)\n")
            
            doc.write(f"- Linha: {no['linha']}\n\n")

# -------------------------
# Geração de Documentação - Erros Semânticos
def gerarDocErrosSemanticos(todos_erros, nome_arquivo):
    with open(f"erros_semanticos_{nome_arquivo}.md", "w", encoding="utf-8") as doc:
        doc.write("# Erros Semânticos Detectados\n\n")
        
        if not todos_erros:
            doc.write("**Nenhum erro semântico encontrado.**\n\n")
            doc.write("O programa está semanticamente correto:\n")
            doc.write("- Todos os tipos são compatíveis\n")
            doc.write("- Todas as variáveis foram inicializadas antes do uso\n")
            doc.write("- Todas as estruturas de controle estão corretas\n")
        else:
            doc.write(f"**Total de erros encontrados:** {len(todos_erros)}\n\n")
            doc.write("---\n\n")
            
            for i, erro in enumerate(todos_erros, 1):
                doc.write(f"## Erro {i}\n\n")
                doc.write(f"```\n{erro}\n```\n\n")

# -------------------------
# Geração de Documentação - Árvore Atribuída
def gerarDocArvoreAtribuida(arvore_atribuida, nome_arquivo):
    with open(f"arvore_atribuida_{nome_arquivo}.md", "w", encoding="utf-8") as doc:
        doc.write("# Árvore Sintática Abstrata Atribuída\n\n")
        doc.write("## Visualização em Texto\n\n")
        doc.write("```\n")
        doc.write(f"PROGRAMA (tipo: {arvore_atribuida['tipo_inferido']})\n")
        doc.write(f"└─ Linha {arvore_atribuida['linha']}\n")
        
        for i, no in enumerate(arvore_atribuida['filhos']):
            prefixo = "   ├─" if i < len(arvore_atribuida['filhos']) - 1 else "   └─"
            doc.write(f"{prefixo} {no['tipo_no']} (tipo: {no['tipo_inferido']})\n")
        
        doc.write("```\n\n")
        
        doc.write("## Estrutura Detalhada (JSON)\n\n")
        doc.write("```json\n")
        doc.write(json.dumps(arvore_atribuida, indent=2, ensure_ascii=False))
        doc.write("\n```\n\n")
    
    # Também salva em JSON puro
    with open(f"arvore_atribuida_{nome_arquivo}.json", "w", encoding="utf-8") as json_file:
        json.dump(arvore_atribuida, json_file, indent=2, ensure_ascii=False)

# -------------------------
# Geração de Documentação - Tabela de Símbolos
def gerarDocTabelaSimbolos(tabela_simbolos, nome_arquivo):
    
    with open(f"tabela_memoria_{nome_arquivo}.md", "w", encoding="utf-8") as doc:
        doc.write("# Tabela de Símbolos\n\n")
        doc.write("Armazena informações sobre a memória do programa.\n\n")
        
        tokens_sintaticos = {'(', ')', '+', '-', '*', '/', '%', '^', '|', '<', '>', '<=', '>=', '==', '!=', '<>', 'IF', 'WHILE', 'RES'}
        simbolos_validos = {k: v for k, v in tabela_simbolos.items() if k not in tokens_sintaticos}

        if not simbolos_validos:
            doc.write("*Tabela vazia - nenhuma variável declarada*\n\n")
        else:
            for simbolo, info in sorted(simbolos_validos.items(), key=lambda x: str(x[0])):
                valor = str(info['valor']) if info['valor'] is not None else "N/A"
                escopo = info.get('escopo', 'global')
                doc.write(f"--------------------------------------------------------------------\n")
                doc.write(f"Simbolo: {simbolo} \n Tipo: {info['tipo']} \n")
                doc.write(f"Inicializada: {'Sim' if info['inicializada'] else 'Não'} \n")
                doc.write(f"Valor: {valor} \n Linha declarada: {info.get('linha_declaracao', 'N/A')}  \n")
                doc.write(f"Escopo: {escopo} {'Sim' if info['usada'] else 'Não'} \n")
            
            doc.write(f"\n**Total de símbolos:** {len(tabela_simbolos)}\n")

def main():
    if len(sys.argv) < 2:
        print("Uso correto: python trabalho.py <arquivo_de_entrada>")
        print("Exemplo: python trabalho.py teste1.txt")
        return

    caminho = sys.argv[1]
    nome_base = caminho.split('.')[0]

    # Lê o arquivo de entrada
    linhas = lerArquivo(caminho)
    if linhas is None:
        return

    # Estruturas principais
    tabela_simbolos = inicializarTabelaSimbolos()
    historico_resultados = []
    todos_erros = []
    todas_arvores = []

    # Define as regras semânticas
    regras_semanticas = definirGramaticaAtributos()

    # Constrói a gramática LL(1)
    try:
        G, FIRST, FOLLOW, tabelaLL1 = construirGramatica()
        print("Gramática LL(1) construída com sucesso.")
    except Exception as e:
        print(f"Erro ao construir a gramática: {e}")
        return

    # Gera documentação da gramática de atributos
    gerarDocGramaticaAtributos(nome_base)
    print(f"Arquivo 'gramatica_atributos_{nome_base}.txt' criado com sucesso.\n")

    # Nomes dos arquivos de saída
    relatorio_nome = f"relatorio_completo_{nome_base}.txt"
    json_nome = f"arvore_atribuida_e_erros_{nome_base}.txt"

    with open(relatorio_nome, "w", encoding="utf-8") as rel:
        rel.write(f"Relatório Completo da Análise — {nome_base}\n\n")
        rel.write(f"Arquivo processado: {caminho}\n\n")
        rel.write("-" * 60 + "\n")

        print("Iniciando análise do arquivo...\n")

        # Processa cada linha do arquivo
        for numero_linha, linha in enumerate(linhas, start=1):
            print(f"Analisando linha {numero_linha}: {linha}")
            rel.write(f"\nLinha {numero_linha}\n")
            rel.write(f"Código: {linha}\n\n")

            try:
                # Etapa 1: Análise Léxica
                tokens_originais = []
                parseExpressao(linha, tokens_originais)
                tokens, tokens_valores = analisadorLexico(tokens_originais)
                rel.write(f"Tokens: {tokens}\n\n")
                print(f"  - Análise léxica concluída ({len(tokens)} tokens).")

                # Etapa 2: Análise Sintática
                derivacao = analisadorSintatico(tokens, tabelaLL1)
                rel.write(f"Derivação sintática: {len(derivacao)} produções.\n\n")
                print(f"  - Análise sintática concluída ({len(derivacao)} produções).")

                # Etapa 3: Análise Semântica
                tabela_simbolos, erros, arvore_anotada, tipo_final, memorias_declaradas_nesta_linha = analisarSemantica(
                    derivacao, tokens_valores, tabela_simbolos,
                    regras_semanticas, historico_resultados, numero_linha
                )

                # Validações adicionais
                erros.extend(analisarSemanticaMemoria(tabela_simbolos, numero_linha, memorias_declaradas_nesta_linha))
                erros.extend(analisarSemanticaControle(arvore_anotada, numero_linha))

                # Gera árvore atribuída consolidada
                arvore_atribuida = gerarArvoreAtribuida(arvore_anotada, tipo_final, numero_linha)
                todas_arvores.append(arvore_atribuida)

                # Atualiza histórico (para comandos RES)
                historico_resultados.append({
                    'linha': numero_linha,
                    'tipo': tipo_final,
                    'arvore': arvore_atribuida
                })

                # Resultados da linha
                if erros:
                    rel.write(f"Erros encontrados ({len(erros)}):\n")
                    for e in erros:
                        rel.write(f"- {e}\n")
                        todos_erros.append(e)
                    print(f"  - {len(erros)} erro(s) encontrado(s).")
                else:
                    rel.write(f"Semântico: OK (tipo final: {tipo_final})\n")
                    print("  - Análise semântica concluída sem erros.")

                # Árvore atribuída (resumo)
                rel.write("\nÁrvore atribuída:\n")
                rel.write(f"PROGRAMA (tipo: {tipo_final})\n")
                for no in arvore_atribuida['filhos']:
                    rel.write(f"  ├─ {no['tipo_no']} (tipo: {no['tipo_inferido']})\n")
                rel.write("-" * 60 + "\n\n")

            except ValueError as e:
                msg = str(e)
                rel.write(f"{msg}\n\n")
                todos_erros.append(msg)
                print(f"  - {msg}")

        # Resumo final no relatório
        rel.write("Resumo Final\n")
        rel.write(f"Linhas processadas: {len(linhas)}\n")
        rel.write(f"Símbolos na tabela: {len(tabela_simbolos)}\n")
        rel.write(f"Total de erros: {len(todos_erros)}\n")

    # Gera os arquivos auxiliares (.txt)
    gerarDocErrosSemanticos(todos_erros, nome_base)
    gerarDocTabelaSimbolos(tabela_simbolos, nome_base)

    # Cria o arquivo consolidado (antes era .json)
    dados_json = {
        "arquivo": caminho,
        "linhas_processadas": len(linhas),
        "tabela_simbolos": tabela_simbolos,
        "total_erros": len(todos_erros),
        "erros": todos_erros,
        "arvores": todas_arvores
    }

    # Grava o “JSON” formatado em texto
    with open(json_nome, "w", encoding="utf-8") as fjson:
        fjson.write("Arvore atribuida da Análise\n")
        fjson.write("-" * 60 + "\n\n")
        fjson.write(json.dumps(dados_json, indent=2, ensure_ascii=False))
        fjson.write("\n")

    # Exibe resumo final no terminal
    print("\nAnálise concluída.")
    print(f"Relatório detalhado: {relatorio_nome}")
    print(f"Arquivo Arvore atribuida: {json_nome}")
    print(f"Tabela de memória: tabela_memoria_{nome_base}.txt")
    print(f"Erros semânticos: erros_semanticos_{nome_base}.txt\n")

    if todos_erros:
        print("A análise foi concluída com erros. Verifique os relatórios para mais detalhes.")
    else:
        print("A análise foi concluída com sucesso, sem erros encontrados.")


if __name__ == "__main__":
    main()