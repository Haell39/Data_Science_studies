# 📚 Guia Completo: Dicionários em Python

## O que é um Dicionário?

Um dicionário é uma estrutura que armazena pares **chave: valor**. Pense como um dicionário de verdade - você procura uma palavra (chave) e encontra o significado (valor).

```python
# Exemplo básico
meu_dict = {
    "nome": "João",
    "idade": 25,
    "cidade": "Recife"
}
```

---

## 1. CRIANDO DICIONÁRIOS

### Forma 1: Com chaves e valores já definidos
```python
pessoa = {
    "nome": "Maria",
    "profissao": "Engenheira",
    "salario": 5000
}
```

### Forma 2: Dicionário vazio
```python
vazio = {}

# Depois preencher
vazio["chave"] = "valor"
```

### Forma 3: Usando dict()
```python
outro_dict = dict(nome="Pedro", idade=30)
```

---

## 2. ACESSANDO VALORES

### Usando a chave diretamente
```python
meu_dict = {"produto": "Pipoca", "preco": 5.50}

print(meu_dict["produto"])  # "Pipoca"
print(meu_dict["preco"])    # 5.50
```

### ⚠️ CUIDADO: KeyError
Se você tentar acessar uma chave que não existe, dá erro:
```python
print(meu_dict["quantidade"])  # ❌ KeyError: 'quantidade'
```

### Solução 1: Usar .get() (RECOMENDADO)
```python
print(meu_dict.get("quantidade"))  # None (sem erro!)
print(meu_dict.get("quantidade", 0))  # 0 (valor padrão)
print(meu_dict.get("produto"))  # "Pipoca"
```

### Solução 2: Verificar com 'in'
```python
if "quantidade" in meu_dict:
    print(meu_dict["quantidade"])
else:
    print("Chave não existe")
```

---

## 3. ADICIONANDO E MODIFICANDO

### Adicionar um novo par
```python
meu_dict = {"nome": "João"}
meu_dict["idade"] = 25  # Adiciona a chave "idade"
print(meu_dict)  # {'nome': 'João', 'idade': 25}
```

### Modificar um valor existente
```python
meu_dict["nome"] = "Pedro"  # Muda o valor de "nome"
print(meu_dict)  # {'nome': 'Pedro', 'idade': 25}
```

### Adicionar múltiplos pares com .update()
```python
meu_dict.update({
    "cidade": "Recife",
    "profissao": "Dev"
})
```

---

## 4. REMOVENDO PARES

### Remover uma chave específica
```python
meu_dict = {"nome": "João", "idade": 25}
del meu_dict["idade"]  # Remove a chave "idade"
print(meu_dict)  # {'nome': 'João'}
```

### Remover e obter o valor
```python
valor = meu_dict.pop("nome", "não encontrado")
print(valor)  # "João"
print(meu_dict)  # {} (vazio)
```

### Limpar tudo
```python
meu_dict.clear()
print(meu_dict)  # {}
```

---

## 5. NAVEGANDO PELO DICIONÁRIO

### Todas as chaves
```python
precos = {"Pipoca": 5.50, "Refrigerante": 3.50, "Chocolate": 4.00}
print(precos.keys())  # dict_keys(['Pipoca', 'Refrigerante', 'Chocolate'])

for chave in precos.keys():
    print(chave)  # Pipoca, Refrigerante, Chocolate
```

### Todos os valores
```python
print(precos.values())  # dict_values([5.50, 3.50, 4.00])

for valor in precos.values():
    print(valor)  # 5.50, 3.50, 4.00
```

### Pares chave-valor
```python
print(precos.items())  # dict_items([('Pipoca', 5.50), ('Refrigerante', 3.50), ...])

for chave, valor in precos.items():
    print(f"{chave}: R$ {valor}")
    # Pipoca: R$ 5.50
    # Refrigerante: R$ 3.50
    # Chocolate: R$ 4.00
```

---

## 6. VERIFICAÇÕES

### Verificar se chave existe
```python
precos = {"Pipoca": 5.50, "Refrigerante": 3.50}

if "Pipoca" in precos:
    print("Encontrado!")  # Isso vai rodar

if "Chiclete" in precos:
    print("Não vai rodar")
else:
    print("Chiclete não está no dicionário")
```

