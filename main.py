from modules.branch_and_bound import branch_and_bound
from modules.leitura_arquivo import le_arquivo

# Função main que lê o arquivo de entrada e chama a função do algoritmo Branch and Bound

def main(caminho):
  # Le os dados do arquivo
  n, m, coeficientes_objetivo, restricoes, valores_direita = le_arquivo(caminho)

  # Recebe a melhor solução inteira dada pelo método Branch and Bound, caso exista
  melhor_valor_objetivo, melhor_solucao = branch_and_bound(n, m, coeficientes_objetivo, restricoes, valores_direita)

  if melhor_solucao == None:
    print("O problema é inviável")
  else:
    print("Valor da função objetivo na solução ótima: ", melhor_valor_objetivo)
    print("Valores das variáveis na solução ótima: ")
    for valor in range(len(melhor_solucao)):
      print(f"x{valor+1} = {int(melhor_solucao[valor])}")

if __name__ == "__main__":
  caminho = "ArquivosTeste/teste1.txt"
  main(caminho)