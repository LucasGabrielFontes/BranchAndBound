# arvore.py

import matplotlib.pyplot as plt

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

def calcula_posicoes(no, x=0, y=0, pos=None, x_offset=[0]):
    if pos is None:
        pos = {}
    if no.esquerda:
        calcula_posicoes(no.esquerda, x, y - 1, pos, x_offset)
    # Atribui a posição x atual ao nó
    pos[no] = (x_offset[0], y)
    x_offset[0] += 1  # Incrementa o deslocamento x para o próximo nó
    if no.direita:
        calcula_posicoes(no.direita, x, y - 1, pos, x_offset)
    return pos

# Função para desenhar a árvore de ramificações com matplotlib
def desenha_arvore(arvore):
    pos = calcula_posicoes(arvore[0])  # Supondo que arvore[0] é o nó raiz
    for no in pos:
        x, y = pos[no]
        resultado_objetivo = no.resultado_objetivo
        texto_no = f"{resultado_objetivo:.2f}" if resultado_objetivo is not None else "Inviável"
        plt.text(x, y, texto_no, ha='center', va='center',
                 bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
        if no.esquerda:
            x_esq, y_esq = pos[no.esquerda]
            plt.plot([x, x_esq], [y, y_esq], 'k-')
        if no.direita:
            x_dir, y_dir = pos[no.direita]
            plt.plot([x, x_dir], [y, y_dir], 'k-')