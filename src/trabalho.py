# Integrantes do grupo:
# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
#
# Nome do grupo no Canvas: RA3 5

## Precisa ter
# Arquivos de texto = X
# Utilizar arvore sintatica do Trabalho 2 = Sim
# Criar gramática de atributos = X
# Implementar analisador semântico para gerar árvore abstrata = X
# Gerar doc de analise semântica = X
# Detectar erros léxicos, sintáticos e semânticos = X

# Não precisa gerar código Assembly

import sys # import para gerenciar argumentos de linha de comando
import json

EPS = 'E' # símbolo para epsilon / vazio

# -------------------------
# Função para ler arquivo linha por linha
def lerArquivo(nomeArquivo, linhas):
    try:
        with open(nomeArquivo, 'r') as file:
            for linha in file:
                linha = linha.strip()
                if linha:  # Ignorar linhas vazias
                    linhas.append(linha)
    except FileNotFoundError:
        print(f"Erro: arquivo '{nomeArquivo}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return
    return linhas

# -------------------------
# Função para separar tokens em uma linha
def parseExpressao(linha, _tokens_): ## revisar erro daqui
    token = ""
    parenteses = 0
    i = 0
    while i < len(linha):
        char = linha[i]
        if char.isspace():  # espaço em branco
            if token:
                _tokens_.append(token)
                token = ""
        elif char in "()":  # parênteses
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
        elif char in "+-*/%^":  # operadores
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)

        elif char == '|':  # operador raiz quadrada
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)

        elif char in "><=!":
            if token:
                _tokens_.append(token)
                token = ""
            # Verifica se é um operador composto (<=, >=)
            if i + 1 < len(linha) and linha[i + 1] == '=':
                _tokens_.append(char + '=')
                i += 1
            elif char == '<' and i + 1 < len(linha) and linha[i + 1] == '>':
                _tokens_.append('<>')
                i += 1
            else:
                _tokens_.append(char)
        else:  # acumula números ou comandos (ex: MEM, RES)
            token += char
        i += 1
    if token:
        _tokens_.append(token)
    if parenteses != 0:
        raise ValueError("Erro Sintático: parêntese aberto sem correspondente.")
    return True

#funções de estado para o analisador léxico
def estadoNumero(token):
    if not token:
        return False
    try:
        if token.count(".") > 1: # Checa se há mais de um ponto decimal
            return False
        return True
    except ValueError:
        return False
    
def estadoOperador(token):
    match token:
        case "+" | "-" | "*" | "|" | "/" | "%" | "^":
            return True
        case _:
            return False

def estadoParenteses(token):
    match token:
        case "(" | ")":
            return True
        case _:
            return False
        
def estadoComparador(token):
    match token:
        case "<" | ">" | "<=" | ">=" | "==" | "!=" | "<>": 
            return True
        case _:
            return False

# AFD: identificadores/COMANDOS (RES/MEM)
def RESorMEM(token):
    if not token:
        return False

    estado = "Q0"  # Q0(início), QID
    for ch in token:
        match estado:
            case "Q0":
                if ch.isalpha() and ch.isupper():
                    estado = "QID"
                else:
                    return False
            case "QID":
                if ch.isalpha() and ch.isupper():
                    pass
                elif ch.isdigit():
                    pass
                else:
                    return False

        return True

