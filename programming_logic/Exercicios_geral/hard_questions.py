"""
vendas = [150.0, 500.0, 1250.50, 499.99, 720.0, 2300.0, 45.90, 890.10, 501.0, 300.0]


nova_lista = []

for i in vendas:
    if i > 500:
        nova_lista.append(i)

print(nova_lista) 
"""

""" 
nova_lista = [i for i in vendas if i > 500 ]
print(nova_lista)
"""

# 2.
""" 
atrasos = [2, -1, 5, 0, -3, 1, 0, 4, -2, 3]

def ruptura():
    for i in atrasos:
        if i > 0:
            print('Ruptura')
        else:
            print('No prazo')


print(ruptura())
 """

# 3.
""" 
vendas_promotores = [1500, 750, 450, 1100, 600, 950, 200, 1300, 500, 800]

def bonus():
    for i in vendas_promotores:
        if i > 1000:
            print(f'Para maior que 1000 vendas o bonus é de 10% {i} --> {i * 1.1}')
        elif 500 < i <= 1000:
            print(f'Vendas entre 501 e 1000 o bonus é 5% {i} --> {i * 1.05}')
        else:
            print(f'O bonus para menos de 501 vendas é 0 --> {i}')

a = bonus()
print(a)
 """

# 4.
""" 
pedidos = ["Pipoca", "Refrigerante", "Pipoca", "Chocolate", "Pipoca", "Chiclete", "Pipoca", "Refrigerante", "Pipoca", "Chiclete"]

count = 0
pedido_alvo = 'Pipoca'
for i in pedidos:
    if i == pedido_alvo:
        count += 1

print(f'{pedido_alvo} aparece {count} vezes na lista')
 """

# 5.
"""
precos_produtos = {
    "Pipoca": 5.50,
    "Refrigerante": 3.50,
    "Chocolate": 4.00,
    "Chiclete": 1.50,
    "Água": 2.00,
    "Suco": 4.50
}


user_ask = input("Qual produto voce quer: ")
preco = precos_produtos.get(user_ask)

if user_ask in precos_produtos:
    print(f'O valor do seu pedido é {precos_produtos.get(user_ask)}')
else:
    print('Invalido, produto nao existe!')
 """
# 5. Busca flexivel maiúscula/minúscula
""" 
produto_pedido = input("Qual produto voce quer? ").lower()

preco = None

for chave, valor in precos_produtos.items():
    if chave.lower() == produto_pedido.lower():
        preco = valor
        break
    
if preco:
    print(f'O valor a pagar é {preco}')
else:
    print('produto nao existe')
 """

# 6.
""" 
nomes_e_valores = ["João", 150, "Maria", None, "Pedro", 250, None, "Ana", 300, None, "Carlos"]

for i in nomes_e_valores:
    if i == None:
        nomes_e_valores.remove(i)
        
print(nomes_e_valores)
 """
# 6. B
""" 
nomes_e_valores = ["João", 150, "Maria", None, "Pedro", 250, None, "Ana", 300, None, "Carlos"]

nome_valores_limpa = [i for i in nomes_e_valores if i != None]
print(nome_valores_limpa)

# [item for item in lista if condição]
"""

# 7.
""" 
promotores = {
    "João": 2500,
    "Maria": 3100,
    "Pedro": 1800,
    "Ana": 2900,
    "Carlos": 2200
}

promotor_maior = promotores.get("João")
for chave, valor in promotores.items():
    if valor > promotor_maior:
        promotor_maior = valor
    else:
        continue

print(promotor_maior)
 """
 
# 8.
""" 
notas_nps = [5, 4, 5, 3, 5, 5, 4, 2, 5, 5, 5, 3, 5, 5, 4, 5, 2, 5, 5, 5]
count = 0
for i in notas_nps:
    if i == 5:
        count = count + 1
    else:
        continue

media = count / len(notas_nps) * 100
print(f'{media}%')
"""
 
 # 9.
""" 
estoque_inicial = 50

while True:
    n = int(input("Digite a qntd desejada: "))
    if n <= 0:
        print('Valores negativos e nulos nao permitidos!')
        continue
    if n > estoque_inicial:
        print("Valor fornecido maior que estoque atual!")
        continue  
    if estoque_inicial > 0:
        estoque_inicial = estoque_inicial - n
        print(estoque_inicial)
    if estoque_inicial == 0:
        print("Estoque zerado!")
        break
    elif estoque_inicial < 0:
        print('Estoque zerado!')
        break
 """

# 10. 
""" 
def gondola_func(preco_estimado, preco_real):
    diferenca = abs(preco_estimado - preco_real)
    total = (preco_real + preco_estimado)
    gondola_test = (diferenca / total) * 100
    if gondola_test > 10:
        print(f'A difereça é de {gondola_test:.2f}%')
        return 'Alerta de Gondola'
    else:
        print(f'A difereça é de {gondola_test:.2f}%')
        return 'Ok'

print(gondola_func(50, 100))
print(gondola_func(50, 61))
 """





































"""MEDIUM-HARD Questions"""














