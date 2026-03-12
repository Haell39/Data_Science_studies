"""
PROJETO MINI - ANÁLISE DE DADOS COMPLETA
Aplicação prática dos conceitos fundamentais
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

print("=" * 70)
print("PROJETO MINI - ANÁLISE DE DADOS COMPLETA")
print("=" * 70)

# 1. GERAÇÃO DE DADOS SIMULADOS
print("\n1. GERAÇÃO DE DADOS")
print("-" * 40)

# Configurar semente para reprodutibilidade
np.random.seed(42)

# Gerar dataset de vendas
n_vendas = 1000
data_inicio = datetime(2023, 1, 1)
datas = [data_inicio + timedelta(days=i) for i in range(n_vendas)]

dados_vendas = {
    'data': datas,
    'produto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Headphone'], n_vendas),
    'categoria': np.random.choice(['Eletrônicos', 'Acessórios'], n_vendas),
    'quantidade': np.random.randint(1, 10, n_vendas),
    'valor_unitario': np.random.choice([5000, 150, 200, 1200, 300], n_vendas),
    'vendedor': np.random.choice(['Ana', 'Bruno', 'Carla', 'Daniel'], n_vendas),
    'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], n_vendas),
    'cliente_tipo': np.random.choice(['PF', 'PJ'], n_vendas, p=[0.7, 0.3])
}

# Criar DataFrame
df = pd.DataFrame(dados_vendas)

# Calcular valor total
df['valor_total'] = df['quantidade'] * df['valor_unitario']

# Adicionar informações adicionais
df['dia_semana'] = df['data'].dt.day_name()
df['mes'] = df['data'].dt.month
df['trimestre'] = df['data'].dt.quarter
df['ano'] = df['data'].dt.year

# Ajustar categoria baseada no produto
df.loc[df['produto'].isin(['Laptop', 'Monitor']), 'categoria'] = 'Eletrônicos'
df.loc[df['produto'].isin(['Mouse', 'Teclado', 'Headphone']), 'categoria'] = 'Acessórios'

print(f"Dataset criado: {df.shape}")
print(f"Período: {df['data'].min().strftime('%d/%m/%Y')} a {df['data'].max().strftime('%d/%m/%Y')}")
print(f"\nPrimeiras linhas:")
print(df.head())

# 2. ANÁLISE EXPLORATÓRIA
print("\n2. ANÁLISE EXPLORATÓRIA")
print("-" * 40)

# Estatísticas básicas
print("Estatísticas descritivas:")
print(df[['quantidade', 'valor_unitario', 'valor_total']].describe().round(2))

# Análise por produto
print(f"\nAnálise por produto:")
analise_produto = df.groupby('produto').agg({
    'quantidade': ['sum', 'mean'],
    'valor_total': ['sum', 'mean', 'count']
}).round(2)
print(analise_produto)

# Análise por vendedor
print(f"\nAnálise por vendedor:")
vendas_vendedor = df.groupby('vendedor')['valor_total'].agg(['sum', 'count', 'mean']).round(2)
vendas_vendedor.columns = ['Total', 'Quantidade', 'Média']
vendas_vendedor = vendas_vendedor.sort_values('Total', ascending=False)
print(vendas_vendedor)

# Análise por região
print(f"\nAnálise por região:")
vendas_regiao = df.groupby('regiao')['valor_total'].sum().sort_values(ascending=False)
print(vendas_regiao)

# 3. VISUALIZAÇÕES
print("\n3. VISUALIZAÇÕES")
print("-" * 40)

# Configurar estilo
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)

# Dashboard completo
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Dashboard de Análise de Vendas', fontsize=16, fontweight='bold')

# 1. Vendas por produto
vendas_produto = df.groupby('produto')['valor_total'].sum().sort_values()
ax1.barh(vendas_produto.index, vendas_produto.values, color='skyblue')
ax1.set_title('Vendas Totais por Produto')
ax1.set_xlabel('Valor Total (R$)')
ax1.grid(True, alpha=0.3, axis='x')

# 2. Vendas mensais
vendas_mensais = df.groupby(df['data'].dt.to_period('M'))['valor_total'].sum()
ax2.plot(vendas_mensais.index.astype(str), vendas_mensais.values, 'o-', linewidth=2, markersize=6)
ax2.set_title('Evolução Mensal de Vendas')
ax2.set_xlabel('Mês')
ax2.set_ylabel('Valor Total (R$)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)

# 3. Distribuição por região
vendas_regiao = df.groupby('regiao')['valor_total'].sum()
ax3.pie(vendas_regiao.values, labels=vendas_regiao.index, autopct='%1.1f%%', startangle=90)
ax3.set_title('Distribuição de Vendas por Região')

# 4. Performance dos vendedores
vendas_vendedor = df.groupby('vendedor')['valor_total'].sum().sort_values()
ax4.barh(vendas_vendedor.index, vendas_vendedor.values, color='lightgreen')
ax4.set_title('Performance dos Vendedores')
ax4.set_xlabel('Valor Total (R$)')
ax4.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.show()

# 4. ANÁLISE TEMPORAL
print("\n4. ANÁLISE TEMPORAL")
print("-" * 40)

# Vendas por dia da semana
vendas_dia_semana = df.groupby('dia_semana')['valor_total'].sum()
ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
vendas_dia_semana = vendas_dia_semana.reindex(ordem_dias)

plt.figure(figsize=(10, 4))
plt.bar(vendas_dia_semana.index, vendas_dia_semana.values, color='orange', alpha=0.7)
plt.title('Vendas por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# Tendência mensal
plt.figure(figsize=(12, 4))
vendas_mensais = df.groupby(df['data'].dt.to_period('M'))['valor_total'].sum()
plt.plot(vendas_mensais.index.astype(str), vendas_mensais.values, 'o-', linewidth=2, markersize=8)
plt.title('Tendência de Vendas Mensais')
plt.xlabel('Mês')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 5. ANÁLISE DE CORRELAÇÃO
print("\n5. ANÁLISE DE CORRELAÇÃO")
print("-" * 40)

# Criar matriz de correlação
dados_numericos = df[['quantidade', 'valor_unitario', 'valor_total', 'mes', 'trimestre']]
correlacao = dados_numericos.corr()

print("Matriz de Correlação:")
print(correlacao.round(3))

# Visualizar correlação
plt.figure(figsize=(8, 6))
plt.imshow(correlacao, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
plt.colorbar(label='Correlação')
plt.xticks(range(len(correlacao.columns)), correlacao.columns, rotation=45)
plt.yticks(range(len(correlacao.columns)), correlacao.columns)
plt.title('Matriz de Correlação')

# Adicionar valores
for i in range(len(correlacao.columns)):
    for j in range(len(correlacao.columns)):
        plt.text(j, i, f'{correlacao.iloc[i, j]:.2f}', 
                ha='center', va='center', color='black', fontsize=10)

plt.tight_layout()
plt.show()

# 6. SEGMENTAÇÃO DE CLIENTES
print("\n6. SEGMENTAÇÃO DE CLIENTES")
print("-" * 40)

# Análise por tipo de cliente
segmento_cliente = df.groupby('cliente_tipo').agg({
    'valor_total': ['sum', 'mean', 'count'],
    'quantidade': 'sum'
}).round(2)
segmento_cliente.columns = ['Total', 'Média', 'Transações', 'Quantidade']
print(segmento_cliente)

# Visualização
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Total por tipo
totais_tipo = df.groupby('cliente_tipo')['valor_total'].sum()
ax1.bar(totais_tipo.index, totais_tipo.values, color=['blue', 'red'], alpha=0.7)
ax1.set_title('Valor Total por Tipo de Cliente')
ax1.set_ylabel('Valor Total (R$)')
ax1.grid(True, alpha=0.3, axis='y')

# Ticket médio
ticket_medio = df.groupby('cliente_tipo')['valor_total'].mean()
ax2.bar(ticket_medio.index, ticket_medio.values, color=['blue', 'red'], alpha=0.7)
ax2.set_title('Ticket Médio por Tipo de Cliente')
ax2.set_ylabel('Ticket Médio (R$)')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 7. PRODUTOS MAIS VENDIDOS
print("\n7. ANÁLISE DE PRODUTOS")
print("-" * 40)

# Top produtos
top_produtos = df.groupby('produto').agg({
    'valor_total': 'sum',
    'quantidade': 'sum'
}).sort_values('valor_total', ascending=False)

print("Top Produtos (por valor total):")
print(top_produtos)

# Análise de cruzamento
cruzamento_produto_regiao = pd.crosstab(df['produto'], df['regiao'], 
                                       values=df['valor_total'], aggfunc='sum')
print(f"\nCruzamento Produto x Região:")
print(cruzamento_produto_regiao.round(2))

# Visualização
plt.figure(figsize=(10, 6))
cruzamento_produto_regiao.plot(kind='bar', stacked=True)
plt.title('Vendas por Produto e Região')
plt.xlabel('Produto')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45)
plt.legend(title='Região')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 8. INSIGHTS E RECOMENDAÇÕES
print("\n8. INSIGHTS E RECOMENDAÇÕES")
print("-" * 40)

# Calcular métricas importantes
total_vendas = df['valor_total'].sum()
ticket_medio_geral = df['valor_total'].mean()
produto_mais_vendido = df.groupby('produto')['valor_total'].sum().idxmax()
melhor_vendedor = df.groupby('vendedor')['valor_total'].sum().idxmax()
melhor_regiao = df.groupby('regiao')['valor_total'].sum().idxmax()
dia_mais_vendas = df.groupby('dia_semana')['valor_total'].sum().idxmax()

print("INSIGHTS PRINCIPAIS:")
print(f"• Total de vendas: R${total_vendas:,.2f}")
print(f"• Ticket médio: R${ticket_medio_geral:.2f}")
print(f"• Produto mais vendido: {produto_mais_vendido}")
print(f"• Melhor vendedor: {melhor_vendedor}")
print(f"• Melhor região: {melhor_regiao}")
print(f"• Dia com mais vendas: {dia_mais_vendas}")

print(f"\nRECOMENDAÇÕES:")
print(f"1. FOCO EM PRODUTOS:")
print(f"   • Priorizar {produto_mais_vendido} em campanhas")
print(f"   • Criar pacotes com produtos complementares")

print(f"\n2. ESTRATÉGIA DE VENDAS:")
print(f"   • Destacar {melhor_vendedor} como mentor")
print(f"   • Expandir operações na região {melhor_regiao}")
print(f"   • Aumentar esforços nas {dia_mais_vendas}")

print(f"\n3. OTIMIZAÇÃO:")
print(f"   • Monitorar ticket médio (atual: R${ticket_medio_geral:.2f})")
print(f"   • Implementar programa de fidelidade para clientes PJ")
print(f"   • Analisar sazonalidade para planejamento de estoque")

# 9. RELATÓRIO FINAL
print("\n9. RELATÓRIO FINAL")
print("-" * 40)

# Criar resumo executivo
resumo = {
    'Período': f"{df['data'].min().strftime('%d/%m/%Y')} a {df['data'].max().strftime('%d/%m/%Y')}",
    'Total de Vendas': f"R${total_vendas:,.2f}",
    'Total de Transações': f"{len(df):,}",
    'Ticket Médio': f"R${ticket_medio_geral:.2f}",
    'Produto Top': produto_mais_vendido,
    'Vendedor Top': melhor_vendedor,
    'Região Top': melhor_regiao,
    'Dias de Operação': df['data'].nunique()
}

print("RESUMO EXECUTIVO:")
for chave, valor in resumo.items():
    print(f"• {chave}: {valor}")

# 10. EXPORTAÇÃO DE RESULTADOS
print("\n10. EXPORTAÇÃO DE RESULTADOS")
print("-" * 40)

# Criar DataFrame com insights
insights_df = pd.DataFrame(list(resumo.items()), columns=['Métrica', 'Valor'])
insights_df.to_csv('insights_vendas.csv', index=False)
print("Insights exportados para 'insights_vendas.csv'")

# Exportar dados analisados
df.to_csv('dados_vendas_completos.csv', index=False)
print("Dados completos exportados para 'dados_vendas_completos.csv'")

# Exportar análise por produto
top_produtos.to_csv('analise_produtos.csv')
print("Análise de produtos exportada para 'analise_produtos.csv'")

print("\n" + "=" * 70)
print("PROJETO DE ANÁLISE DE DADOS CONCLUÍDO!")
print("Todos os conceitos fundamentais foram aplicados com sucesso!")
print("=" * 70)
