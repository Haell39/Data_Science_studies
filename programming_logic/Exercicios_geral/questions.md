# Exercícios de Python para Varejo

## 🟢 Nível Fácil: Variáveis e Condicionais Simples

**Foco:** Entender como manipular dados básicos de sell-out e estoque.

1. **Soma de Vendas:** Peça dois valores de vendas e imprima a soma total.
2. **Conversor de Lead Time:** Peça o tempo de entrega em dias e converta para horas.
3. **Média de Notas:** Receba 3 notas de um treinamento e calcule a média.
4. **Alerta de Estoque:** Peça a quantidade de um produto; se for menor que 10, imprima "Repor Estoque".
5. **Custo de Frete:** Se o estado for "PE", o frete é R$ 20,00; senão, é R$ 10,00.
6. **Par ou Ímpar:** Receba um número de ID e diga se ele é par ou ímpar.
7. **Maior de Idade:** Verifique se um colaborador tem 18 anos ou mais para contratação.
8. **Calculadora de Bônus:** Se a venda for acima de R$ 1.000, dê 10% de desconto.
9. **Positivo ou Negativo:** Verifique se o saldo de estoque inserido é positivo, negativo ou zero.
10. **Comparador de Preços:** Peça o preço de dois produtos concorrentes e diga qual é o mais barato.

---

## 🟡 Nível Médio: Laços (Loops) e Listas

**Foco:** Processar múltiplos registros de promotores e visitas ao PDV.

1. **Contagem de Lojas:** Use um laço para imprimir os números de 1 a 10 (IDs das lojas).
2. **Soma de Lista:** Crie uma lista com 5 valores de vendas e calcule a soma total.
3. **Filtro de Ruptura:** Dada uma lista de estoques `[5, 0, 12, 0, 8]`, conte quantos estão em zero.
4. **Tabuada de Vendas:** Peça um número e mostre a tabuada dele (útil para projeção de metas).
5. **Busca em Lista:** Verifique se o produto "Shampoo" está presente em uma lista de mercadorias.
6. **Maior Venda:** Em uma lista de valores, encontre e imprima o maior valor vendido no dia.
7. **Média de Visitas:** Receba o tempo de 5 visitas de um promotor e calcule a média de tempo no PDV.
8. **Inversor de Nome:** Peça o nome de um cliente e imprima-o de trás para frente.
9. **Filtro de Estado:** Dada uma lista de estados, imprima apenas os que forem "PE" ou "SP".
10. **Validador de Nota:** Peça uma nota de NPS (1 a 5); enquanto o usuário digitar fora desse intervalo, peça novamente.

---
# 🔴 Nível "Real-World": Dados Iniciais para os Exercícios

## Exercício 1: Relatório de Desempenho

**Descrição Original:**
> Dada uma lista de vendas, crie uma nova lista apenas com valores acima de R$ 500,00.

**Dados iniciais fornecidos:**
```python
vendas = [250, 600, 1200, 300, 750, 450, 900, 150, 550, 1100]
```

**Tarefa:** Crie uma nova lista apenas com valores acima de R$ 500,00

---

## Exercício 2: Classificação de Ruptura

**Descrição Original:**
> Se o atraso for > 0, classifique como "Ruptura"; se for <= 0, "No Prazo".

**Dados iniciais fornecidos:**
```python
atrasos = [2, -1, 5, 0, -3, 1, 0, 4, -2, 3]
```

**Tarefa:** Classifique cada atraso:
- Se atraso > 0 → "Ruptura"
- Se atraso <= 0 → "No Prazo"

---

## Exercício 3: Bonificação Escalonada

**Descrição Original:**
> Venda > 1000 (10% bônus), entre 500 e 1000 (5%), abaixo (0%).

**Dados iniciais fornecidos:**
```python
vendas_promotores = [1500, 750, 450, 1100, 600, 950, 200, 1300, 500, 800]
```

**Tarefa:** Calcule o bônus para cada venda:
- Venda > 1000 = 10% de bônus
- Venda entre 500 e 1000 = 5% de bônus
- Venda <= 500 = 0% de bônus

---

## Exercício 4: Frequência de Produtos

**Descrição Original:**
> Conte quantas vezes o produto "Pipoca" aparece em uma lista de pedidos.