# -------------------------
# Analisador léxico: valida CADA token isoladamente
def analisadorLexico(tokens):
    tokens_convertidos = []
    tokens_valores = []

    for token in tokens:
        if estadoParenteses(token):
            tokens_convertidos.append(token)
            tokens_valores.append(token)
            continue
        if estadoOperador(token):
            tokens_convertidos.append(token)
            tokens_valores.append(token)
            continue
        if estadoNumero(token):
            if token.count(".") == 1:
                token = float(token)
                tokens_convertidos.append("float")
                tokens_valores.append(float(token))
            else:
                token = int(token)
                tokens_convertidos.append("int")
                tokens_valores.append(int(token))
            continue
        if estadoComparador(token):
            tokens_convertidos.append(token)
            tokens_valores.append(token)
            continue
        if RESorMEM(token):
            if token == "RES":
                tokens_convertidos.append("res")  # converte comando RES para token 'res'
                tokens_valores.append(token)
            elif token == "IF":
                tokens_convertidos.append("if") # converte comando IF para token 'if'
                tokens_valores.append(token)
            elif token == "WHILE":
                tokens_convertidos.append("while") # converte comando WHILE para token 'while'
                tokens_valores.append(token)
            else:
                tokens_convertidos.append("ident")  # converte outros identificadores para token 'ident'
                tokens_valores.append(token)
            continue

        # Se não passou em nada, é inválido
        raise ValueError(f"Erro léxico: token inválido -> {token}")

    return tokens_convertidos, tokens_valores

def inicializarTabelaSimbolos():
    """Inicializa a tabela de símbolos vazia"""
    return {}

def adicionarSimbolo(tabela, nome, tipo='desconhecido', inicializada=False, valor=None, linha = 0):
    """Adiciona um símbolo à tabela de símbolos"""
    tabela[nome] = {
        'tipo': tipo,
        'inicializada': inicializada,
        'valor': valor,
        'linha': linha,
        'usada': False
    }
    return tabela

def buscarSimbolo(tabela, nome):
    """Busca um símbolo na tabela de símbolos"""
    return tabela.get(nome, None)



def inicializarMemoria():
    """Inicializa a memória vazia"""
    return {}

def buscarSimbolo(tabela, nome):
    """Busca um símbolo na tabela de símbolos"""
    return tabela.get(nome, None)

def adicionarMemoria(memoria, nome, tipo='desconhecido', inicializada=False):
    """Adiciona um item à memória"""
    memoria[nome] = {
        'tipo': tipo,
        'inicializada': inicializada,
        'usada': False
    }
    return memoria





