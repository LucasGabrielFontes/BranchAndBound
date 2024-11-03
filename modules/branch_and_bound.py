# branch_and_bound.py

from mip import Model, xsum, CONTINUOUS, MAXIMIZE, CBC
import matplotlib.pyplot as plt
from arvore import No, desenha_arvore

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
    for variavel, valor in solucao_relaxada.items():
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
        no_atual.resultado_objetivo = resultado_objetivo  # Armazena o valor da função objetivo no nó atual

        # Se o problema for inviável, poda o nó por inviabilidade
        if resultado_objetivo is None:
            continue

        # Poda por limitante: se o valor objetivo não é melhor que o melhor já encontrado, descarta o nó
        if resultado_objetivo <= melhor_valor_objetivo:
            continue

        # Se a solução é inteira, verifica se é a melhor e também poda o nó por integralidade
        if solucao_inteira(solucao_relaxada):
            if resultado_objetivo > melhor_valor_objetivo:
                melhor_valor_objetivo = resultado_objetivo
                melhor_solucao = solucao_relaxada
            continue
        else: # Caso não tenha sido podado, é necessário bifurcar o nó
            # Escolhe a variável fracionária mais próxima de 0.5
            variavel_fracionaria = escolhe_variavel_fracionaria(solucao_relaxada)

            # Bifurca em x_j = 0
            no_esquerdo = No(variaveis_fixadas=no_atual.variaveis_fixadas.copy())
            no_esquerdo.variaveis_fixadas.update({variavel_fracionaria: 0}) # Adiciona mais uma restrição ao filho de que a variável escolhida deve ser igual a 0
            no_atual.esquerda = no_esquerdo # Define o nó esquerdo
            pilha.append(no_esquerdo)

            # Bifurca em x_j = 1
            no_direito = No(variaveis_fixadas=no_atual.variaveis_fixadas.copy())
            no_direito.variaveis_fixadas.update({variavel_fracionaria: 1})  # Adiciona mais uma restrição ao filho de que a variável escolhida deve ser igual a 1
            no_atual.direita = no_direito # Define o nó direito
            pilha.append(no_direito)

    # Desenha a árvore
    plt.figure(figsize=(24, 14))
    desenha_arvore((raiz, raiz.resultado_objetivo))
    plt.axis('off')
    plt.show()

    return melhor_valor_objetivo, melhor_solucao