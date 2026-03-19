
**O que é uma lista?**

É uma coleção ordenada de valores guardados numa única variável. Pensa numa fila de itens numerados.

```python
frutas = ["maçã", "banana", "uva", "manga"]
#índice:    0        1        2       3
#índice neg: -4      -3       -2      -1
```

---

**Operações essenciais que você precisa dominar:**

```python
frutas = ["maçã", "banana", "uva"]

# Acessar
frutas[0]        # "maçã"
frutas[-1]       # "uva" (último)

# Adicionar
frutas.append("manga")     # adiciona no final
frutas.insert(1, "kiwi")   # adiciona na posição 1

# Remover
frutas.remove("banana")    # remove pelo valor
frutas.pop()               # remove o último
frutas.pop(0)              # remove pelo índice

# Informações
len(frutas)      # quantidade de itens
"uva" in frutas  # True/False — verifica se existe

# Percorrer
for fruta in frutas:
    print(fruta)

# Percorrer com índice
for i in range(len(frutas)):
    print(i, frutas[i])
```

---

**Slicing — fatiar a lista (muito cobrado!):**

```python
numeros = [10, 20, 30, 40, 50]

numeros[1:3]   # [20, 30] — do índice 1 até 2
numeros[:2]    # [10, 20] — do início até índice 1
numeros[2:]    # [30, 40, 50] — do índice 2 até o fim
numeros[::-1]  # [50, 40, 30, 20, 10] — invertida
```

---

## Exercícios

### Exercício 1 - Acesso (Fácil)
Dada a lista `cores = ["vermelho","azul","verde","amarelo","roxo"]`, imprima o primeiro, o último e o terceiro elemento.

**Dica:** Lembre: índice começa em 0. Índice negativo conta do fim.

### Exercício 2 - Acesso (Fácil)
Dada a lista `numeros = [10, 20, 30, 40, 50]`, use slicing para imprimir: os 3 primeiros, os 2 últimos e a lista invertida.

**Dica:** Sintaxe: `lista[inicio:fim]` — o fim não é incluído.

### Exercício 3 - Loop (Fácil)
Dada a lista `notas = [7, 9, 5, 8, 6]`, calcule e imprima a média.

**Dica:** Some todos os elementos com um acumulador e divida por `len(notas)`.

### Exercício 4 - Modificar (Fácil)
Crie uma lista vazia chamada `pares`. Usando um loop de 1 a 20, adicione apenas os números pares nessa lista e imprima o resultado.

**Dica:** Use o operador `%` para verificar se é par, e `.append()` para adicionar.

### Exercício 5 - Busca (Médio)
Dada a lista `produtos = ["arroz","feijão","macarrão","sal","açúcar"]`, peça ao usuário um produto e informe se ele está ou não na lista.

**Dica:** Use o operador `in` para verificar se o item existe na lista.

### Exercício 6 - Loop (Médio)
Dada a lista `numeros = [3, 7, 2, 9, 4, 6, 1, 8, 5]`, conte quantos números são maiores que 5 e imprima esse total.

**Dica:** Use um contador que começa em 0 e incrementa quando a condição for verdadeira.

### Exercício 7 - Modificar (Médio)
Dada a lista `nomes = ["ana","carlos","beatriz","daniel","elena"]`, remova o primeiro e o último nome e adicione "fernanda" no final. Imprima a lista final.

**Dica:** Use `pop(0)` para remover o primeiro, `pop()` para o último, e `append()` para adicionar.

### Exercício 8 - Busca (Médio)
Dada a lista `valores = [15, 42, 8, 73, 29, 61, 4]`, encontre o menor valor SEM usar a função `min()`.

**Dica:** Mesma lógica do "maior valor" — mas compare com `<` em vez de `>`.

### Exercício 9 - Desafio (Difícil)
Dada a lista `nums = [1, 2, 2, 3, 4, 4, 4, 5]`, crie uma nova lista chamada `sem_duplicatas` que contenha apenas os valores únicos, mantendo a ordem.

**Dica:** Percorra a lista e use `not in` para só adicionar o item se ele ainda não estiver na nova lista.

### Exercício 10 - Desafio (Difícil)
Dadas duas listas `a = [1, 2, 3, 4, 5]` e `b = [3, 4, 5, 6, 7]`, crie uma terceira lista com os elementos que aparecem nas DUAS listas (interseção). Não use sets.

**Dica:** Para cada elemento de "a", verifique se ele também está em "b" usando `in`.