# --------------------------
# Analisador sintático: constrói a gramática, tabela LL(1)
def construirGramatica():

    def is_nonterminal(sym, G):
        return sym in G # true se sym é um não-terminal em G, false é terminal

    def calcularFirst(G):
        FIRST = {A: set() for A in G} # inicializa FIRST para cada não-terminal com conjuntos vazios
        changed = True
        while changed:
            changed = False
            for A in G: # para cada não-terminal A. Ex: G['EXPR']
                for prod in G[A]: # para cada produção de A. Ex = [['(', 'RPN_SEQ', ')']]
                    if len(prod) == 0:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS); changed = True
                        continue
                    add_epsilon = True
                    for sym in prod: # para cada símbolo na produção. Ex: sym = '(' ou 'RPN_SEQ'
                        if sym == EPS:
                            if EPS not in FIRST[A]:
                                FIRST[A].add(EPS); changed = True
                            add_epsilon = False; break
                        if not is_nonterminal(sym, G):
                            if sym not in FIRST[A]:
                                FIRST[A].add(sym); changed = True
                            add_epsilon = False; break
                        else:
                            before = len(FIRST[A])
                            FIRST[A].update(x for x in FIRST[sym] if x != EPS)
                            if len(FIRST[A]) != before: changed = True
                            if EPS in FIRST[sym]:
                                add_epsilon = True
                            else:
                                add_epsilon = False; break
                    if add_epsilon:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS); changed = True
        return FIRST

    def first_of_sequence(seq, FIRST, G):
        result = set()
        if len(seq) == 0:
            result.add(EPS); 
            return result
        add_epsilon = True
        for sym in seq:
            if sym == EPS:
                result.add(EPS); add_epsilon = False; break
            if not is_nonterminal(sym, G):
                result.add(sym); add_epsilon = False; break
            else:
                result.update(x for x in FIRST[sym] if x != EPS)
                if EPS in FIRST[sym]:
                    add_epsilon = True
                else:
                    add_epsilon = False; break
        if add_epsilon: 
            result.add(EPS)
        return result

    def calcularFollow(G, FIRST, start='LINHA'):
        FOLLOW = {A: set() for A in G} # inicializa FOLLOW para cada não-terminal com conjuntos vazios
        FOLLOW[start].add('$')
        changed = True
        while changed:
            changed = False
            for A in G: # para cada não-terminal A. Ex: G['EXPR']
                for prod in G[A]: # para cada produção de A. Ex = [['(', 'RPN_SEQ', ')']]
                    for i, B in enumerate(prod): # para cada símbolo na produção. Ex: B = '(' ou 'RPN_SEQ'
                        if not is_nonterminal(B, G): continue
                        beta = prod[i+1:] # tudo depois de B atual
                        first_beta = first_of_sequence(beta, FIRST, G)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(x for x in first_beta if x != EPS)
                        if EPS in first_beta or len(beta) == 0:
                            FOLLOW[B].update(FOLLOW[A])
                        if len(FOLLOW[B]) != before: changed = True
        return FOLLOW

    def construirTabelaLL1(G, FIRST, FOLLOW):
        table = {}
        conflicts = []
        for A in G: # para cada não-terminal A. Ex: G['EXPR']
            for prod in G[A]: # para cada produção de A. Ex = [['(', 'RPN_SEQ', ')']]
                first_prod = first_of_sequence(prod, FIRST, G)
                for a in (first_prod - {EPS}): # para cada terminal em FIRST(produção)
                    key = (A, a) # chave da tabela LL(1)
                    if key in table and table[key] != prod:
                        conflicts.append((key, table[key], prod))
                    else:
                        table[key] = prod
                if EPS in first_prod:
                    for b in FOLLOW[A]:
                        key = (A, b)
                        if key in table and table[key] != prod: # já existe outra produção para (A, b)
                            conflicts.append((key, table[key], prod))
                        else:
                            table[key] = prod
        return table, conflicts

    G = {} # construção da gramática usando dicionário
    G['LINHA'] = [['EXPR']]
    G['EXPR']  = [['(', 'ITEMS', ')']]
    G['ITEMS'] = [['ITEM', 'ITEMS'], [EPS]]
    G['ITEM'] = [['NUMERO'], ['IDENT'], ['OPERADOR'], ['IFKW'], ['WHILEKW'], ['EXPR']]
    G['NUMERO'] = [['float'], ['int']]    # token lexical 'float' ou 'int'
    G['IDENT']  = [['ident']]   # token lexical 'ident' (men/MEM/RES etc.)
    G['OPERADOR'] = [['+'], ['-'], ['*'], ['/'], ['%'], ['^'], ['|'], ['>'], ['<'], ['>='], ['<='], ['=='], ['!='], ['res']] 
    G['IFKW'] = [['if']]        # será token 'if'
    G['WHILEKW'] = [['while']]  # será token 'while'

    FIRST = calcularFirst(G)
    FOLLOW = calcularFollow(G, FIRST, start='LINHA')
    tabelaLL1, conflitos = construirTabelaLL1(G, FIRST, FOLLOW)

    if conflitos:
        print("Conflitos encontrados na tabela LL(1):")
        for (A, a), prod1, prod2 in conflitos:
            print(f"  Não determinismo para ({A}, {a}): {prod1} e {prod2}")
        raise ValueError("Gramática não é LL(1) devido a conflitos na tabela.")
    else:
        print("Gramática é LL(1).")
        return G, FIRST, FOLLOW, tabelaLL1

