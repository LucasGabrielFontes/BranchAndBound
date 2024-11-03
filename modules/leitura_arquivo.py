# leitura_arquivo.py

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