### Verificar tamanho
```python
print(len(precos))  # 2
```

### Verificar se vazio
```python
if precos:
    print("Tem conteúdo")
else:
    print("Está vazio")
```

---

## 7. EXEMPLOS PRÁTICOS

### Exemplo 1: Consultar valor
```python
precos = {"Pipoca": 5.50, "Refrigerante": 3.50}

produto = "Pipoca"
if produto in precos:
    print(f"Preço: R$ {precos[produto]}")
else:
    print(f"Produto '{produto}' não encontrado")
```

### Exemplo 2: Consultar com entrada do usuário
```python
precos = {"Pipoca": 5.50, "Refrigerante": 3.50, "Chocolate": 4.00}

produto_buscado = input("Qual produto? ")
preco = precos.get(produto_buscado)

if preco:
    print(f"Preço: R$ {preco}")
else:
    print("Produto não encontrado")
```

### Exemplo 3: Listar tudo
```python
precos = {"Pipoca": 5.50, "Refrigerante": 3.50, "Chocolate": 4.00}

print("=== TABELA DE PREÇOS ===")
for produto, preco in precos.items():
    print(f"{produto}: R$ {preco:.2f}")
```

### Exemplo 4: Encontrar mais caro/barato
```python
precos = {"Pipoca": 5.50, "Refrigerante": 3.50, "Chocolate": 4.00}

mais_caro = max(precos.values())
mais_barato = min(precos.values())

print(f"Mais caro: R$ {mais_caro}")
print(f"Mais barato: R$ {mais_barato}")
```

### Exemplo 5: Contar algo (vendas por promotor)
```python
vendas = {
    "João": 2500,
    "Maria": 3100,
    "Pedro": 1800
}

# Encontrar quem vendeu mais
melhor = max(vendas, key=vendas.get)
print(f"Maior vendedor: {melhor}")
```

---

## 8. COMPARAÇÃO: LISTA vs DICIONÁRIO

### Lista (quando você quer ordem/index)
```python
nomes = ["João", "Maria", "Pedro"]
print(nomes[0])  # "João" (acessa pelo índice)
```

### Dicionário (quando você quer associação)
```python
vendas = {
    "João": 2500,
    "Maria": 3100,
    "Pedro": 1800
}
print(vendas["João"])  # 2500 (acessa pelo nome, não pelo índice)
```

---

## 9. ERROS COMUNS

### ❌ Erro 1: Confundir [ ] com get()
```python
# Isso dá erro se a chave não existe
valor = dict["chave"]  # KeyError!

# Isso é seguro
valor = dict.get("chave", "padrão")  # None ou "padrão"
```

### ❌ Erro 2: Esquecer de verificar
```python
precos = {"Pipoca": 5.50}

# ERRADO - vai quebrar
print(precos["Refrigerante"])  # KeyError!

# CORRETO
print(precos.get("Refrigerante", "Não encontrado"))
```

### ❌ Erro 3: Modificar enquanto itera
```python
# NÃO FAÇA ISSO:
for chave in precos:
    del precos[chave]  # Pode causar problemas

# FAÇA ISSO:
chaves_para_deletar = [k for k in precos if <condição>]
for chave in chaves_para_deletar:
    del precos[chave]
```

---

## 🎯 RESUMO RÁPIDO

| Operação | Código |
|----------|--------|
| Criar | `d = {"chave": "valor"}` |
| Acessar (seguro) | `d.get("chave", "padrão")` |
| Acessar (direto) | `d["chave"]` |
| Adicionar | `d["nova_chave"] = "valor"` |
| Deletar | `del d["chave"]` |
| Verificar se existe | `"chave" in d` |
| Todas as chaves | `d.keys()` |
| Todos os valores | `d.values()` |
| Pares | `d.items()` |
| Tamanho | `len(d)` |
| Limpar | `d.clear()` |

---

## 💡 Dica Final

**Sempre use `.get()` quando não tiver certeza se a chave existe!**

```python
# Seguro
valor = precos.get("Pipoca", 0)

# Arriscado
valor = precos["Pipoca"]  # Quebra se não existir
```

Agora vai lá e faz o exercício 5! 🚀