# Definição da Gramática de Atributos
def definirGramaticaAtributos():
    """
    Define a gramática de atributos da linguagem.
    Retorna as regras semânticas para verificação de tipos.
    """
    regras_semanticas = {
        'operadores_aritmeticos': {
            '+': {'aceita': ['int', 'real'], 'retorna': 'promover'},
            '-': {'aceita': ['int', 'real'], 'retorna': 'promover'},
            '*': {'aceita': ['int', 'real'], 'retorna': 'promover'},
            '|': {'aceita': ['int', 'real'], 'retorna': 'real'},  # Divisão real sempre retorna real
            '/': {'aceita': ['int'], 'retorna': 'int'},  # Divisão inteira
            '%': {'aceita': ['int'], 'retorna': 'int'},  # Módulo
            '^': {'aceita_base': ['int', 'real'], 'aceita_exp': ['int'], 'retorna': 'promover'}
        },
        'operadores_relacionais': {
            '<': {'aceita': ['int', 'real'], 'retorna': 'booleano'},
            '>': {'aceita': ['int', 'real'], 'retorna': 'booleano'},
            '<=': {'aceita': ['int', 'real'], 'retorna': 'booleano'},
            '>=': {'aceita': ['int', 'real'], 'retorna': 'booleano'},
            '==': {'aceita': ['int', 'real'], 'retorna': 'booleano'},
            '!=': {'aceita': ['int', 'real'], 'retorna': 'booleano'},
            '<>': {'aceita': ['int', 'real'], 'retorna': 'booleano'}
        },
        'estruturas_controle': {
            'if': {'condicao': 'booleano', 'retorna': 'tipo_ramos'},
            'while': {'condicao': 'booleano', 'retorna': 'tipo_corpo'}
        },
        'comandos_especiais': {
            'res': {'parametro': 'int', 'retorna': 'tipo_resultado'},
            'mem_atrib': {'valor': ['int', 'real'], 'retorna': 'tipo_valor'},
            'mem_leitura': {'retorna': 'tipo_memoria'}
        }
    }
    
    return regras_semanticas

def promoverTipo(tipo1, tipo2):
    """Promoção de tipos: se um é real, o resultado é real"""
    if tipo1 == 'real' or tipo2 == 'real':
        return 'real'
    if tipo1 == 'int' and tipo2 == 'int':
        return 'int'
    if tipo1 == 'booleano' or tipo2 == 'booleano':
        return 'booleano'
    return 'desconhecido'
# --------------------------
# Analisador sintático: processa tokens usando a tabela LL(1)
def analisadorSintatico(tokens, tabelaLL1): # entrada: vetor de tokens, tabelaLL1
    stack = ['$', 'LINHA'] # pilha inicial com símbolo de início e marcador de fim
    derivation = [] # para armazenar a sequência de derivações
    index = 0 # índice para rastrear a posição atual nos tokens   
    nonterminals = {A for (A, _) in tabelaLL1.keys()} 

    def is_nonterminal(sym):
        return sym in nonterminals # true se sym é um não-terminal em G, false é terminal

    while stack:
        top = stack.pop() # obtém o símbolo do topo da pilha
        if index < len(tokens):
            current_token = tokens[index] # token atual a ser processado
        else:
            current_token = '$' # marcador de fim de entrada
        
        if top == current_token == '$':
            return derivation # análise sintática bem-sucedida
        
        if not is_nonterminal(top): # se o topo é um terminal
            if top == current_token: # se coincidem, consome o token
                index += 1
            else:
                raise ValueError(f"Erro Sintático: esperado '{top}', encontrado '{current_token}'")
        else: # topo é um não-terminal
            key = (top, current_token)
            if key in tabelaLL1:
                production = tabelaLL1[key]
                derivation.append((top, production)) # registra a produção usada
                for sym in reversed(production): # empilha a produção na ordem inversa
                    if sym != EPS: # não empilha epsilon
                        stack.append(sym)
            else:
                raise ValueError(f"Erro Sintático: não há produção para {top}, '{current_token}'")
    raise ValueError("Erro Sintático: pilha vazia antes do fim dos tokens")