**Dados iniciais fornecidos:**
```python
pedidos = ["Pipoca", "Refrigerante", "Pipoca", "Chocolate", "Pipoca", "Chiclete", "Pipoca", "Refrigerante", "Pipoca", "Chiclete"]
```

**Tarefa:** Conte quantas vezes o produto "Pipoca" aparece na lista

---

## Exercício 5: Dicionário de Preços

**Descrição Original:**
> Crie um dicionário com `produto: preço` e peça para o usuário consultar um valor.

**Dados iniciais fornecidos:**
```python
precos_produtos = {
    "Pipoca": 5.50,
    "Refrigerante": 3.50,
    "Chocolate": 4.00,
    "Chiclete": 1.50,
    "Água": 2.00,
    "Suco": 4.50
}
```

**Tarefa:** 
- Peça ao usuário um nome de produto
- Retorne o preço se existir
- Retorne mensagem de erro se não existir

---

## Exercício 6: Limpeza de Dados

**Descrição Original:**
> Dada uma lista com nomes e valores nulos (None), remova os nulos e imprima a lista limpa.

**Dados iniciais fornecidos:**
```python
nomes_e_valores = ["João", 150, "Maria", None, "Pedro", 250, None, "Ana", 300, None, "Carlos"]
```

**Tarefa:** Remova os valores `None` (nulos) e imprima a lista limpa

---

## Exercício 7: Ranking de Promotores

**Descrição Original:**
> Receba nomes e total vendido; identifique quem vendeu mais para ganhar o prêmio do mês.

**Dados iniciais fornecidos:**
```python
promotores = {
    "João": 2500,
    "Maria": 3100,
    "Pedro": 1800,
    "Ana": 2900,
    "Carlos": 2200
}
```

**Tarefa:** Identifique qual promotor vendeu mais (para ganhar o prêmio do mês)

---

## Exercício 8: Análise de NPS

**Descrição Original:**
> Calcule a porcentagem de notas 5 (Promotores) em uma lista de avaliações de clientes.

**Dados iniciais fornecidos:**
```python
notas_nps = [5, 4, 5, 3, 5, 5, 4, 2, 5, 5, 5, 3, 5, 5, 4, 5, 2, 5, 5, 5]
```

**Tarefa:** Calcule qual é a porcentagem de notas 5 (Promotores) em relação ao total

---

## Exercício 9: Simulação de Giro

**Descrição Original:**
> Comece com um estoque de 50; peça vendas sucessivas até que o estoque chegue a zero.

**Dados iniciais fornecidos:**
```python
estoque_inicial = 50
```

**Tarefa:**
- Comece com `estoque = 50`
- Peça vendas sucessivas ao usuário (quanto ele quer vender)
- Atualize o estoque a cada venda
- Pare quando estoque chegar a zero ou ficar negativo
- Mostre o estoque após cada venda

---

## Exercício 10: KPI de Execução

**Descrição Original:**
> Crie uma função que receba `Preço Estimado` e `Preço Real`; se a diferença for > 10%, retorne "Alerta de Gôndola".

**Tarefa:** Crie uma função `kpi_execucao(preco_estimado, preco_real)` que:
- Calcula a diferença percentual: `|preco_estimado - preco_real| / preco_estimado * 100`
- Retorna "Alerta de Gôndola" se diferença > 10%
- Retorna "OK" caso contrário

**Exemplos de uso:**
```python
print(kpi_execucao(100, 95))    # Diferença = 5% → "OK"
print(kpi_execucao(100, 88))    # Diferença = 12% → "Alerta de Gôndola"
print(kpi_execucao(50, 40))     # Diferença = 20% → "Alerta de Gôndola"
print(kpi_execucao(200, 195))   # Diferença = 2.5% → "OK"
```

---

## 💡 Dicas Gerais

- **Exercícios 1-4**: Use list comprehension ou loops simples
- **Exercício 5**: Use `.get()` ou verificação com `in`
- **Exercício 6**: Use list comprehension com condição `is not None`
- **Exercício 7**: Use `max()` com função customizada ou `max(dict.items())`
- **Exercício 8**: Conte quantos 5 existem e divida pelo total
- **Exercício 9**: Use `while` loop e entrada do usuário com `input()`
- **Exercício 10**: Use `abs()` para valor absoluto

**Boa sorte! 🚀**