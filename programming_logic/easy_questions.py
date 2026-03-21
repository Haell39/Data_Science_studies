# 1.
""" 
a = int(input("Enter a number: "))
b = int(input("Enter a number: "))

print(a + b)

 """
# 2.

""" 
time = int(input("Enter time in DAYS: "))

hours = time * 24
print(f'{time} days in hours is {hours}h1')
 """


# 3.
""" 
a = int(input("Enter your note 1: "))
b = int(input("Enter your note 2: "))
c = int(input("Enter your note 3: "))

media = a + b + c / 3
media = (a + b + c) / 3
print(f"{media:.2f}")

 """

""" 
# 4.
q = int(input("Enter a quantidade de estoque: "))
if q < 10:
    print('Estoque insuficiente!')
else:
    print('Ok!')
 """


""" 
while True:
    s = input("Quantidade disponível (ou 'sair' para encerrar): ")
    if s.lower() == 'sair':
        print("Encerrado.")
        break
    try:
        q = int(s)
    except ValueError:
        print("Entrada inválida. Tente novamente.")
        continue
    if q >= 10:
        print("Estoque suficiente.")
        break
    print("Estoque baixo. Informe novamente.") 
"""

""" 
# 4. versao pro
while True:
    s = input("Quantidade ou sair pra sair: ")
    if s.lower() == 'sair':
        print("FIM")
        break
    q = int(input("Enter your product quantity: "))
    if q >= 10:
        print('Suficiente')
        break
    print('esoque baixo tente dnv!')

 """

#5.
""" 
frete = input('Digite o estado: ')
if frete == 'PE':
    print('R$ 20,00')
else:
    print('R$ 10,00')
 """

# 6. 

""" 
def par_impar():
    n = int(input("Digite um numero: "))
    print('par' if n % 2 == 0 else 'impar')


par_impar()
 """


# 7.

""" 
def eh_maior():
    age = int(input("Diga sua idade: "))
    print('Adulto' if age >= 18 else 'criança')

eh_maior()
 """


# 8. 

""" 
def bonus():
    venda = int(input('Digite o valor de sua venda: '))
    return venda * 1.1 if venda > 1000 else venda * 1

print(f'{bonus():.2f}')
 """

# 9. 
""" 
estoque = int(input("Digite o saldo do estoque: "))

print('positivo' if estoque > 0 else 'negativo' if estoque < 0 else 'Nulo')
 """

# 10.
""" 
a = int(input("Digite o preço do produto 1: "))
b = int(input("Digite o preço do produto 2: "))

print('Produto 1 maior' if a > b else 'Produto 2 maior' if b > a else 'Identicos') """