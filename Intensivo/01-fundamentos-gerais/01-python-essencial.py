"""
PYTHON ESSENCIAL - FUNDAMENTOS GERAIS
Os 20% mais importantes para 80% do uso em Data Science
"""

print("=" * 60)
print("PYTHON ESSENCIAL - FUNDAMENTOS")
print("=" * 60)

# 1. VARIÁVEIS E TIPOS ESSENCIAIS
print("\n1. VARIÁVEIS E TIPOS")
print("-" * 30)

# Números
idade = 25
salario = 5000.50
print(f"Idade: {idade} (tipo: {type(idade).__name__})")
print(f"Salário: {salario} (tipo: {type(salario).__name__})")

# Strings
nome = "João Silva"
profissao = 'Data Scientist'
print(f"Nome: {nome}")
print(f"Profissão: {profissao}")

# Booleanos
ativo = True
formado = False
print(f"Ativo: {ativo}")
print(f"Formado: {formado}")

# 2. ESTRUTURAS DE DADOS ESSENCIAIS
print("\n2. ESTRUTURAS DE DADOS")
print("-" * 30)

# Listas - mais usada em DS
notas = [8.5, 7.0, 9.2, 6.8, 8.0]
print(f"Notas: {notas}")
print(f"Média: {sum(notas)/len(notas):.2f}")
print(f"Maior nota: {max(notas)}")
print(f"Menor nota: {min(notas)}")

# Adicionar e remover
notas.append(7.5)
print(f"Após adicionar 7.5: {notas}")
notas.remove(6.8)
print(f"Após remover 6.8: {notas}")

# Dicionários - essencial para dados estruturados
aluno = {
    "nome": "Maria Santos",
    "idade": 23,
    "curso": "Data Science",
    "notas": [9.0, 8.5, 8.7],
    "cidade": "São Paulo"
}
print(f"\nDicionário aluno: {aluno}")
print(f"Nome: {aluno['nome']}")
print(f"Curso: {aluno['curso']}")

# Acessar com get (mais seguro)
print(f"Idade: {aluno.get('idade', 'Não informada')}")
print(f"País: {aluno.get('pais', 'Brasil')}")

# 3. OPERAÇÕES E OPERADORES
print("\n3. OPERAÇÕES BÁSICAS")
print("-" * 30)

a, b = 10, 3
print(f"a = {a}, b = {b}")
print(f"Soma: {a + b}")
print(f"Multiplicação: {a * b}")
print(f"Divisão: {a / b:.2f}")
print(f"Exponenciação: {a ** b}")

# Operações com listas
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
print(f"Lista1: {lista1}")
print(f"Lista2: {lista2}")
print(f"Concatenada: {lista1 + lista2}")

# 4. ESTRUTURAS DE CONTROLE ESSENCIAIS
print("\n4. ESTRUTURAS DE CONTROLE")
print("-" * 30)

# If-elif-else
nota = 7.5
if nota >= 9:
    status = "Excelente"
elif nota >= 7:
    status = "Bom"
elif nota >= 5:
    status = "Regular"
else:
    status = "Insuficiente"
print(f"Nota: {nota} -> Status: {status}")

# For loop - essencial para processar dados
print("\nProcessando lista de números:")
numeros = [10, 20, 30, 40, 50]
soma = 0
for num in numeros:
    soma += num
    print(f"  Número: {num}, Soma parcial: {soma}")
print(f"Soma total: {soma}")

# List comprehension - muito usado em DS
quadrados = [x ** 2 for x in range(1, 11)]
print(f"\nQuadrados de 1 a 10: {quadrados}")

pares = [x for x in range(1, 21) if x % 2 == 0]
print(f"Números pares de 1 a 20: {pares}")

# While loop
print("\nContagem regressiva:")
contador = 5
while contador > 0:
    print(f"  {contador}")
    contador -= 1
print("Fogo!")

# 5. FUNÇÕES ESSENCIAIS
print("\n5. FUNÇÕES ESSENCIAIS")
print("-" * 30)

# Função básica
def calcular_media(numeros):
    """Calcula a média de uma lista de números."""
    if not numeros:
        return 0
    return sum(numeros) / len(numeros)

# Função com parâmetros padrão
def saudacao(nome, cargo="Analista"):
    """Retorna uma saudação personalizada."""
    return f"Olá, {nome}! Você é {cargo}."

# Função lambda - muito usado em DS
dobro = lambda x: x * 2
eh_par = lambda x: x % 2 == 0

# Testando funções
notas_teste = [8.0, 7.5, 9.0, 8.5]
media = calcular_media(notas_teste)
print(f"Média das notas {notas_teste}: {media:.2f}")

print(saudacao("Carlos", "Data Scientist"))
print(saudacao("Ana"))  # usa o padrão "Analista"

print(f"Dobro de 5: {dobro(5)}")
print(f"O número 8 é par? {eh_par(8)}")
print(f"O número 7 é par? {eh_par(7)}")

