"""
NUMPY BÁSICO - FUNDAMENTOS GERAIS
Os 20% mais importantes para 80% do uso em Data Science
"""

import numpy as np

print("=" * 60)
print("NUMPY BÁSICO - FUNDAMENTOS")
print("=" * 60)

# 1. CRIAÇÃO DE ARRAYS ESSENCIAIS
print("\n1. CRIAÇÃO DE ARRAYS")
print("-" * 30)

# Array a partir de lista
lista = [1, 2, 3, 4, 5]
arr = np.array(lista)
print(f"Lista: {lista}")
print(f"Array: {arr}")
print(f"Tipo: {type(arr)}")
print(f"Shape: {arr.shape}")
print(f"Dtype: {arr.dtype}")

# Arrays com zeros e uns
zeros = np.zeros(5)
uns = np.ones(5)
print(f"Zeros: {zeros}")
print(f"Uns: {uns}")

# Array com range
range_arr = np.arange(0, 10, 2)
print(f"Arange (0,10,2): {range_arr}")

# Array com espaçamento linear
linspace = np.linspace(0, 10, 5)
print(f"Linspace (0,10,5): {linspace}")

# Array 2D
matriz = np.array([[1, 2, 3], [4, 5, 6]])
print(f"Matriz 2x3:\n{matriz}")
print(f"Shape: {matriz.shape}")

# 2. OPERAÇÕES VETORIZADAS
print("\n2. OPERAÇÕES VETORIZADAS")
print("-" * 30)

# Operações básicas
arr = np.array([1, 2, 3, 4, 5])
print(f"Array original: {arr}")
print(f"Array + 10: {arr + 10}")
print(f"Array * 2: {arr * 2}")
print(f"Array ** 2: {arr ** 2}")

# Operações entre arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print(f"\nArray1: {arr1}")
print(f"Array2: {arr2}")
print(f"Soma: {arr1 + arr2}")
print(f"Multiplicação: {arr1 * arr2}")

# Funções matemáticas
arr = np.array([1, 4, 9, 16, 25])
print(f"\nArray: {arr}")
print(f"Raiz quadrada: {np.sqrt(arr)}")
print(f"Log: {np.log(arr)}")
print(f"Exp: {np.exp(arr)}")

# Estatísticas básicas
dados = np.array([10, 20, 30, 40, 50])
print(f"\nDados: {dados}")
print(f"Média: {np.mean(dados)}")
print(f"Mediana: {np.median(dados)}")
print(f"Desvio padrão: {np.std(dados)}")
print(f"Mínimo: {np.min(dados)}")
print(f"Máximo: {np.max(dados)}")
print(f"Soma: {np.sum(dados)}")

# 3. INDEXAÇÃO E SLICING
print("\n3. INDEXAÇÃO E SLICING")
print("-" * 30)

# Array 1D
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(f"Array: {arr}")
print(f"Elemento [0]: {arr[0]}")
print(f"Elemento [-1]: {arr[-1]}")
print(f"Slice [2:5]: {arr[2:5]}")
print(f"Slice [:3]: {arr[:3]}")
print(f"Slice [7:]: {arr[7:]}")
print(f"Slice [::2]: {arr[::2]}")

# Array 2D
matriz = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
])
print(f"\nMatriz 3x4:\n{matriz}")
print(f"Elemento [0,0]: {matriz[0, 0]}")
print(f"Linha 1: {matriz[1]}")
print(f"Coluna 2: {matriz[:, 2]}")
print(f"Submatriz [0:2, 1:3]:\n{matriz[0:2, 1:3]}")

# Indexação booleana
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
mask = arr > 5
print(f"\nArray: {arr}")
print(f"Mask (arr > 5): {mask}")
print(f"Elementos > 5: {arr[mask]}")
print(f"Elementos pares: {arr[arr % 2 == 0]}")

# 4. MANIPULAÇÃO DE ARRAYS
print("\n4. MANIPULAÇÃO DE ARRAYS")
print("-" * 30)

