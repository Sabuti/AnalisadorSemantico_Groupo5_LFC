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
def parseExpressao(linha, _tokens_):
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
                    raise ValueError("Erro: parêntese fechado sem correspondente.")
        elif char in "+-*/%^":  # operadores
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
        raise ValueError("Erro: parênteses desbalanceados.")
    return True

#funções de estado para o analisador léxico
def estadoNumero(token):
    if not token:
        return False
    try:
        if token.count(".") > 1: # Checa se há mais de um ponto decimal
            return False
        float(token)
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
        case "<" | ">" | "<=" | ">=" | "==" | "!=": 
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

    if token in {"RES", "MEM", "IF", "WHILE"}:
        return True
    return True

# -------------------------
# Analisador léxico: valida CADA token isoladamente
def analisadorLexico(tokens):
    tokens_convertidos = []

    for token in tokens:
        if estadoParenteses(token):
            tokens_convertidos.append(token)
            continue
        if estadoOperador(token):
            tokens_convertidos.append(token)
            continue
        if estadoNumero(token):
            tokens_convertidos.append("real")  # converte número para token 'real'
            continue
        if estadoComparador(token):
            tokens_convertidos.append(token)
            continue
        if RESorMEM(token):
            if token == "RES":
                tokens_convertidos.append("res")  # converte comando RES para token 'res'
            elif token == "IF":
                tokens_convertidos.append("if") # converte comando IF para token 'if'
            elif token == "WHILE":
                tokens_convertidos.append("while") # converte comando WHILE para token 'while'
            else:
                tokens_convertidos.append("ident")  # converte outros identificadores para token 'ident'
            continue

        # Se não passou em nada, é inválido
        raise ValueError(f"Erro léxico: token inválido -> {token}")

    return tokens_convertidos

def analisadorSemantico(derivacao, memoria, historico_resultados):
    """
    Executa a análise semântica sobre a derivação gerada pelo analisador sintático.
    Retorna: memoria_atualizada, erros_semanticos, arvore_abstrata
    """
    erros_semanticos = []
    arvore_abstrata = []
    contador_mem = 1

    for nao_terminal, producao in derivacao:
        if not producao:
            continue

        # Atribuição simulada: (real ident)
        if len(producao) >= 2 and producao[0] == 'real' and producao[1] == 'ident':
            nome = producao[1]
            contador_mem += 1
            memoria = adicionarMemoria(memoria, nome, tipo='real', inicializada=True)
            arvore_abstrata.append(('ATRIB', nome, producao[0]))

        # Operação aritmética
        elif any(op in producao for op in ['+', '-', '*', '/', '%', '^']):
            arvore_abstrata.append(('OPERACAO', producao))
            if producao.count('real') + producao.count('ident') < 2:
                erros_semanticos.append("Erro: operador aritmético com operandos insuficientes.")

        # Comparação
        elif any(op in producao for op in ['<', '>', '<=', '>=', '==', '!=']):
            arvore_abstrata.append(('COMPARACAO', producao))
            if producao.count('real') + producao.count('ident') < 2:
                erros_semanticos.append("Erro: operador de comparação sem dois operandos.")

        # Estruturas de controle
        elif 'if' in producao:
            arvore_abstrata.append(('CONDICAO_IF', producao))
            if not any(op in producao for op in ['<', '>', '==', '<=', '>=', '!=']):
                erros_semanticos.append("Erro: IF sem condição de comparação.")

        elif 'while' in producao:
            arvore_abstrata.append(('LOOP_WHILE', producao))
            if not any(op in producao for op in ['<', '>', '==', '<=', '>=', '!=']):
                erros_semanticos.append("Erro: WHILE sem condição de comparação.")

        # Variáveis MEM
        elif 'ident' in producao:
            nome = producao[0]
            contador_mem += 1
            if nome.startswith("MEM"):
                if nome not in memoria:
                    erros_semanticos.append(f"Erro: variável '{nome}' usada sem declaração prévia.")
                    memoria = adicionarMemoria(memoria, nome, tipo='real', inicializada=False)
            arvore_abstrata.append(('IDENT', nome))
        
        elif 'res' in producao:
            if 'RES' not in memoria:
                memoria = adicionarMemoria(memoria, 'RES', tipo='real', inicializada=False)
            arvore_abstrata.append(('IDENT', 'RES'))

    # Atualizar RES
    if historico_resultados:
        memoria = adicionarMemoria(memoria, 'RES', tipo='real', inicializada=True)
        memoria['RES']['valor'] = historico_resultados[-1]

    # Validação geral
    if not memoria:
        erros_semanticos.append("Aviso: nenhuma variável MEM ou RES declarada.")

    return memoria, erros_semanticos, arvore_abstrata


def validarRPN(tokens, memoria, erros):
    erros = []
    pilha = []
    
    # Extrai tokens da derivação para validar RPN
    tokens = []
    for _, producao in derivacao:
        if producao and producao[0] not in ['(', ')']:  # Ignora parênteses
            tokens.extend(producao)
    
    # Simula avaliação RPN
    for token in tokens:
        if token in ['real', 'ident']:
            pilha.append('operando')
        elif token in ['+', '-', '*', '/', '%', '^', '|', '<', '>', '<=', '>=', '==', '!=', 'res']:
            if len(pilha) < 2:
                erros.append(f"Erro RPN: Operador '{token}' sem operandos suficientes")
                return False, erros
            pilha.pop()  # Remove operando 2
            pilha.pop()  # Remove operando 1
            pilha.append('resultado')  # Adiciona resultado
    
    # No final deve sobrar exatamente um resultado
    if len(pilha) != 1:
        erros.append("Erro RPN: Expressão mal formada")
        return False, erros
    
    return True, erros


