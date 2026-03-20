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

list = ["doce", 'shampoo', 'Shampoo', 'xampu', 'play']
count = 0
for item in list:
    if item.lower() == 'shampoo':
        count += 1
print(f'Tem um total de {count} {item} na lista')
















