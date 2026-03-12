"""
PANDAS ESSENCIAL - FUNDAMENTOS GERAIS
Os 20% mais importantes para 80% do uso em Data Science
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("PANDAS ESSENCIAL - FUNDAMENTOS")
print("=" * 60)

# 1. SERIES - ESTRUTURA BÁSICA
print("\n1. SERIES")
print("-" * 30)

# Criar Series a partir de lista
dados = [10, 20, 30, 40, 50]
series = pd.Series(dados)
print(f"Series básica:\n{series}")
print(f"Tipo: {type(series)}")
print(f"Valores: {series.values}")
print(f"Índice: {series.index}")

# Series com índice personalizado
series_nomes = pd.Series([25, 30, 35, 28], 
                        index=['Ana', 'Bruno', 'Carla', 'Daniel'])
print(f"\nSeries com nomes:\n{series_nomes}")

# Acesso em Series
print(f"\nAcesso:")
print(f"Idade de Ana: {series_nomes['Ana']}")
print(f"Primeira idade: {series_nomes[0]}")
print(f"Idades > 28:\n{series_nomes[series_nomes > 28]}")

# 2. DATAFRAMES - ESTRUTURA PRINCIPAL
print("\n2. DATAFRAMES")
print("-" * 30)

# Criar DataFrame a partir de dicionário
dados_dict = {
    'nome': ['Ana', 'Bruno', 'Carla', 'Daniel'],
    'idade': [25, 30, 35, 28],
    'cidade': ['São Paulo', 'Rio', 'Belo Horizonte', 'Porto Alegre'],
    'salario': [5000, 6000, 7000, 5500]
}
df = pd.DataFrame(dados_dict)
print("DataFrame básico:")
print(df)

# Informações básicas
print(f"\nInformações do DataFrame:")
print(f"Shape: {df.shape}")
print(f"Colunas: {list(df.columns)}")
print(f"Tipos de dados:\n{df.dtypes}")

# Criar DataFrame a partir de lista de dicionários
dados_lista = [
    {'produto': 'Laptop', 'preco': 5000, 'estoque': 10},
    {'produto': 'Mouse', 'preco': 150, 'estoque': 50},
    {'produto': 'Teclado', 'preco': 200, 'estoque': 30}
]
df_produtos = pd.DataFrame(dados_lista)
print(f"\nDataFrame de produtos:")
print(df_produtos)

# 3. LEITURA DE DADOS
print("\n3. LEITURA DE DADOS")
print("-" * 30)

# Criar dados CSV simulados em memória
from io import StringIO

csv_data = """nome,idade,cidade,salario
Ana,25,São Paulo,5000
Bruno,30,Rio,6000
Carla,35,Belo Horizonte,7000
Daniel,28,Porto Alegre,5500
Elena,22,Salvador,4500
Fabio,40,Recife,8000
"""

# Ler CSV
df_csv = pd.read_csv(StringIO(csv_data))
print("DataFrame lido de CSV:")
print(df_csv)

# 4. SELEÇÃO E FILTRAGEM
print("\n4. SELEÇÃO E FILTRAGEM")
print("-" * 30)

df = df_csv.copy()

# Selecionar colunas
print("Seleção de colunas:")
print(f"Coluna 'nome':\n{df['nome']}")
print(f"Colunas ['nome', 'salario']:\n{df[['nome', 'salario']]}")

# Seleção por posição (iloc)
print(f"\nPrimeiras 3 linhas (iloc[:3]):")
print(df.iloc[:3])
print(f"Linha 1, coluna 0 (iloc[1,0]): {df.iloc[1, 0]}")

# Seleção por rótulo (loc)
print(f"\nLinha 2 (loc[2]):")
print(df.loc[2])

# Filtragem condicional
print(f"\nFiltragem - Idade > 30:")
print(df[df['idade'] > 30])

print(f"\nFiltragem - Salário > 5000:")
print(df[df['salario'] > 5000])

# Múltiplas condições
print(f"\nFiltragem - Idade > 25 E Salário < 6000:")
print(df[(df['idade'] > 25) & (df['salario'] < 6000)])

print(f"\nFiltragem - Cidade é São Paulo OU Rio:")
print(df[df['cidade'].isin(['São Paulo', 'Rio'])])

# 5. OPERAÇÕES BÁSICAS
print("\n5. OPERAÇÕES BÁSICAS")
print("-" * 30)

# Estatísticas descritivas
print("Estatísticas descritivas:")
print(df.describe())

# Estatísticas por coluna
print(f"\nEstatísticas específicas:")
print(f"Média de idade: {df['idade'].mean():.1f}")
print(f"Mediana do salário: R${df['salario'].median():.2f}")
print(f"Desvio padrão do salário: R${df['salario'].std():.2f}")
print(f"Contagem por cidade:\n{df['cidade'].value_counts()}")

# Ordenação
print(f"\nOrdenado por idade (crescente):")
print(df.sort_values('idade'))

print(f"\nOrdenado por salário (decrescente):")
print(df.sort_values('salario', ascending=False))

# 6. MANIPULAÇÃO DE COLUNAS
print("\n6. MANIPULAÇÃO DE COLUNAS")
print("-" * 30)

df = df_csv.copy()

# Adicionar coluna
df['bonus'] = df['salario'] * 0.1
print("DataFrame com coluna 'bonus':")
print(df)

# Modificar coluna
df['salario_ajustado'] = df['salario'] + df['bonus']
print(f"\nCom salário ajustado:")
print(df[['nome', 'salario', 'bonus', 'salario_ajustado']])

# Coluna condicional
df['faixa_etaria'] = np.where(df['idade'] < 30, 'Jovem', 
                              np.where(df['idade'] < 40, 'Adulto', 'Sênior'))
print(f"\nCom faixa etária:")
print(df[['nome', 'idade', 'faixa_etaria']])

# Remover coluna
df_sem_bonus = df.drop('bonus', axis=1)
print(f"\nSem coluna 'bonus':")
print(df_sem_bonus.columns)

# 7. AGRUPAMENTO
print("\n7. AGRUPAMENTO (GROUPBY)")
print("-" * 30)

# Agrupar por cidade
agrupado_cidade = df.groupby('cidade')['salario'].agg(['mean', 'count', 'std'])
print("Salários por cidade:")
print(agrupado_cidade)

# Agrupamento múltiplo
df['categoria_salario'] = np.where(df['salario'] > 6000, 'Alto', 
                                  np.where(df['salario'] > 4000, 'Médio', 'Baixo'))
agrupado_multi = df.groupby(['cidade', 'categoria_salario']).size().unstack()
print(f"\nDistribuição por cidade e categoria salarial:")
print(agrupado_multi)

# 8. TRATAMENTO DE DADOS AUSENTES
print("\n8. DADOS AUSENTES")
print("-" * 30)

# Criar DataFrame com dados ausentes
df_com_missing = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carla', 'Daniel', None],
    'idade': [25, None, 35, 28, 22],
    'salario': [5000, 6000, None, 5500, 4500],
    'cidade': ['São Paulo', 'Rio', None, 'Porto Alegre', 'Salvador']
})

print("DataFrame com dados ausentes:")
print(df_com_missing)

# Verificar dados ausentes
print(f"\nDados ausentes por coluna:")
print(df_com_missing.isnull().sum())

# Remover linhas com dados ausentes
df_sem_missing = df_com_missing.dropna()
print(f"\nSem linhas com dados ausentes:")
print(df_sem_missing)

# Preencher dados ausentes
df_preenchido = df_com_missing.copy()
df_preenchido['idade'] = df_preenchido['idade'].fillna(df_preenchido['idade'].mean())
df_preenchido['salario'] = df_preenchido['salario'].fillna(df_preenchido['salario'].median())
df_preenchido['cidade'] = df_preenchido['cidade'].fillna('Não informada')
df_preenchido['nome'] = df_preenchido['nome'].fillna('Sem nome')

print(f"\nDados preenchidos:")
print(df_preenchido)

# 9. JUNÇÃO DE DATAFRAMES
print("\n9. JUNÇÃO DE DATAFRAMES")
print("-" * 30)

# DataFrame de departamentos
deptos = pd.DataFrame({
    'cidade': ['São Paulo', 'Rio', 'Belo Horizonte', 'Porto Alegre', 'Salvador'],
    'departamento': ['TI', 'Vendas', 'RH', 'Financeiro', 'Marketing'],
    'regiao': ['Sudeste', 'Sudeste', 'Sudeste', 'Sul', 'Nordeste']
})

print("DataFrame de departamentos:")
print(deptos)

# Merge (join)
df_completo = pd.merge(df, deptos, on='cidade', how='left')
print(f"\nDataFrame completo (merge):")
print(df_completo)

# Concat (empilhamento)
df_extra = pd.DataFrame({
    'nome': ['Gabriel', 'Helena'],
    'idade': [32, 27],
    'cidade': ['Curitiba', 'Brasília'],
    'salario': [5200, 4800]
})

df_concatenado = pd.concat([df, df_extra], ignore_index=True)
print(f"\nDataFrame concatenado:")
print(df_concatenado)

# 10. EXPORTAÇÃO DE DADOS
print("\n10. EXPORTAÇÃO DE DADOS")
print("-" * 30)

# Para CSV (em memória)
csv_output = df.to_csv(index=False)
print("DataFrame exportado para CSV:")
print(csv_output[:200] + "...")

# Para Excel (simulado)
print("\nDataFrame pode ser exportado com:")
print("df.to_excel('dados.xlsx', index=False)")
print("df.to_json('dados.json', orient='records')")
print("df.to_csv('dados.csv', index=False)")

# 11. APLICAÇÃO PRÁTICA
print("\n11. APLICAÇÃO PRÁTICA")
print("-" * 30)

# Simular dados de vendas
np.random.seed(42)
n_vendas = 100

dados_vendas = {
    'data_venda': pd.date_range('2023-01-01', periods=n_vendas, freq='D'),
    'produto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor'], n_vendas),
    'quantidade': np.random.randint(1, 10, n_vendas),
    'valor_unitario': np.random.choice([5000, 150, 200, 1200], n_vendas),
    'vendedor': np.random.choice(['Ana', 'Bruno', 'Carla'], n_vendas),
    'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], n_vendas)
}

df_vendas = pd.DataFrame(dados_vendas)
df_vendas['valor_total'] = df_vendas['quantidade'] * df_vendas['valor_unitario']

print("Dataset de Vendas:")
print(f"Shape: {df_vendas.shape}")
print(f"\nPrimeiras linhas:")
print(df_vendas.head())

print(f"\nEstatísticas das vendas:")
print(df_vendas[['quantidade', 'valor_unitario', 'valor_total']].describe())

# Análise por produto
vendas_produto = df_vendas.groupby('produto')['valor_total'].agg(['sum', 'count', 'mean'])
print(f"\nVendas por produto:")
print(vendas_produto)

# Análise por vendedor
vendas_vendedor = df_vendas.groupby('vendedor')['valor_total'].sum().sort_values(ascending=False)
print(f"\nVendas por vendedor:")
print(vendas_vendedor)

# 12. DESAFIO INTEGRADOR
print("\n12. DESAFIO INTEGRADOR")
print("-" * 30)

def analisar_dataset_completo():
    """Análise completa de um dataset simulado."""
    
    # Gerar dados simulados
    np.random.seed(123)
    n_funcionarios = 200
    
    dados = {
        'id_funcionario': range(1, n_funcionarios + 1),
        'nome': [f'Func_{i}' for i in range(n_funcionarios)],
        'departamento': np.random.choice(['TI', 'Vendas', 'RH', 'Financeiro', 'Marketing'], n_funcionarios),
        'idade': np.random.normal(35, 8, n_funcionarios),
        'salario': np.random.normal(6000, 2000, n_funcionarios),
        'anos_empresa': np.random.exponential(5, n_funcionarios),
        'performance': np.random.uniform(0, 10, n_funcionarios),
        'satisfacao': np.random.uniform(1, 5, n_funcionarios)
    }
    
    df = pd.DataFrame(dados)
    
    # Ajustar dados
    df['idade'] = np.maximum(df['idade'], 18).astype(int)
    df['salario'] = np.maximum(df['salario'], 2000).round(2)
    df['anos_empresa'] = np.maximum(df['anos_empresa'], 0.5).round(1)
    
    # Análise
    print("ANÁLISE COMPLETA DE DATASET DE RH")
    print("=" * 50)
    print(f"Total de funcionários: {len(df)}")
    
    # Estatísticas gerais
    print(f"\nEstatísticas gerais:")
    print(f"Idade média: {df['idade'].mean():.1f} anos")
    print(f"Salário médio: R${df['salario'].mean():.2f}")
    print(f"Tempo médio na empresa: {df['anos_empresa'].mean():.1f} anos")
    print(f"Performance média: {df['performance'].mean():.2f}")
    print(f"Satisfação média: {df['satisfacao'].mean():.2f}")
    
    # Análise por departamento
    print(f"\nAnálise por departamento:")
    dept_stats = df.groupby('departamento').agg({
        'salario': ['mean', 'count'],
        'performance': 'mean',
        'satisfacao': 'mean'
    }).round(2)
    print(dept_stats)
    
    # Correlações
    correlacoes = df[['idade', 'salario', 'anos_empresa', 'performance', 'satisfacao']].corr()
    print(f"\nMatriz de correlação:")
    print(correlacoes.round(3))
    
    # Categorias
    df['faixa_salario'] = pd.cut(df['salario'], 
                                bins=[0, 4000, 7000, 10000, float('inf')],
                                labels=['Baixo', 'Médio', 'Alto', 'Muito Alto'])
    
    print(f"\nDistribuição salarial:")
    print(df['faixa_salario'].value_counts())
    
    # Top performers
    top_performers = df.nlargest(5, 'performance')[['nome', 'departamento', 'salario', 'performance']]
    print(f"\nTop 5 Performers:")
    print(top_performers)
    
    return df

# Executar desafio
dataset_rh = analisar_dataset_completo()

print("\n" + "=" * 60)
print("PANDAS ESSENCIAL CONCLUÍDO!")
print("Você domina os 20% mais importantes!")
print("=" * 60)
