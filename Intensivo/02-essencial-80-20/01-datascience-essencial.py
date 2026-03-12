"""
DATA SCIENCE ESSENCIAL - 80/20
Os 20% mais importantes para resolver 80% dos problemas reais
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("DATA SCIENCE ESSENCIAL - 80/20")
print("=" * 70)

# 1. CARREGAMENTO E EXPLORAÇÃO DE DADOS REAIS
print("\n1. CARREGAMENTO E EXPLORAÇÃO DE DADOS")
print("-" * 50)

# Gerar dataset realista de e-commerce
np.random.seed(42)
n_registros = 2000

# Dataset de vendas e-commerce
dados = {
    'id_pedido': range(1, n_registros + 1),
    'data_pedido': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365)) 
                   for _ in range(n_registros)],
    'id_cliente': np.random.randint(1, 500, n_registros),
    'produto': np.random.choice(['Notebook', 'Celular', 'Tablet', 'Fone', 'Mouse'], 
                                n_registros, p=[0.2, 0.3, 0.15, 0.25, 0.1]),
    'categoria': np.random.choice(['Eletrônicos', 'Acessórios'], n_registros, p=[0.7, 0.3]),
    'quantidade': np.random.randint(1, 5, n_registros),
    'preco_unitario': np.random.choice([3000, 1500, 800, 300, 100], n_registros, 
                                       p=[0.2, 0.3, 0.15, 0.25, 0.1]),
    'metodo_pagamento': np.random.choice(['Cartão', 'PIX', 'Boleto', 'Débito'], 
                                        n_registros, p=[0.4, 0.3, 0.2, 0.1]),
    'cidade': np.random.choice(['São Paulo', 'Rio', 'BH', 'Porto Alegre', 'Salvador'], 
                              n_registros),
    'estado': np.random.choice(['SP', 'RJ', 'MG', 'RS', 'BA'], n_registros),
    'frete': np.random.uniform(10, 50, n_registros)
}

df = pd.DataFrame(dados)

# Adicionar dados ausentes (realista)
df.loc[np.random.choice(df.index, 50, replace=False), 'frete'] = np.nan
df.loc[np.random.choice(df.index, 30, replace=False), 'metodo_pagamento'] = np.nan

# Calcular valor total
df['valor_total'] = df['quantidade'] * df['preco_unitario'] + df['frete']

# Adicionar features derivadas
df['dia_semana'] = df['data_pedido'].dt.day_name()
df['mes'] = df['data_pedido'].dt.month
df['trimestre'] = df['data_pedido'].dt.quarter
df['final_semana'] = df['data_pedido'].dt.weekday >= 5

print(f"Dataset criado: {df.shape}")
print(f"\nInformações básicas:")
print(df.info())

print(f"\nEstatísticas descritivas:")
print(df.describe().round(2))

print(f"\nValores ausentes:")
print(df.isnull().sum())

# 2. LIMPEZA E PREPARAÇÃO DE DADOS
print("\n2. LIMPEZA E PREPARAÇÃO DE DADOS")
print("-" * 50)

# Tratar valores ausentes
# Frete - preencher com média
imputer_numeric = SimpleImputer(strategy='mean')
df['frete'] = imputer_numeric.fit_transform(df[['frete']]).flatten()

# Método pagamento - preencher com moda
imputer_categorical = SimpleImputer(strategy='most_frequent')
df['metodo_pagamento'] = imputer_categorical.fit_transform(df[['metodo_pagamento']]).flatten()

print(f"Valores ausentes após tratamento:")
print(df.isnull().sum())

# Remover outliers (método IQR)
def remover_outliers(df, coluna):
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    return df[(df[coluna] >= limite_inferior) & (df[coluna] <= limite_superior)]

print(f"\nShape antes de remover outliers: {df.shape}")
df = remover_outliers(df, 'valor_total')
print(f"Shape após remover outliers: {df.shape}")

# 3. ANÁLISE EXPLORATÓRIA AVANÇADA
print("\n3. ANÁLISE EXPLORATÓRIA AVANÇADA")
print("-" * 50)

# Análise temporal
vendas_mensais = df.groupby(df['data_pedido'].dt.to_period('M')).agg({
    'valor_total': 'sum',
    'id_pedido': 'count'
}).round(2)
vendas_mensais.columns = ['Valor_Total', 'Qtd_Pedidos']

print("Vendas mensais:")
print(vendas_mensais.head())

# Análise por produto
analise_produto = df.groupby('produto').agg({
    'valor_total': ['sum', 'mean', 'count'],
    'quantidade': 'sum'
}).round(2)
print(f"\nAnálise por produto:")
print(analise_produto)

# Análise por método pagamento
analise_pagamento = df.groupby('metodo_pagamento')['valor_total'].agg(['sum', 'count', 'mean'])
analise_pagamento.columns = ['Total', 'Transações', 'Ticket_Médio']
print(f"\nAnálise por método pagamento:")
print(analise_pagamento.round(2))

# 4. VISUALIZAÇÃO IMPACTANTE
print("\n4. VISUALIZAÇÃO IMPACTANTE")
print("-" * 50)

# Configurar estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Dashboard completo
fig = plt.figure(figsize=(20, 12))

# 1. Tendência de vendas
ax1 = plt.subplot(2, 4, 1)
vendas_diarias = df.groupby(df['data_pedido'].dt.date)['valor_total'].sum()
ax1.plot(vendas_diarias.index, vendas_diarias.values, linewidth=2)
ax1.set_title('Tendência de Vendas Diárias')
ax1.set_xlabel('Data')
ax1.set_ylabel('Valor Total')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)

# 2. Top produtos
ax2 = plt.subplot(2, 4, 2)
top_produtos = df.groupby('produto')['valor_total'].sum().sort_values()
ax2.barh(top_produtos.index, top_produtos.values)
ax2.set_title('Vendas por Produto')
ax2.set_xlabel('Valor Total')

# 3. Distribuição de valores
ax3 = plt.subplot(2, 4, 3)
ax3.hist(df['valor_total'], bins=30, alpha=0.7, edgecolor='black')
ax3.set_title('Distribuição de Valores')
ax3.set_xlabel('Valor Total')
ax3.set_ylabel('Frequência')
ax3.grid(True, alpha=0.3, axis='y')

# 4. Métodos pagamento
ax4 = plt.subplot(2, 4, 4)
pagamento_counts = df['metodo_pagamento'].value_counts()
ax4.pie(pagamento_counts.values, labels=pagamento_counts.index, autopct='%1.1f%%')
ax4.set_title('Métodos de Pagamento')

# 5. Vendas por estado
ax5 = plt.subplot(2, 4, 5)
vendas_estado = df.groupby('estado')['valor_total'].sum().sort_values()
ax5.barh(vendas_estado.index, vendas_estado.values, color='coral')
ax5.set_title('Vendas por Estado')
ax5.set_xlabel('Valor Total')

# 6. Boxplot por categoria
ax6 = plt.subplot(2, 4, 6)
sns.boxplot(data=df, x='categoria', y='valor_total', ax=ax6)
ax6.set_title('Valor por Categoria')
ax6.tick_params(axis='x', rotation=45)

# 7. Correlação
ax7 = plt.subplot(2, 4, 7)
numeric_cols = ['quantidade', 'preco_unitario', 'frete', 'valor_total']
correlacao = df[numeric_cols].corr()
sns.heatmap(correlacao, annot=True, cmap='coolwarm', center=0, 
           square=True, fmt='.2f', ax=ax7)
ax7.set_title('Correlação')

# 8. Final de semana vs dia útil
ax8 = plt.subplot(2, 4, 8)
df_semana = df.groupby('final_semana')['valor_total'].mean()
labels = ['Dia Útil', 'Final de Semana']
ax8.bar(labels, df_semana.values, color=['skyblue', 'orange'])
ax8.set_title('Venda Média: Dia vs FDS')
ax8.set_ylabel('Valor Médio')

plt.suptitle('Dashboard E-commerce - Análise Completa', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# 5. FEATURE ENGINEERING
print("\n5. FEATURE ENGINEERING")
print("-" * 50)

# Criar novas features
df['ticket_medio'] = df['valor_total'] / df['quantidade']
df['faixa_preco'] = pd.cut(df['preco_unitario'], 
                          bins=[0, 200, 800, 2000, float('inf')],
                          labels=['Baixo', 'Médio', 'Alto', 'Premium'])
df['faixa_valor_total'] = pd.cut(df['valor_total'],
                                bins=[0, 500, 2000, 5000, float('inf')],
                                labels=['Baixo', 'Médio', 'Alto', 'Premium'])

# Encoding de variáveis categóricas
le_produto = LabelEncoder()
le_categoria = LabelEncoder()
le_pagamento = LabelEncoder()
le_estado = LabelEncoder()

df['produto_encoded'] = le_produto.fit_transform(df['produto'])
df['categoria_encoded'] = le_categoria.fit_transform(df['categoria'])
df['pagamento_encoded'] = le_pagamento.fit_transform(df['metodo_pagamento'])
df['estado_encoded'] = le_estado.fit_transform(df['estado'])

print("Features criadas:")
print(f"• ticket_medio: média por item")
print(f"• faixa_preco: categorização de preço")
print(f"• faixa_valor_total: categorização de valor total")
print(f"• Encodings: produto, categoria, pagamento, estado")

print(f"\nNovas colunas: {[col for col in df.columns if col.endswith('_encoded') or 'faixa' in col or 'ticket' in col]}")

# 6. ANÁLISE ESTATÍSTICA AVANÇADA
print("\n6. ANÁLISE ESTATÍSTICA AVANÇADA")
print("-" * 50)

# Teste de hipótese: vendas no final de semana vs dia útil
from scipy import stats

vendas_fds = df[df['final_semana'] == True]['valor_total']
vendas_dia_util = df[df['final_semana'] == False]['valor_total']

# Teste t
t_stat, p_value = stats.ttest_ind(vendas_fds, vendas_dia_util)

print("Teste de Hipótese - Vendas FDS vs Dia Útil:")
print(f"Estatística t: {t_stat:.4f}")
print(f"Valor p: {p_value:.4f}")
print(f"Conclusão: {'Diferença significativa' if p_value < 0.05 else 'Sem diferença significativa'}")

# Análise de variância (ANOVA) por produto
grupos_produto = [df[df['produto'] == p]['valor_total'] for p in df['produto'].unique()]
f_stat, p_value_anova = stats.f_oneway(*grupos_produto)

print(f"\nANOVA - Preços por Produto:")
print(f"Estatística F: {f_stat:.4f}")
print(f"Valor p: {p_value_anova:.4f}")
print(f"Conclusão: {'Diferença significativa entre produtos' if p_value_anova < 0.05 else 'Sem diferença significativa'}")

# 7. SEGMENTAÇÃO DE CLIENTES
print("\n7. SEGMENTAÇÃO DE CLIENTES")
print("-" * 50)

# Análise RFV (Recência, Frequência, Valor)
data_ref = df['data_pedido'].max()

# Recência (dias desde última compra)
recencia = df.groupby('id_cliente')['data_pedido'].max().reset_index()
recencia['recencia'] = (data_ref - recencia['data_pedido']).dt.days

# Frequência (número de pedidos)
frequencia = df.groupby('id_cliente')['id_pedido'].count().reset_index()
frequencia.columns = ['id_cliente', 'frequencia']

# Valor (total gasto)
valor = df.groupby('id_cliente')['valor_total'].sum().reset_index()
valor.columns = ['id_cliente', 'valor_total']

# Combinar
rfv = recencia.merge(frequencia, on='id_cliente').merge(valor, on='id_cliente')
rfv = rfv.drop('data_pedido', axis=1)

# Scores RFV (1-5)
rfv['recencia_score'] = pd.qcut(rfv['recencia'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfv['frequencia_score'] = pd.qcut(rfv['frequencia'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfv['valor_score'] = pd.qcut(rfv['valor_total'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

# RFV Score
rfv['rfv_score'] = rfv['recencia_score'] + rfv['frequencia_score'] + rfv['valor_score']

# Segmentação
def segmentar_cliente(score):
    if score >= 13:
        return 'Campeão'
    elif score >= 10:
        return 'Leal'
    elif score >= 7:
        return 'Potencial'
    elif score >= 5:
        return 'Novo'
    else:
        return 'Em Risco'

rfv['segmento'] = rfv['rfv_score'].apply(segmentar_cliente)

print("Segmentação RFV:")
segmento_counts = rfv['segmento'].value_counts()
print(segmento_counts)

# Visualização segmentos
plt.figure(figsize=(10, 6))
segmento_counts.plot(kind='bar', color='purple', alpha=0.7)
plt.title('Distribuição de Segmentos de Clientes')
plt.xlabel('Segmento')
plt.ylabel('Número de Clientes')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 8. ANÁLISE DE SÉRIES TEMPORAIS
print("\n8. ANÁLISE DE SÉRIES TEMPORAIS")
print("-" * 50)

# Série temporal de vendas
vendas_ts = df.groupby('data_pedido')['valor_total'].sum().reset_index()
vendas_ts = vendas_ts.sort_values('data_pedido')

# Média móvel
vendas_ts['media_movel_7'] = vendas_ts['valor_total'].rolling(window=7).mean()
vendas_ts['media_movel_30'] = vendas_ts['valor_total'].rolling(window=30).mean()

# Visualização
plt.figure(figsize=(12, 6))
plt.plot(vendas_ts['data_pedido'], vendas_ts['valor_total'], alpha=0.5, label='Vendas Diárias')
plt.plot(vendas_ts['data_pedido'], vendas_ts['media_movel_7'], label='Média Móvel 7 dias')
plt.plot(vendas_ts['data_pedido'], vendas_ts['media_movel_30'], label='Média Móvel 30 dias')
plt.title('Análise de Séries Temporais - Vendas')
plt.xlabel('Data')
plt.ylabel('Valor Total')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Decomposição sazonal (simplificada)
from statsmodels.tsa.seasonal import seasonal_decompose

# Reamostrar para semanal para melhor visualização
vendas_semanal = vendas_ts.set_index('data_pedido')['valor_total'].resample('W').sum()

# Decomposição
decomposicao = seasonal_decompose(vendas_semanal, model='additive', period=4)

plt.figure(figsize=(12, 10))
plt.subplot(4, 1, 1)
plt.plot(decomposicao.observed)
plt.title('Série Original')
plt.subplot(4, 1, 2)
plt.plot(decomposicao.trend)
plt.title('Tendência')
plt.subplot(4, 1, 3)
plt.plot(decomposicao.seasonal)
plt.title('Sazonalidade')
plt.subplot(4, 1, 4)
plt.plot(decomposicao.resid)
plt.title('Resíduos')
plt.tight_layout()
plt.show()

# 9. INSIGHTS E RECOMENDAÇÕES
print("\n9. INSIGHTS E RECOMENDAÇÕES")
print("-" * 50)

# Calcular KPIs
total_vendas = df['valor_total'].sum()
total_pedidos = len(df)
ticket_medio = total_vendas / total_pedidos
clientes_unicos = df['id_cliente'].nunique()
ltv_medio = total_vendas / clientes_unicos

print("KPIs Principais:")
print(f"• Total de Vendas: R${total_vendas:,.2f}")
print(f"• Total de Pedidos: {total_pedidos:,}")
print(f"• Ticket Médio: R${ticket_medio:.2f}")
print(f"• Clientes Únicos: {clientes_unicos:,}")
print(f"• LTV Médio: R${ltv_medio:.2f}")

# Insights específicos
print(f"\nINSIGHTS ESTRATÉGICOS:")

# Produto mais lucrativo
produto_top = df.groupby('produto')['valor_total'].sum().idxmax()
print(f"1. PRODUTOS: {produto_top} é o mais lucrativo")

# Melhor método pagamento
pagamento_top = df.groupby('metodo_pagamento')['valor_total'].sum().idxmax()
print(f"2. PAGAMENTO: {pagamento_top} gera mais receita")

# Estado com maior volume
estado_top = df.groupby('estado')['valor_total'].sum().idxmax()
print(f"3. REGIÃO: {estado_top} tem maior volume")

# Segmento mais valioso
segmento_top = rfv.groupby('segmento')['valor_total'].mean().idxmax()
print(f"4. CLIENTES: Segmento '{segmento_top}' tem maior LTV")

print(f"\nRECOMENDAÇÕES AÇÃO:")
print(f"1. FOCO EM PRODUTOS: Aumentar estoque e marketing de {produto_top}")
print(f"2. OTIMIZAÇÃO DE PAGAMENTO: Oferecer incentivos para {pagamento_top}")
print(f"3. EXPANSÃO: Investir na região {estado_top}")
print(f"4. RETENÇÃO: Criar programa VIP para segmento {segmento_top}")
print(f"5. SAZONALIDADE: Planejar campanhas baseadas nos padrões identificados")

# 10. EXPORTAÇÃO E AUTOMAÇÃO
print("\n10. EXPORTAÇÃO E AUTOMAÇÃO")
print("-" * 50)

# Criar dashboard automático
def criar_dashboard(df):
    """Função para gerar dashboard automaticamente."""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Dashboard Automático E-commerce', fontsize=16, fontweight='bold')
    
    # 1. Vendas mensais
    vendas_mensais = df.groupby(df['data_pedido'].dt.to_period('M'))['valor_total'].sum()
    axes[0, 0].plot(vendas_mensais.index.astype(str), vendas_mensais.values, 'o-')
    axes[0, 0].set_title('Vendas Mensais')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Top produtos
    top_produtos = df.groupby('produto')['valor_total'].sum().sort_values()
    axes[0, 1].barh(top_produtos.index, top_produtos.values)
    axes[0, 1].set_title('Top Produtos')
    
    # 3. Métodos pagamento
    pagamento_counts = df['metodo_pagamento'].value_counts()
    axes[0, 2].pie(pagamento_counts.values, labels=pagamento_counts.index, autopct='%1.1f%%')
    axes[0, 2].set_title('Métodos Pagamento')
    
    # 4. Segmentos clientes
    segmento_counts = rfv['segmento'].value_counts()
    axes[1, 0].bar(segmento_counts.index, segmento_counts.values, color='purple', alpha=0.7)
    axes[1, 0].set_title('Segmentos Clientes')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 5. Distribuição valores
    axes[1, 1].hist(df['valor_total'], bins=30, alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('Distribuição Valores')
    
    # 6. Estados
    vendas_estado = df.groupby('estado')['valor_total'].sum().sort_values()
    axes[1, 2].barh(vendas_estado.index, vendas_estado.values, color='coral')
    axes[1, 2].set_title('Vendas por Estado')
    
    plt.tight_layout()
    return fig

# Gerar dashboard
dashboard_fig = criar_dashboard(df)
plt.show()

# Exportar resultados
relatorio_final = {
    'KPI': ['Total Vendas', 'Total Pedidos', 'Ticket Médio', 'Clientes Únicos', 'LTV Médio'],
    'Valor': [f"R${total_vendas:,.2f}", f"{total_pedidos:,}", f"R${ticket_medio:.2f}", 
              f"{clientes_unicos:,}", f"R${ltv_medio:.2f}"]
}

relatorio_df = pd.DataFrame(relatorio_final)
relatorio_df.to_csv('kpis_ecommerce.csv', index=False)

# Exportar segmentação
rfv.to_csv('segmentacao_clientes.csv', index=False)

# Exportar análise de produtos
analise_produto.to_csv('analise_produtos.csv')

print("Arquivos exportados:")
print("• kpis_ecommerce.csv")
print("• segmentacao_clientes.csv") 
print("• analise_produtos.csv")

print("\n" + "=" * 70)
print("DATA SCIENCE ESSENCIAL 80/20 CONCLUÍDO!")
print("Você domina as técnicas essenciais para 80% dos problemas!")
print("=" * 70)