def analisadorSemantico(derivacao, tokens_valores, tabela_simbolos, regras_semanticas, historico_resultados, numero_linha):
    """
    Executa a análise semântica sobre a derivação gerada pelo analisador sintático.
    Retorna: memoria_atualizada, erros_semanticos, arvore_abstrata
    """
    erros_semanticos = []
    arvore_abstrata = []
    pilha_tipos = []
    pilha_valores = []
    indx = 1

    for nao_terminal, producao in derivacao:
        if not producao or producao == [EPS]:
            continue
        
        for simbolo in producao:
            if simbolo == 'int':
                tipo = 'int'
                valor = tokens_valores[indx]
                indx += 1
                pilha_tipos.append(tipo)
                pilha_valores.append(valor)
                arvore_abstrata.append({
                    'tipo': tipo,
                    'valor': valor,
                    'linha': numero_linha
                })
            if simbolo == 'float':
                tipo = 'float'
                valor = tokens_valores[indx]
                indx += 1
                pilha_tipos.append(tipo)
                pilha_valores.append(valor)
                arvore_abstrata.append({
                    'tipo': tipo,
                    'valor': valor,
                    'linha': numero_linha
                })
            elif simbolo == 'ident':
                nome = tokens_valores[indx]
                indx += 1
                if len(pilha_tipos) > 0:
                    tipo = pilha_tipos.pop()
                    valor = pilha_valores[-1] if len(pilha_valores) > 0 else None
                    tabela_simbolos = adicionarSimbolo(tabela_simbolos, nome, tipo, True, valor, numero_linha)
                    arvore_abstrata.append({
                        'tipo': tipo,
                        'nome': nome,
                        'valor': valor,
                        'linha': numero_linha
                    })
                else:
                    info = buscarSimbolo(tabela_simbolos, nome)
                    if info is None:
                        erros_semanticos.append(f"Linha {numero_linha}: Uso de identificador não declarado '{nome}'.")
                        tipo = 'desconhecido'
                        valor = None
                    elif not info['inicializada']:
                        erros_semanticos.append(f"Linha {numero_linha}: Uso de identificador não inicializado '{nome}'.")
                        tipo = info['tipo']
                        valor = None
                    else:
                        tipo = info['tipo']
                        valor = info['valor']
                        tabela_simbolos[nome]['usada'] = True
                    pilha_tipos.append(tipo)
                    pilha_valores.append(valor)
                    arvore_abstrata.append({
                        'tipo': tipo,
                        'nome': nome,
                        'valor': valor,
                        'linha': numero_linha
                    })
            elif simbolo == 'res':
                if len(pilha_tipos) > 0:
                    if pilha_tipos[-1] != 'int':
                        erros_semanticos.append(f"Linha {numero_linha}: Comando RES espera um parâmetro do tipo 'int', mas recebeu '{pilha_tipos[-1]}'.")
                    else:
                        n = int(pilha_valores.pop())
                        if n < 1 or n > len(historico_resultados):
                            erros_semanticos.append(f"Linha {numero_linha}: Comando RES com índice fora do intervalo: {n}.")
                            tipo = 'desconhecido'
                        elif n >= len(historico_resultados):
                            erros_semanticos.append(f"Linha {numero_linha}: Comando RES com índice igual ao tamanho do histórico: {n}.")
                            tipo = 'desconhecido'
                        else:
                            indx = len(historico_resultados) - n
                            tipo = historico_resultados[indx][tipo]

                    pilha_tipos.pop()  # remove o tipo do parâmetro
                    pilha_valores.pop()  # remove o valor do parâmetro
                    pilha_tipos.append(tipo)
                    pilha_valores.append(None)  # valor desconhecido

                    arvore_abstrata.append({
                        'tipo': tipo,
                        'comando': 'res',
                        'parametro': n,
                        'linha': numero_linha
                    })
                
                elif simbolo in {'+', '-', '*', '/', '%', '^', '|'}:
                    if len(pilha_tipos) < 2:
                        erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' requer dois operandos.")
                        continue

                    tipo2 = pilha_tipos.pop()
                    tipo1 = pilha_tipos.pop()
                    pilha_valores.pop()
                    pilha_valores.pop()
                    regras = regras_semanticas['operadores_aritmeticos'].get(simbolo, None)

                    if simbolo == '^':
                        if tipo1 not in regras['aceita_base']:
                            erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' não aceita base do tipo '{tipo1}'.")
                        if tipo2 not in regras['aceita_exp']:
                            erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' não aceita expoente do tipo '{tipo2}'.")
                    elif simbolo in {'/', '%'}:
                        if tipo1 != 'int' or tipo2 != 'int':
                            erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' requer operandos do tipo 'int'.")
                        tipo_resultado = regras['retorna']
                    
                    elif simbolo == '|':
                        if tipo1 not in regras['aceita'] or tipo2 not in regras['aceita']:
                            erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' requer operandos do tipo 'int' ou 'real'.")
                        tipo_resultado = regras['retorna']
                    else:
                        if tipo1 not in regras['aceita'] or tipo2 not in regras['aceita']:
                            erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' requer operandos do tipo 'int' ou 'real'.")
                        tipo_resultado = promoverTipo(tipo1, tipo2)

                    pilha_tipos.append(tipo_resultado)
                    pilha_valores.append(None)  # valor desconhecido

                    arvore_abstrata.append({
                        'tipo': tipo_resultado,
                        'operador': simbolo,
                        'operandos': [tipo1, tipo2],
                        'linha': numero_linha
                    })

                elif simbolo in {'<', '>', '<=', '>=', '==', '!=', '<>'}:
                    if len(pilha_tipos) < 2:
                        erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' requer dois operandos.")
                        continue

                    tipo2 = pilha_tipos.pop()
                    tipo1 = pilha_tipos.pop()
                    pilha_valores.pop()
                    pilha_valores.pop()
                    regras = regras_semanticas['operadores_relacionais'].get(simbolo, None)

                    if tipo1 not in regras['aceita'] or tipo2 not in regras['aceita']:
                        erros_semanticos.append(f"Linha {numero_linha}: Operador '{simbolo}' requer operandos do tipo 'int' ou 'real'.")

                    tipo_resultado = regras['retorna']
                    pilha_tipos.append(tipo_resultado)
                    pilha_valores.append(None)  # valor desconhecido

                    arvore_abstrata.append({
                        'tipo': tipo_resultado,
                        'operador': simbolo,
                        'operandos': [tipo1, tipo2],
                        'linha': numero_linha
                    })
                
                elif simbolo == 'if':
                    if len(pilha_tipos) < 1:
                        erros_semanticos.append(f"Linha {numero_linha}: Comando IF requer uma condição.")
                        continue

                    tipo_condicao = pilha_tipos.pop()
                    pilha_valores.pop()

                    if tipo_condicao != 'booleano':
                        erros_semanticos.append(f"Linha {numero_linha}: Condição do IF deve ser do tipo 'booleano', mas recebeu '{tipo_condicao}'.")

                    tipo_resultado = promoverTipo(*pilha_tipos) if pilha_tipos else 'desconhecido'
                    pilha_tipos.append(tipo_resultado)
                    pilha_valores.append(None)  # valor desconhecido

                    arvore_abstrata.append({
                        'tipo': tipo_resultado,
                        'comando': 'if',
                        'condicao': tipo_condicao,
                        'linha': numero_linha
                    })
                
                elif simbolo == 'while':
                    if len(pilha_tipos) < 1:
                        erros_semanticos.append(f"Linha {numero_linha}: Comando WHILE requer uma condição.")
                        continue

                    tipo_condicao = pilha_tipos.pop()
                    pilha_valores.pop()

                    if tipo_condicao != 'booleano':
                        erros_semanticos.append(f"Linha {numero_linha}: Condição do WHILE deve ser do tipo 'booleano', mas recebeu '{tipo_condicao}'.")

                    tipo_resultado = promoverTipo(*pilha_tipos) if pilha_tipos else 'desconhecido'
                    pilha_tipos.append(tipo_resultado)
                    pilha_valores.append(None)  # valor desconhecido

                    arvore_abstrata.append({
                        'tipo': tipo_resultado,
                        'comando': 'while',
                        'condicao': tipo_condicao,
                        'linha': numero_linha
                    })
    tipo_final = pilha_tipos.pop() if pilha_tipos else 'desconhecido'
    return tabela_simbolos, erros_semanticos, arvore_abstrata, tipo_final


            

