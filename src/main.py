from mip import *

# Classe que representa o formato geral de um nó da árvore do algoritmo Branch and Bound
class No:
    def __init__(self, variaveis_fixadas, resultado_objetivo=None, valores_variaveis=None):
        """
        variaveis_fixadas: Um dicionário que indica quais variáveis foram fixadas e seus valores (0 ou 1)
        resultado_objetivo: Valor da função objetivo na solução relaxada
        valores_variaveis: Valores encontrados para cada uma das variávies na relaxação linear - incluindo variáveis fracionárias
        """
        self.variaveis_fixadas = variaveis_fixadas  # Quais variáveis foram fixadas e seus valores
        self.resultado_objetivo = resultado_objetivo  # Resultado da função objetivo da relaxação
        self.valores_variaveis = valores_variaveis  # Solução fracionária da relaxação linear
        self.esquerda = None  # Filho esquerdo (ramo x_j = 0)
        self.direita = None  # Filho direito (ramo x_j = 1)

# Função para ler o arquivo de entrada
def le_arquivo(path):
    """
    Parâmetro:
    path: string
      Caminho do arquivo

    Retorno:
    n: quantidade de variáveis do problema

    m: quantidade de restrições do problema

    coeficientes_objetivo: coeficientes das variáveis na função objetivo

    restricoes: lista de listas de coeficientes das variáveis em cada uma das restrições do problema

    valores_direita: termos independentes de cada uma das restrições
    """

    try:
        with open(path, 'r') as arquivo:
            # Lê a primeira linha: quantidade de variáveis (n) e quantidade de restrições (m)
            n, m = map(int, arquivo.readline().strip().split())

            """
              .strip(): retira espaços em branco no começo e no fim da linha, incluindo o caractere de nova linha '\n'
              .split(): retorna uma lista de strings, geradas a partir da separação em torno de espaço em branco
              map(): aplica uma determinada função, nesse caso int(), a todos os elementos de uma lista
            """

            # Lê a segunda linha: coeficientes das variáveis na função objetivo
            coeficientes_objetivo = list(map(float, arquivo.readline().strip().split()))

            # Lê as próximas linhas: coeficientes das variáveis em cada uma das restrições e os termos independentes em cada uma das restrições também
            restricoes = []
            valores_direita = []
            for _ in range(m):
                linha = list(map(float, arquivo.readline().strip().split()))
                restricoes.append(linha[:-1])  # coeficientes das variáveis (lista de listas) - retira o último elemento da linha, que é o termo independente
                valores_direita.append(linha[-1])  # valor à direita da desigualdade - só recebe o último elemento da linha

        # Retorna os dados lidos
        return n, m, coeficientes_objetivo, restricoes, valores_direita

    except FileNotFoundError:
        print(f"Erro: Arquivo '{path}' não encontrado.")
        return None, None, None, None, None
    except ValueError:
        print(f"Erro ao processar o arquivo '{path}'. Verifique o formato.")
        return None, None, None, None, None

# Função que resolve uma relaxação linear com a biblioteca Python-Mip
def resolve_relaxacao(n, m, variaveis_fixadas, coeficientes_objetivo, restricoes, valores_direita):
    """
    Resolve a relaxação linear para um problema de programação linear inteira binária

    Parâmetros:
    n: quantidade de variáveis

    m: quantidade de restrições

    variaveis_fixadas: dicionário
        Dicionário com variáveis fixadas e seus valores (0 ou 1).

    coeficientes_objetivo: lista
        Coeficientes da função objetivo.

    restricoes: lista de listas
        Matriz de coeficientes das restrições.

    valores_direita: lista
        Lista dos limites das restrições.

    Retorno:
    resultado_objetivo: float ou None
        Valor da função objetivo, ou None se o problema for inviável.

    solucao: dicionário ou None
        Dicionário com os valores das variáveis na solução relaxada, ou None se o problema for inviável.
    """

    model = Model(sense=MAXIMIZE, solver_name=CBC)  # Criação do modelo de maximização utilizando o solver padrão CBC

    # Criação das variáveis contínuas com limites entre 0 e 1: não há restrição de integralidade. Logo, é uma relaxação linear do problema
    x = [model.add_var(var_type=CONTINUOUS, lb=0, ub=1, name=f'x_{i}') for i in range(n)]

    # Definição da função objetivo
    model.objective = xsum(coeficientes_objetivo[i]*x[i] for i in range(n))

    # Adiciona as restrições
    for i in range(m):
        model += xsum(restricoes[i][j]*x[j] for j in range(n)) <= valores_direita[i]

    # Aplica as retrições de variáveis fixadas, caso existam
    for var, valor in variaveis_fixadas.items():
        model += x[var] == valor

    # Resolve a relaxação linear
    model.optimize()

    # Retorna o valor da função objetivo objetivo encontrado e a os valores das variáveis em 'solucao', ou None se o problema for inviável
    if model.num_solutions:
        solucao = {i: x[i].x for i in range(n)}
        resultado_objetivo = model.objective_value
        return resultado_objetivo, solucao
    else:
        return None, None

