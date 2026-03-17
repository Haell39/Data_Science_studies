# Respostas — Exercícios de Lógica de Programação

## Nível Fácil

1) Soma de lista

```python
def soma(lista):
    if not lista:
        return 0
    s = 0
    for x in lista:
        s += x
    return s

# Exemplo: soma([1,2,3]) -> 6
```

2) Máximo e mínimo

```python
def min_max(lista):
    if not lista:
        raise ValueError("lista vazia")
    minimo = maximo = lista[0]
    for x in lista[1:]:
        if x < minimo:
            minimo = x
        if x > maximo:
            maximo = x
    return minimo, maximo

# Exemplo: min_max([3,1,4]) -> (1,4)
```

3) Contar pares

```python
def conta_pares(lista):
    return sum(1 for x in lista if x % 2 == 0)

# Exemplo: conta_pares([1,2,4]) -> 2
```

4) Fibonacci iterativo

```python
def fibonacci(n):
    if n < 0:
        raise ValueError("n negativo")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Exemplo: fibonacci(6) -> 8
```

5) Palíndromo

```python
import re
def eh_palindromo(s):
    s = re.sub(r"[^a-z0-9]", "", s.lower())
    return s == s[::-1]

# Exemplo: eh_palindromo('A man, a plan') -> False; 'arara' -> True
```

## Nível Médio

1) Verificador de primo

```python
import math
def eh_primo(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(math.sqrt(n))
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

# Exemplo: eh_primo(17) -> True
```

2) Insertion sort

```python
def insertion_sort(lista):
    arr = lista[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

# Exemplo: insertion_sort([3,1,2]) -> [1,2,3]
```

3) Frequência de palavras

```python
import re
from collections import Counter
def frequencia_palavras(texto):
    tokens = re.findall(r"\b\w+\b", texto.lower())
    return dict(Counter(tokens))

# Exemplo: frequencia_palavras('Oi oi tudo') -> {'oi':2,'tudo':1}
```

4) Busca binária

```python
def busca_binaria(lista, alvo):
    l, r = 0, len(lista)-1
    while l <= r:
        m = (l + r) // 2
        if lista[m] == alvo:
            return m
        elif lista[m] < alvo:
            l = m + 1
        else:
            r = m - 1
    return -1

# Exemplo: busca_binaria([1,3,5],3) -> 1
```

5) Soma de pares com alvo (O(n))

```python
def encontra_par_com_soma(lista, alvo):
    seen = {}
    for i, v in enumerate(lista):
        comp = alvo - v
        if comp in seen:
            return (seen[comp], i)
        seen[v] = i
    return None

# Exemplo: encontra_par_com_soma([2,7,11,15],9) -> (0,1)
```

## Nível Difícil

1) Merge Sort

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# Exemplo: merge_sort([3,1,2]) -> [1,2,3]
```

2) Subset Sum (backtracking)

```python
def subset_sum(nums, alvo):
    def dfs(i, total):
        if total == alvo:
            return True
        if i >= len(nums) or total > alvo:
            return False
        # escolher
        if dfs(i+1, total+nums[i]):
            return True
        # não escolher
        return dfs(i+1, total)
    return dfs(0, 0)

# Exemplo: subset_sum([3,34,4,12,5,2],9) -> True
```

3) LRU Cache (implementação simples)

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacidade:
            self.cache.popitem(last=False)

# Uso: c = LRUCache(2); c.put(1,1); c.put(2,2); c.get(1) -> 1
```

4) Avaliador de expressões (Shunting-yard simplificado)

```python
def avaliar(expr):
    # Tokeniza números e operadores (suporta espaços)
    import re
    tokens = re.findall(r"\d+|[()+\-*/]", expr)

    prec = {'+':1,'-':1,'*':2,'/':2}
    ops = []
    vals = []

    def apply_op():
        op = ops.pop()
        b = vals.pop(); a = vals.pop()
        if op == '+': vals.append(a+b)
        elif op == '-': vals.append(a-b)
        elif op == '*': vals.append(a*b)
        elif op == '/': vals.append(a/b)

    for t in tokens:
        if t.isdigit():
            vals.append(int(t))
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops and ops[-1] != '(':
                apply_op()
            ops.pop()
        else:
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[t]:
                apply_op()
            ops.append(t)

    while ops:
        apply_op()

    return vals[0]

# Exemplo: avaliar('3 + 4 * 2 / ( 1 - 5 )') -> 1.0
```

5) BFS e distância mínima

```python
from collections import deque

def bfs(grafo, inicio):
    visitados = set([inicio])
    q = deque([inicio])
    ordem = []
    while q:
        u = q.popleft()
        ordem.append(u)
        for v in grafo.get(u, []):
            if v not in visitados:
                visitados.add(v)
                q.append(v)
    return ordem

def distancia_minima(grafo, inicio, alvo):
    q = deque([(inicio,0)])
    visitados = set([inicio])
    while q:
        u, d = q.popleft()
        if u == alvo:
            return d
        for v in grafo.get(u, []):
            if v not in visitados:
                visitados.add(v)
                q.append((v, d+1))
    return None

# Exemplo: grafo={'A':['B'],'B':['C'],'C':[]}; bfs(grafo,'A')->['A','B','C']
```