def inicializarMemoria():
    """Inicializa a memória vazia"""
    return {}


def adicionarMemoria(memoria, nome, tipo='desconhecido', inicializada=False):
    """Adiciona um item à memória"""
    memoria[nome] = {
        'tipo': tipo,
        'inicializada': inicializada,
        'usada': False
    }
    return memoria

def gerarDocumentacaoSemantica(memoria, todos_erros, nome_arquivo):
    """Gera documentação da análise semântica"""
    nome_base = nome_arquivo.split('.')[0]
    with open(f"semantico_{nome_base}.txt", "w", encoding="utf-8") as doc:
        doc.write("=== ANÁLISE SEMÂNTICA ===\n\n")
        doc.write("MEMÓRIA (Tabela de Símbolos):\n")
        doc.write("-" * 50 + "\n")
        if memoria:
            for simbolo, info in memoria.items():
                doc.write(f"{simbolo}: {info}\n")
        else:
            doc.write("Memória vazia\n")
        doc.write("\nERROS SEMÂNTICOS ENCONTRADOS:\n")
        doc.write("-" * 50 + "\n")
        if todos_erros:
            for i, erro in enumerate(todos_erros, 1):
                doc.write(f"{i:2d}. {erro}\n")
        else:
            doc.write("Nenhum erro semântico encontrado.\n")
        doc.write(f"\nRESUMO:\n")
        doc.write(f"- Total de itens na memória: {len(memoria)}\n")
        doc.write(f"- Total de erros: {len(todos_erros)}\n")


# --------------------------

# Analisador sintático: constrói a gramática, tabela LL(1)
def processarResultadoExpressao(derivacao, memoria, historico_resultados):
    """ 
    Processa uma expressão regular e calcula seu resultado 
    Retorna o resultado (simulado) e atualiza o histórico 
    """
    # Simula o cálculo do resultado (implementação simplificada)
    resultado_simulado = 0.0
    # Lógica simplificada para calcular resultado
    for _, producao in derivacao:
        if producao and 'real' in producao:
            resultado_simulado += 1.0  # soma simulada

    
    # Adiciona ao histórico
    historico_resultados.append(resultado_simulado)
    # Atualiza RES com o último resultado
    memoria = adicionarMemoria(memoria, 'RES', 'numero', True)
    memoria['RES']['valor'] = resultado_simulado
    return memoria, historico_resultados, resultado_simulado


def identificarTipoLinha(derivacao):
    """ Identifica se a linha é uma expressão, atribuição ou consulta """
    for nao_terminal, producao in derivacao:
        if nao_terminal == 'ATRIBUICAO_MEM':
            return 'atribuicao_mem'
        elif nao_terminal == 'CONSULTA_RES':
            return 'consulta_res'
        elif nao_terminal == 'EXPR':
            return 'expressao'
    
    return 'desconhecido'


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
    G['NUMERO'] = [['real']]    # token lexical 'real'
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

# --------------------------
# Analisador sintático: processa tokens usando a tabela LL(1)
def parsear(tokens, tabelaLL1): # entrada: vetor de tokens, tabelaLL1
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
                raise ValueError(f"Erro de sintaxe: esperado '{top}', encontrado '{current_token}'")
        else: # topo é um não-terminal
            key = (top, current_token)
            if key in tabelaLL1:
                production = tabelaLL1[key]
                derivation.append((top, production)) # registra a produção usada
                for sym in reversed(production): # empilha a produção na ordem inversa
                    if sym != EPS: # não empilha epsilon
                        stack.append(sym)
            else:
                raise ValueError(f"Erro de sintaxe: não há produção para {top}, '{current_token}'")
    raise ValueError("Erro de sintaxe: pilha vazia antes do fim dos tokens")

# --------------------------
# Programa principal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <nome_do_arquivo>")
    else:
        caminho = sys.argv[1]
        linhas = []
        memoria = {}
        resultados = []
        G, FIRST, FOLLOW, tabelaLL1 = construirGramatica()
        lerArquivo(caminho, linhas)
        with open(caminho, "r", encoding="utf-8") as f:
            for numero_linha, linha in enumerate(f, start=1):
                linha = linha.strip()
                if not linha:
                    continue
                tokens = []
                try:
                    # do trabalho 1
                    parseExpressao(linha, tokens)
                    tokens = analisadorLexico(tokens)
                    # do trabalho 2
                    derivation = parsear(tokens, tabelaLL1)
                    # pro trabalho 3: analisar semanticamente a derivação
                    #analisadorSemantico(derivation)
                    memoria, erros_semanticos, arvore_abstrata = analisadorSemantico(derivation, memoria, resultados)
                    gerarDocumentacaoSemantica(memoria, erros_semanticos, f"{caminho}_linha{numero_linha}")
                    # pra depurar
                    print(f"Linha válida: {linha}")
                    print(f"Tokens: {tokens}")
                    #print(f"Derivações: {derivation}\n")
                except ValueError as e:
                    print(e)