# Reshape
arr = np.arange(12)
print(f"Array original: {arr}")
reshaped = arr.reshape(3, 4)
print(f"Reshape (3,4):\n{reshaped}")

# Flatten
print(f"Flatten: {reshaped.flatten()}")

# Transposição
matriz = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\nMatriz original:\n{matriz}")
print(f"Transposta:\n{matriz.T}")

# Concatenação
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
concatenado = np.concatenate([arr1, arr2])
print(f"\nConcatenado: {concatenado}")

# Empilhamento
stacked_v = np.vstack([arr1, arr2])
stacked_h = np.hstack([arr1, arr2])
print(f"Stack vertical:\n{stacked_v}")
print(f"Stack horizontal: {stacked_h}")

# 5. OPERAÇÕES COM MATRIZES
print("\n5. OPERAÇÕES COM MATRIZES")
print("-" * 30)

# Produto escalar
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
dot_product = np.dot(v1, v2)
print(f"Vetor 1: {v1}")
print(f"Vetor 2: {v2}")
print(f"Produto escalar: {dot_product}")

# Produto matricial
mat1 = np.array([[1, 2], [3, 4]])
mat2 = np.array([[5, 6], [7, 8]])
print(f"\nMatriz 1:\n{mat1}")
print(f"Matriz 2:\n{mat2}")
print(f"Produto matricial:\n{np.dot(mat1, mat2)}")

# 6. FILTROS E CONDIÇÕES
print("\n6. FILTROS E CONDIÇÕES")
print("-" * 30)

# where
arr = np.array([10, 20, 30, 40, 50])
condicao = arr > 25
resultado = np.where(condicao, "Alto", "Baixo")
print(f"Array: {arr}")
print(f"Condição (>25): {resultado}")

# Múltiplas condições
idades = np.array([15, 22, 35, 12, 28, 45])
categorias = np.where(
    idades < 18, "Menor",
    np.where(idades < 30, "Jovem", "Adulto")
)
print(f"\nIdades: {idades}")
print(f"Categorias: {categorias}")

# 7. ESTATÍSTICAS AVANÇADAS
print("\n7. ESTATÍSTICAS AVANÇADAS")
print("-" * 30)

# Correlação
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
correlacao = np.corrcoef(x, y)
print(f"Array X: {x}")
print(f"Array Y: {y}")
print(f"Correlação:\n{correlacao}")

# Percentis
dados = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(f"\nDados: {dados}")
print(f"Percentil 25: {np.percentile(dados, 25)}")
print(f"Percentil 50 (mediana): {np.percentile(dados, 50)}")
print(f"Percentil 75: {np.percentile(dados, 75)}")

# 8. GERAÇÃO DE DADOS ALEATÓRIOS
print("\n8. DADOS ALEATÓRIOS")
print("-" * 30)

# Semente para reprodutibilidade
np.random.seed(42)

# Inteiros aleatórios
int_aleatorios = np.random.randint(0, 100, 10)
print(f"Inteiros aleatórios (0-99, 10 elementos): {int_aleatorios}")

# Floats aleatórios
float_aleatorios = np.random.random(5)
print(f"Floats aleatórios (5 elementos): {float_aleatorios}")

# Distribuição normal
normal = np.random.normal(0, 1, 1000)
print(f"\nDados normais (média={np.mean(normal):.2f}, std={np.std(normal):.2f})")
print(f"Média: {np.mean(normal):.4f}")
print(f"Desvio padrão: {np.std(normal):.4f}")

# 9. APLICAÇÃO PRÁTICA - ANÁLISE DE DADOS
print("\n9. APLICAÇÃO PRÁTICA")
print("-" * 30)

# Simular dados de vendas
np.random.seed(42)
vendas_diarias = np.random.normal(1000, 200, 30)  # 30 dias
vendas_diarias = np.maximum(vendas_diarias, 0)  # não negativo

