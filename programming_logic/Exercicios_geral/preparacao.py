# BLOCO 2: Nível Iniciante (Estruturas Condicionais)

# 1. Classificador de Números
""" 
def classificador():
    n = int(input("Digite um numero qualquer: "))
    if n % 2 == 0:
        print(f"O Numero {n} é PAR")
    else:
        print(f"O Numero {n} é IMPAR")
    print("Zero" if n == 0 else "Positivo" if n > 0 else "Negativo")

classificador()
"""

# 2. Cálculo de Média Acadêmica
""" 
def media_aritimetica():
    n = float(input("Digite dua nota 1: "))
    n2 = float(input("Digite dua nota 2: "))
    n3 = float(input("Digite dua nota 3: "))
    n4 = float(input("Digite dua nota 4: "))
    
    media = (n + n2 + n3 + n4) / 4
    print(f'Sua média foi: {media:.2f}')
    
    print("Aprovado" if media >= 7 else "Recuperação" if 5 <= media <= 6.9 else "Reprovado")


media_aritimetica()
"""
# Bloco 3: Nivel Intermediário

# 3. Tabuada
""" 
def tabuada():
    n = int(input("Escolha um numero qualquer: "))
    for i in range(1, 11):
        print(f'{n} x {i} = {n * i}')

tabuada()
 """

# 4. Somatorio

def somatorio():
    lista = []

    for i in range(10):
        n = int(input("Digite um numero qualquer: "))
        lista.append(n)

    soma = 0
    for item in lista:
        soma += item

    print(f'A soma de todos numeros da lista é: {soma}')
    # soma = sum(lista)
    # print(soma)

    maior = lista[0]
    for item in lista:
        if item > maior:
            maior = item
    
    print(f'O Maior nomero na lista é: {maior}')

    menor = lista[0]
    for i in lista:
        if i < menor:
            menor = i
    
    print(f'O menor numero na lista é: {menor}')

    lista_50 = []
    for i in lista:
        if i > 50:
            lista_50.append(i)

    print(f'Os numeros da lista que são maiores que 50 são {lista_50}')


    """ lista_ordenada = lista.sort()
    print("A metade maior da lista abaixo: ")
    print(lista[-1])
    print(lista[-2])
    print(lista[-3])
    print(lista[-4])
    print(lista[-5]) """

somatorio()

    























