# 1. 

""" for i in range(1, 11):
    print(i)
 """

# 2. 
""" 
vendas = [10, 5, 7, 89, 105]
soma = 0
for i in vendas:
    soma +=i


print(f'A soma dos valores da lista é {soma}')
"""

# 3.
""" 
list = [5, 0, 12, 0, 8]

count = 0
for i in list:
    if i == 0:
        count +=1
print(count)
 """

# 4.
""" 
def tabuada():
    x = int(input("Digite um numero: "))
    for n in range(1, 11):
        print(f'{x} x {n} = {x * n}')

tabuada()

 """

# 5.
""" 
list = ["doce", 'shampoo', 'Shampoo', 'xampu', 'play']
count = 0
for i in list:
    if i == 'Shampoo':
        count += 1
        print(f'Ja tem o item {i} {count} vezes')

 """
# segundo jeito:
""" 
lista = ["doce", 'shampoo', 'Shampoo', 'xampu', 'play']
count = 0
for i in lista:
    if i.lower() == 'shampoo':
        count += 1
        # print(f'Tem um total de {count} {i} na lista')

print(f'O item shampoo aparece {count} vezes na lista')
 """

# 6.
""" 
vendas = [5, 0, 12, 0, 80, 70, 54, 1]       

def maior_venda(vendas):
    if vendas == []: #if not vendas:
        return None
    
    maior = vendas[0]
    for i in vendas:
        if i > maior:
            maior = i
    return maior
            
a = maior_venda(vendas)
print(a)
 """

# 7.

lista_tempo = []
nome_promotor = input("Digite Seu Nome: ")
for i in range(1, 6):
    tempo = int(input(f"Diga o tempo da sua {i}ª visita: "))
    lista_tempo.append(tempo)

print(lista_tempo)

media_lista_tempo = sum(lista_tempo) / len(lista_tempo)
print(f'O promotor {nome_promotor} teve uma média de {media_lista_tempo}h nas 5 visitas!')


# 8.
""" 
name = input("Digite seu nome: ")

print(name[::-1].capitalize())
 """
 
# 9. 

""" 
estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

escolhidos = []
for i in estados:
    if i == 'PE':
        pernambuco = i
        escolhidos.append(pernambuco)
    if i == 'SP':
        saopaolo = i
        escolhidos.append(saopaolo)
        
print(escolhidos)
 """
 
 # 9. B
"""  
estados_alvo = ['PE', 'SP']
estados_verify = []
estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
] 

# for i in estados:
#     if i in estados_alvo:
#         estados_verify.append(i)

# estados_verify = [i for i in estados if i in estados_alvo] --> list comprehension

print(estados_verify)
 """

# 10.

""" 
nota_ips = int(input("Digite sua nota IPS entre 1 e 5: "))
while True:
    if nota_ips > 5 or nota_ips < 1:
        nota_ips = int(input("Digite sua nota IPS entre 1 e 5: "))
    else:
        print('Obrigado')
        break

 """
