print("Análise de Vendas (30 dias):")
print(f"Vendas médias: R${np.mean(vendas_diarias):.2f}")
print(f"Venda máxima: R${np.max(vendas_diarias):.2f}")
print(f"Venda mínima: R${np.min(vendas_diarias):.2f}")
print(f"Desvio padrão: R${np.std(vendas_diarias):.2f}")

# Dias acima da média
dias_acima_media = vendas_diarias[vendas_diarias > np.mean(vendas_diarias)]
print(f"Dias acima da média: {len(dias_acima_media)}")
print(f"Percentual: {len(dias_acima_media)/len(vendas_diarias)*100:.1f}%")

# Crescimento semana a semana
semanas = vendas_diarias.reshape(4, 7)  # 4 semanas, 7 dias
media_semanal = np.mean(semanas, axis=1)
print(f"\nMédia semanal:")
for i, media in enumerate(media_semanal, 1):
    print(f"  Semana {i}: R${media:.2f}")

# 10. DESAFIO INTEGRADOR
print("\n10. DESAFIO INTEGRADOR")
print("-" * 30)

def analisar_dataset_simulado():
    """Análise completa de um dataset simulado."""
    
    # Gerar dados simulados
    np.random.seed(123)
    n_amostras = 100
    
    # Features
    idade = np.random.normal(35, 10, n_amostras)
    salario = np.random.normal(5000, 1500, n_amostras)
    experiencia = np.random.exponential(5, n_amostras)
    
    # Garantar valores positivos
    idade = np.maximum(idade, 18)
    salario = np.maximum(salario, 1000)
    
    # Target (simulado)
    score = 0.3 * (idade / 60) + 0.4 * (salario / 10000) + 0.3 * (experiencia / 10)
    score = score + np.random.normal(0, 0.1, n_amostras)  # ruído
    score = np.clip(score, 0, 1)
    
    # Análise
    print("ANÁLISE DE DATASET SIMULADO")
    print("=" * 40)
    print(f"Amostras: {n_amostras}")
    
    print(f"\nEstatísticas Idade:")
    print(f"  Média: {np.mean(idade):.1f} anos")
    print(f"  Desvio: {np.std(idade):.1f} anos")
    print(f"  Min-Max: {np.min(idade):.1f} - {np.max(idade):.1f}")
    
    print(f"\nEstatísticas Salário:")
    print(f"  Média: R${np.mean(salario):.2f}")
    print(f"  Desvio: R${np.std(salario):.2f}")
    print(f"  Min-Max: R${np.min(salario):.2f} - R${np.max(salario):.2f}")
    
    print(f"\nEstatísticas Experiência:")
    print(f"  Média: {np.mean(experiencia):.1f} anos")
    print(f"  Desvio: {np.std(experiencia):.1f} anos")
    
    print(f"\nEstatísticas Score:")
    print(f"  Média: {np.mean(score):.3f}")
    print(f"  Desvio: {np.std(score):.3f}")
    
    # Correlações
    corr_idade_salario = np.corrcoef(idade, salario)[0, 1]
    corr_idade_score = np.corrcoef(idade, score)[0, 1]
    corr_salario_score = np.corrcoef(salario, score)[0, 1]
    
    print(f"\nCorrelações:")
    print(f"  Idade vs Salário: {corr_idade_salario:.3f}")
    print(f"  Idade vs Score: {corr_idade_score:.3f}")
    print(f"  Salário vs Score: {corr_salario_score:.3f}")
    
    # Classificação
    score_alto = score[score > np.percentile(score, 75)]
    score_baixo = score[score < np.percentile(score, 25)]
    
    print(f"\nClassificação por Score:")
    print(f"  Score alto (>75º percentil): {len(score_alto)} pessoas")
    print(f"  Score baixo (<25º percentil): {len(score_baixo)} pessoas")
    
    return {
        "idade": idade,
        "salario": salario,
        "experiencia": experiencia,
        "score": score
    }

# Executar desafio
dataset = analisar_dataset_simulado()

print("\n" + "=" * 60)
print("NUMPY BÁSICO CONCLUÍDO!")
print("Você domina os 20% mais importantes!")
print("=" * 60)