def analisadorSemanticoMemoria(tabela_simbolos, memoria):
    """
    Analisador semântico focado na memória.
    Retorna: memoria_atualizada, erros_semanticos
    """
    erros_semanticos = []
    for nome, info in tabela_simbolos.items():
        if not info['inicializada']:
            erros_semanticos.append(f"Linha {info['linha']}: Identificador '{nome}' declarado mas não inicializado.")
        else:
            memoria = adicionarMemoria(memoria, nome, info['tipo'], True)
    return memoria, erros_semanticos

def analisadorSemanticaControle(arvore_abstrata, numero_linha):
    #valida estruturas de controle (if, while)
    
    erros_semanticos = []
    for nodo in arvore_abstrata:
         if 'comando' in nodo:
              comando = nodo['comando']
              if comando == 'if' or comando == 'while':
                tipo_condicao = nodo['condicao']
                if tipo_condicao != 'booleano':
                     erros_semanticos.append(f"Linha {numero_linha}: Condição do {comando.upper()} deve ser do tipo 'booleano', mas recebeu '{tipo_condicao}'.")
    return erros_semanticos
        
def gerarArvoreAtribuida(arvore_anotada, tipo_final, numero_linha):
    """
    Constrói a árvore sintática abstrata atribuída final
    """
    arvore_atribuida = {
        'tipo_no': 'PROGRAMA',
        'tipo_inferido': tipo_final,
        'linha': numero_linha,
        'filhos': arvore_anotada
    }
    
    return arvore_atribuida