# Função que escolhe a variável fracionária que será utilizada para a bifurcação na árvore do algoritmo Branch and Bound
def escolhe_variavel_fracionaria(solucao_relaxada):
    """
    Escolhe a variável fracionária que será escolhida para a bifurcação de um nó na árvore do Branch and Bound: a que for mais próxima de 0,5

    Parâmetros:
    solucao_relaxada: dicionário
        Dicionário com os valores da solução relaxada.

    Retorno:
    var: int ou None
        Índice da variável fracionária escolhida para a bifurcação ou None se todas as variáveis forem inteiras.
    """
    variavel_fracionaria = None
    menor_diferenca = 1  # Definição de uma diferença inicial grande, que não afetará o resultado

    # Procura a variável fracionária mais próxima de 0,5
    for variavel, valor in solucao_relaxada.items():
        if 0 < valor < 1: # Se a variavel não for binária, é uma cadidata a ser escolhida
            diferenca = abs(valor - 0.5)
            if diferenca < menor_diferenca: # Quanto menor a diferença, em módulo, entre o valor da variável e 0,5, mais próxima ela está de 0,5
                menor_diferenca = diferenca
                variavel_fracionaria = variavel
    return variavel_fracionaria # A variável mais próxima de 0,5 é retornada

# Função que verifica se uma solução é inteira ou não
# Solução inteira: os valores de todas as variáveis na solução são inteiros
# Solução não-inteira: pelo menos alguma variável possui valor fracionário
def solucao_inteira(solucao_relaxada):
    """
    Verifica se a solução é inteira (nesse caso, se todas as variáveis binárias).

    Parâmetros:
    solucao_relaxada: dicionário
        Dicionário com os valores das variáveis encontradas na resolução da relaxação linear.

    Retorno:
    bool: True se a solução for inteira, False caso contrário.
    """
    for varriavel, valor in solucao_relaxada.items():
        if valor != 0 and valor != 1: # Se alguma das variáveis for diferente de 0 e 1, já torna a solução não-inteira. Retorna False
            return False

    return True # Após passar pelo for, significa que todas as variáveis são iguais a 0 ou 1. Ou seja, solução é inteira. Retorna True

# Função que, de fato, implementa o algoritmo Branch and Bound
def branch_and_bound(n, m, coeficientes_objetivo, restricoes, valores_direita):
    """
    Implementa o algoritmo Branch and Bound com busca em profundidade.

    Parâmetros:
    n: quantidade de variáveis

    m: quantidade de restrições

    coeficientes_objetivo: list
        Coeficientes da função objetivo.

    restricoes: list de lists
        Matriz de coeficientes das restrições.

    valores_direita: list
        Lista dos limites das restrições.

    Retorno:
    melhor_resultado_objetivo  float
        O melhor valor encontrado para a função objetivo.

    melhor_solucao: dict
        A melhor solução inteira encontrada: valores para cada uma das variáveis.
    """

    # Pilha de nós abertos (usada na busca em profundidade)
    pilha = []

    # Cria o nó raiz com variáveis não fixadas ainda
    raiz = No(variaveis_fixadas={})
    pilha.append(raiz)

    melhor_solucao = None
    melhor_valor_objetivo = float('-inf') # Como a função objetivo é de maximização sempre, inicia-se o melhor valor com -infinito, apenas para futuras comparações, sem prejudicar a lógica

    # Processa cada nó da pilha, enquanto existir
    while pilha:
        no_atual = pilha.pop()  # Remove o último nó da pilha

        # Resolve a relaxação linear para o nó atual
        resultado_objetivo, solucao_relaxada = resolve_relaxacao(n, m, no_atual.variaveis_fixadas, coeficientes_objetivo, restricoes, valores_direita)

        # Se o problema for inviável, poda o nó por inviabilidade
        if resultado_objetivo is None:
            continue

        # Se a solução é inteira, verifica se é a melhor e também poda o nó por integralidade
        if solucao_inteira(solucao_relaxada):
            if resultado_objetivo > melhor_valor_objetivo:
                melhor_valor_objetivo = resultado_objetivo
                melhor_solucao = solucao_relaxada
                continue # O continue é indiferente aqui, mas é usado apenas para explicitar que o nó foi podado
        else: # Caso não tenha sido podado, é necessário bifurcar o nó
            # Escolhe a variável fracionária mais próxima de 0.5
            variavel_fracionaria = escolhe_variavel_fracionaria(solucao_relaxada)

            # Bifurca em x_j = 0
            no_esquerdo = No(variaveis_fixadas=no_atual.variaveis_fixadas.copy())
            no_esquerdo.variaveis_fixadas.update({variavel_fracionaria: 0}) # Adiciona mais uma restrição ao filho de que a variável escolhida deve ser igual a 0
            pilha.append(no_esquerdo)

            # Bifurca em x_j = 1
            no_direito = No(variaveis_fixadas=no_atual.variaveis_fixadas.copy())
            no_direito.variaveis_fixadas.update({variavel_fracionaria: 1})  # Adiciona mais uma restrição ao filho de que a variável escolhida deve ser igual a 1
            pilha.append(no_direito)

    return melhor_valor_objetivo, melhor_solucao

# Função main que lê o arquivo de entrada e chama a função do algoritmo Branch and Bound
def main():
    # Le os dados do arquivo
    n, m, coeficientes_objetivo, restricoes, valores_direita = le_arquivo('./ArquivosTeste/teste1.txt')

    # Recebe a melhor solução inteira dada pelo método Branch and Bound, caso exista
    melhor_valor_objetivo, melhor_solucao = branch_and_bound(n, m, coeficientes_objetivo, restricoes, valores_direita)

    if melhor_solucao == None:
        print("O problema é inviável")
    else:
        print("Valor da função objetivo na solução ótima: ", melhor_valor_objetivo)

if __name__ == "__main__":
    main()