# 6. MANIPULAÇÃO DE STRINGS ESSENCIAL
print("\n6. MANIPULAÇÃO DE STRINGS")
print("-" * 30)

texto = "   Python para Data Science   "
print(f"Original: '{texto}'")
print(f"Trim: '{texto.strip()}'")
print(f"Upper: '{texto.upper()}'")
print(f"Lower: '{texto.lower()}'")
print(f"Replace: '{texto.strip().replace('Python', 'R')}'")

# Split e Join
frase = "Python é poderoso para Data Science"
palavras = frase.split()
print(f"Frase: '{frase}'")
print(f"Palavras: {palavras}")
print(f"Join com '-': {'-'.join(palavras)}")

# Formatação (f-string)
nome = "Pedro"
idade = 30
salario = 7500.50
mensagem = f"{nome} tem {idade} anos e ganha R${salario:.2f}"
print(f"Mensagem formatada: {mensagem}")

# 7. TRATAMENTO DE ERROS BÁSICO
print("\n7. TRATAMENTO DE ERROS")
print("-" * 30)

def divisao_segura(a, b):
    """Divisão com tratamento de erros."""
    try:
        resultado = a / b
        return f"Resultado: {resultado}"
    except ZeroDivisionError:
        return "Erro: Divisão por zero!"
    except TypeError:
        return "Erro: Tipos inválidos!"
    except Exception as e:
        return f"Erro inesperado: {e}"

print(divisao_segura(10, 2))
print(divisao_segura(10, 0))
print(divisao_segura("10", 2))

# 8. ESTRUTURAS DE DADOS ANINHADAS
print("\n8. DADOS ANINHADOS")
print("-" * 30)

# Lista de dicionários - muito comum em DS
alunos = [
    {"nome": "João", "idade": 20, "notas": [8.0, 7.5, 9.0]},
    {"nome": "Maria", "idade": 22, "notas": [9.5, 8.5, 9.0]},
    {"nome": "Pedro", "idade": 19, "notas": [7.0, 8.0, 7.5]}
]

print("Alunos:")
for aluno in alunos:
    media = sum(aluno["notas"]) / len(aluno["notas"])
    print(f"  {aluno['nome']} ({aluno['idade']} anos): Média {media:.2f}")

# 9. IMPORTAÇÃO DE MÓDULOS ESSENCIAIS
print("\n9. MÓDULOS ESSENCIAIS")
print("-" * 30)

import math
import random
from datetime import datetime

# Math
print(f"Raiz de 16: {math.sqrt(16)}")
print(f"Pi: {math.pi:.4f}")

# Random
print(f"Número aleatório 1-100: {random.randint(1, 100)}")
print(f"Sorteio: {random.choice(['Python', 'R', 'Julia'])}")

# Datetime
agora = datetime.now()
print(f"Data/hora: {agora.strftime('%d/%m/%Y %H:%M:%S')}")

# 10. DESAFIO INTEGRADOR
print("\n10. DESAFIO INTEGRADOR")
print("-" * 30)

def analisar_vendas():
    """Função completa que simula análise de vendas."""
    
    # Dados simulados
    vendas = [
        {"produto": "Laptop", "quantidade": 5, "valor_unitario": 5000},
        {"produto": "Mouse", "quantidade": 15, "valor_unitario": 150},
        {"produto": "Teclado", "quantidade": 10, "valor_unitario": 200},
        {"produto": "Monitor", "quantidade": 8, "valor_unitario": 1200}
    ]
    
    # Cálculos
    total_vendas = 0
    produtos_vendidos = 0
    
    print("Relatório de Vendas:")
    print("-" * 40)
    
    for venda in vendas:
        total_item = venda["quantidade"] * venda["valor_unitario"]
        total_vendas += total_item
        produtos_vendidos += venda["quantidade"]
        
        print(f"{venda['produto']}: {venda['quantidade']} x R${venda['valor_unitario']:.2f} = R${total_item:.2f}")
    
    # Estatísticas
    media_venda = total_vendas / len(vendas)
    ticket_medio = total_vendas / produtos_vendidos
    
    print("-" * 40)
    print(f"Total de vendas: R${total_vendas:.2f}")
    print(f"Média por produto: R${media_venda:.2f}")
    print(f"Ticket médio: R${ticket_medio:.2f}")
    print(f"Total de produtos: {produtos_vendidos}")
    
    # Classificação
    if total_vendas > 20000:
        status = "Excelente"
    elif total_vendas > 10000:
        status = "Bom"
    else:
        status = "Precisa melhorar"
    
    print(f"Status das vendas: {status}")
    
    return total_vendas

# Executar desafio
resultado = analisar_vendas()

print("\n" + "=" * 60)
print("PYTHON ESSENCIAL CONCLUÍDO!")
print("Você aprendeu os 20% mais importantes!")
print("=" * 60)