# Geração de Documentação - Gramática de Atributos
def gerarDocGramaticaAtributos(nome_arquivo):
    """Gera arquivo markdown com a gramática de atributos"""
    with open(f"gramatica_atributos_{nome_arquivo}.md", "w", encoding="utf-8") as doc:
        doc.write("# Gramática de Atributos\n\n")
        doc.write("## 1. Tipos de Dados\n\n")
        doc.write("A linguagem suporta três tipos:\n")
        doc.write("- `int`: Números inteiros\n")
        doc.write("- `real` (ou `float`): Números de ponto flutuante\n")
        doc.write("- `booleano`: Resultado de operações relacionais\n\n")
        
        doc.write("## 2. Atributos\n\n")
        doc.write("### Atributos Sintetizados (propagam de baixo para cima):\n")
        doc.write("- `tipo`: O tipo da expressão (int, real, booleano)\n")
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
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁,T₂ ∈ {int, real}\n")
        doc.write("────────────────────────────────────────────────\n")
        doc.write("              Γ ⊢ (e₁ e₂ |) : real\n")
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
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : int    T₁ ∈ {int, real}\n")
        doc.write("───────────────────────────────────────────────\n")
        doc.write("           Γ ⊢ (e₁ e₂ ^) : T₁\n")
        doc.write("```\n\n")
        
        doc.write("### 3.2. Operadores Relacionais\n\n")
        doc.write("```\n")
        doc.write("Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁,T₂ ∈ {int, real}\n")
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
        doc.write("promover_tipo(int, real) = real\n")
        doc.write("promover_tipo(real, int) = real\n")
        doc.write("promover_tipo(real, real) = real\n")
        doc.write("```\n\n")

# Geração de Documentação - Julgamento de Tipos
def gerarDocJulgamentoTipos(arvore_anotada, tipo_final, numero_linha, nome_arquivo):
    """Gera arquivo markdown com o julgamento de tipos"""
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
                    doc.write("(divisão real → real)\n")
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