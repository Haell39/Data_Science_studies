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






















































"""MEDIUM-HARD Questions"""














