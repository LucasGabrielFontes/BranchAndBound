# Branch and Bound para Programação Linear Inteira Binária

Implementação do algoritmo Branch and Bound para resolução de problemas de programação linear inteira binária, utilizando a biblioteca **Python-Mip**. Este projeto foi desenvolvido como parte do projeto final da disciplina de **Pesquisa Operacional**, lecionada pelo professor **Teobaldo Bulhões**.

### Integrantes do Projeto
- Douglas Veras
- Lucas Gabriel
---

## Configuração do Ambiente

### 1. Clonar o Repositório

Clone o repositório para sua máquina local.

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA_DO_REPOSITORIO>
```

### 2. Criar o Ambiente Virtual
É recomendável utilizar um ambiente virtual para instalar as dependências do projeto e evitar conflitos com outras bibliotecas instaladas no sistema. Para criar o ambiente virtual, use o seguinte comando:

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual
Após criar o ambiente, você precisa ativá-lo:

No Windows:
```bash
.venv\Scripts\activate
```
No macOS e Linux:
```bash
source .venv/bin/activate
```

### 4. Instalar as Dependências
Com o ambiente virtual ativo, instale as dependências listadas no arquivo requirements.txt com o seguinte comando:

```bash
pip install -r requirements.txt
```

## Estrutura do Arquivo de Entrada

O algoritmo espera um arquivo .txt contendo as informações do problema de programação linear inteira binária. O formato do arquivo deve seguir a estrutura ilustrada a seguir:

### Exemplo de Problema:

Maximizar:  
5x₁ + 10x₂ + 8x₃

Sujeito a:  
- 3x₁ + 5x₂ + 2x₃ ≤ 6
- 4x₁ + 4x₂ + 4x₃ ≤ 7

Onde:
- x₁, x₂, x₃ ∈ {0, 1}

---

### Formato do Arquivo de Entrada

O arquivo de entrada `.txt` deve seguir a estrutura ilustrada abaixo para o problema de exemplo acima:

```plaintext
3 2         # Número de variáveis e número de restrições
5 10 8      # Coeficientes das variáveis na função objetivo
3 5 2 6     # Coeficientes da primeira restrição, seguido do valor à direita da desigualdade
4 4 4 7     # Coeficientes da segunda restrição, seguido do valor à direita da desigualdade
```

## Executando o programa

Para rodar o algoritmo, você deve executar o arquivo principal main.py na raiz do projeto, passando o caminho do arquivo de entrada como parâmetro para a função main.


### Exemplo de uso
Na raiz do projeto, com o ambiente virtual ativo, rode:

```bash
python main.py
```

### Nota:

O caminho do arquivo .txt que contém as informações do problema pode ser especificado dentro do código no arquivo main.py, ou modificado de acordo com o nome do arquivo e seu local de armazenamento.
