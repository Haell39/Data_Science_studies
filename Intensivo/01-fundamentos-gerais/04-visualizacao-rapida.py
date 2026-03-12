"""
VISUALIZAÇÃO RÁPIDA - FUNDAMENTOS GERAIS
Os 20% mais importantes para 80% do uso em Data Science
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configuração para melhor visualização
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

print("=" * 60)
print("VISUALIZAÇÃO RÁPIDA - FUNDAMENTOS")
print("=" * 60)

# 1. GRÁFICOS BÁSICOS
print("\n1. GRÁFICOS BÁSICOS")
print("-" * 30)

# Gráfico de linhas
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 4))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'r--', linewidth=2, label='cos(x)')
plt.title('Funções Trigonométricas')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico de dispersão
np.random.seed(42)
x = np.random.normal(0, 1, 100)
y = 2 * x + np.random.normal(0, 0.5, 100)

plt.figure(figsize=(10, 4))
plt.scatter(x, y, alpha=0.6, c='blue')
plt.title('Gráfico de Dispersão')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 2. GRÁFICOS DE BARRAS
print("\n2. GRÁFICOS DE BARRAS")
print("-" * 30)

categorias = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
vendas = [120, 85, 95, 110, 75]

plt.figure(figsize=(10, 4))
plt.bar(categorias, vendas, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.title('Vendas por Produto')
plt.xlabel('Produtos')
plt.ylabel('Vendas')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# Gráfico de barras horizontal
plt.figure(figsize=(10, 4))
plt.barh(categorias, vendas, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.title('Vendas por Produto (Horizontal)')
plt.xlabel('Vendas')
plt.ylabel('Produtos')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

# 3. HISTOGRAMAS
print("\n3. HISTOGRAMAS")
print("-" * 30)

# Dados normais
np.random.seed(42)
dados = np.random.normal(100, 15, 1000)

plt.figure(figsize=(10, 4))
plt.hist(dados, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribuição Normal')
plt.xlabel('Valores')
plt.ylabel('Frequência')
plt.grid(True, alpha=0.3, axis='y')
plt.axvline(dados.mean(), color='red', linestyle='--', label=f'Média: {dados.mean():.1f}')
plt.legend()
plt.tight_layout()
plt.show()

# Múltiplos histogramas
np.random.seed(42)
grupo1 = np.random.normal(100, 10, 500)
grupo2 = np.random.normal(110, 15, 500)

plt.figure(figsize=(10, 4))
plt.hist(grupo1, bins=25, alpha=0.6, label='Grupo 1', color='blue')
plt.hist(grupo2, bins=25, alpha=0.6, label='Grupo 2', color='red')
plt.title('Comparação de Distribuições')
plt.xlabel('Valores')
plt.ylabel('Frequência')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 4. BOXPLOTS
print("\n4. BOXPLOTS")
print("-" * 30)

# Gerar dados para boxplot
np.random.seed(42)
data_box = [np.random.normal(0, std, 100) for std in range(1, 4)]

plt.figure(figsize=(10, 4))
plt.boxplot(data_box, labels=['Grupo 1', 'Grupo 2', 'Grupo 3'])
plt.title('Boxplots de Diferentes Grupos')
plt.ylabel('Valores')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 5. GRÁFICOS COM PANDAS
print("\n5. GRÁFICOS COM PANDAS")
print("-" * 30)

# Criar DataFrame
df = pd.DataFrame({
    'mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    'vendas': [120, 135, 125, 145, 160, 155],
    'custos': [80, 85, 82, 90, 95, 92],
    'lucro': [40, 50, 43, 55, 65, 63]
})

# Gráfico de linhas com pandas
plt.figure(figsize=(10, 4))
df.plot(x='mes', y=['vendas', 'custos', 'lucro'], kind='line', marker='o')
plt.title('Evolução Mensal')
plt.xlabel('Mês')
plt.ylabel('Valores')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Gráfico de barras com pandas
plt.figure(figsize=(10, 4))
df.plot(x='mes', y='lucro', kind='bar', color='green', alpha=0.7)
plt.title('Lucro Mensal')
plt.xlabel('Mês')
plt.ylabel('Lucro')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 6. SUBPLOTS
print("\n6. SUBPLOTS")
print("-" * 30)

# Múltiplos gráficos em uma figura
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

# Gráfico 1: Linha
x = np.linspace(0, 10, 50)
ax1.plot(x, np.sin(x), 'b-')
ax1.set_title('Função Seno')
ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')
ax1.grid(True, alpha=0.3)

# Gráfico 2: Dispersão
np.random.seed(42)
x = np.random.randn(50)
y = np.random.randn(50)
ax2.scatter(x, y, alpha=0.6)
ax2.set_title('Dispersão')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.grid(True, alpha=0.3)

# Gráfico 3: Histograma
dados = np.random.normal(0, 1, 100)
ax3.hist(dados, bins=20, alpha=0.7, color='orange')
ax3.set_title('Histograma')
ax3.set_xlabel('Valores')
ax3.set_ylabel('Frequência')
ax3.grid(True, alpha=0.3, axis='y')

# Gráfico 4: Barras
categorias = ['A', 'B', 'C', 'D']
valores = [15, 30, 25, 20]
ax4.bar(categorias, valores, color=['red', 'green', 'blue', 'purple'])
ax4.set_title('Barras')
ax4.set_xlabel('Categorias')
ax4.set_ylabel('Valores')
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 7. CUSTOMIZAÇÃO AVANÇADA
print("\n7. CUSTOMIZAÇÃO AVANÇADA")
print("-" * 30)

# Gráfico customizado
x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(12, 6))

# Configuração de estilo
plt.style.use('seaborn-v0_8-whitegrid')

# Gráfico principal
plt.plot(x, y1, 'b-', linewidth=3, label='sin(x)', marker='o', markersize=4, markevery=10)
plt.plot(x, y2, 'r--', linewidth=3, label='cos(x)', marker='s', markersize=4, markevery=10)

# Customizações
plt.title('Funções Trigonométricas Customizadas', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('x (radianos)', fontsize=12, labelpad=10)
plt.ylabel('y', fontsize=12, labelpad=10)
plt.legend(fontsize=12, loc='upper right', framealpha=0.9)
plt.grid(True, alpha=0.3, linestyle=':', color='gray')

# Limites dos eixos
plt.xlim(0, 2*np.pi)
plt.ylim(-1.5, 1.5)

# Texto adicional
plt.text(np.pi, 0, 'π', fontsize=14, ha='center', va='center', 
         bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))

plt.tight_layout()
plt.show()

# 8. GRÁFICOS ESPECIALIZADOS
print("\n8. GRÁFICOS ESPECIALIZADOS")
print("-" * 30)

# Gráfico de pizza
sizes = [30, 25, 20, 15, 10]
labels = ['Categoria A', 'Categoria B', 'Categoria C', 'Categoria D', 'Categoria E']
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.05, 0, 0, 0, 0))
plt.title('Distribuição Percentual', fontsize=14, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# Gráfico de área (stack plot)
x = np.arange(0, 10, 1)
y1 = np.random.randint(1, 5, 10)
y2 = np.random.randint(1, 5, 10)
y3 = np.random.randint(1, 5, 10)

plt.figure(figsize=(10, 4))
plt.stackplot(x, y1, y2, y3, labels=['Série 1', 'Série 2', 'Série 3'], 
              colors=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.8)
plt.title('Gráfico de Área Empilhado')
plt.xlabel('x')
plt.ylabel('Valores')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 9. SALVAR GRÁFICOS
print("\n9. SALVAR GRÁFICOS")
print("-" * 30)

# Criar gráfico para salvar
plt.figure(figsize=(10, 6))
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'r--', linewidth=2, label='cos(x)')
plt.title('Funções Trigonométricas')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)

# Salvar em diferentes formatos
plt.savefig('grafico_trigonometrico.png', dpi=300, bbox_inches='tight')
plt.savefig('grafico_trigonometrico.pdf', bbox_inches='tight')
plt.savefig('grafico_trigonometrico.svg', bbox_inches='tight')

plt.show()

print("Gráficos salvos como:")
print("- grafico_trigonometrico.png")
print("- grafico_trigonometrico.pdf")
print("- grafico_trigonometrico.svg")

# 10. APLICAÇÃO PRÁTICA - DASHBOARD
print("\n10. APLICAÇÃO PRÁTICA - MINI DASHBOARD")
print("-" * 30)

# Gerar dados simulados
np.random.seed(42)
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
vendas = np.random.randint(80, 150, 6)
custos = vendas * np.random.uniform(0.6, 0.8, 6)
lucro = vendas - custos

# Criar dashboard
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Dashboard de Vendas - 1º Semestre', fontsize=16, fontweight='bold')

# Gráfico 1: Evolução das vendas
ax1.plot(meses, vendas, 'b-o', linewidth=2, markersize=8, label='Vendas')
ax1.plot(meses, custos, 'r--s', linewidth=2, markersize=8, label='Custos')
ax1.plot(meses, lucro, 'g-^', linewidth=2, markersize=8, label='Lucro')
ax1.set_title('Evolução Mensal')
ax1.set_ylabel('Valores (R$)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Gráfico 2: Participação do lucro
ax2.pie(lucro, labels=meses, autopct='%1.1f%%', startangle=90)
ax2.set_title('Participação do Lucro por Mês')

# Gráfico 3: Margem de lucro
margem = (lucro / vendas) * 100
ax3.bar(meses, margem, color='green', alpha=0.7)
ax3.set_title('Margem de Lucro (%)')
ax3.set_ylabel('Percentual')
ax3.grid(True, alpha=0.3, axis='y')

# Gráfico 4: Comparação vendas vs custos
ax4.scatter(vendas, custos, s=100, alpha=0.7, c=range(6), cmap='viridis')
for i, mes in enumerate(meses):
    ax4.annotate(mes, (vendas[i], custos[i]), xytext=(5, 5), textcoords='offset points')
ax4.set_title('Vendas vs Custos')
ax4.set_xlabel('Vendas')
ax4.set_ylabel('Custos')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 11. DESAFIO INTEGRADOR
print("\n11. DESAFIO INTEGRADOR")
print("-" * 30)

def criar_visualizacoes_completas():
    """Criar visualizações completas para um dataset."""
    
    # Gerar dados
    np.random.seed(123)
    n_pontos = 200
    
    dados = {
        'idade': np.random.normal(35, 10, n_pontos),
        'salario': np.random.normal(6000, 2000, n_pontos),
        'experiencia': np.random.exponential(5, n_pontos),
        'satisfacao': np.random.uniform(1, 5, n_pontos)
    }
    
    # Ajustar dados
    dados['idade'] = np.maximum(dados['idade'], 22)
    dados['salario'] = np.maximum(dados['salario'], 2000)
    dados['experiencia'] = np.maximum(dados['experiencia'], 0.5)
    
    df = pd.DataFrame(dados)
    
    # Criar visualizações
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Distribuição de idade
    ax1 = plt.subplot(2, 3, 1)
    ax1.hist(df['idade'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_title('Distribuição de Idade')
    ax1.set_xlabel('Idade')
    ax1.set_ylabel('Frequência')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Salário vs Experiência
    ax2 = plt.subplot(2, 3, 2)
    scatter = ax2.scatter(df['experiencia'], df['salario'], 
                         c=df['idade'], alpha=0.6, cmap='viridis')
    ax2.set_title('Salário vs Experiência')
    ax2.set_xlabel('Experiência (anos)')
    ax2.set_ylabel('Salário (R$)')
    plt.colorbar(scatter, ax=ax2, label='Idade')
    ax2.grid(True, alpha=0.3)
    
    # 3. Boxplot de satisfação
    ax3 = plt.subplot(2, 3, 3)
    ax3.boxplot(df['satisfacao'])
    ax3.set_title('Distribuição de Satisfação')
    ax3.set_ylabel('Satisfação (1-5)')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Correlação
    ax4 = plt.subplot(2, 3, 4)
    corr_matrix = df.corr()
    im = ax4.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax4.set_xticks(range(len(df.columns)))
    ax4.set_yticks(range(len(df.columns)))
    ax4.set_xticklabels(df.columns, rotation=45)
    ax4.set_yticklabels(df.columns)
    ax4.set_title('Matriz de Correlação')
    
    # Adicionar valores de correlação
    for i in range(len(df.columns)):
        for j in range(len(df.columns)):
            text = ax4.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=10)
    
    # 5. Faixas salariais
    ax5 = plt.subplot(2, 3, 5)
    faixas = pd.cut(df['salario'], bins=4, labels=['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto'])
    faixas.value_counts().plot(kind='bar', ax=ax5, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax5.set_title('Distribuição Salarial')
    ax5.set_xlabel('Faixa Salarial')
    ax5.set_ylabel('Contagem')
    ax5.tick_params(axis='x', rotation=45)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 6. Satisfação por faixa de idade
    ax6 = plt.subplot(2, 3, 6)
    df['faixa_idade'] = pd.cut(df['idade'], bins=3, labels=['Jovem', 'Adulto', 'Sênior'])
    df.boxplot(column='satisfacao', by='faixa_idade', ax=ax6)
    ax6.set_title('Satisfação por Faixa de Idade')
    ax6.set_xlabel('Faixa de Idade')
    ax6.set_ylabel('Satisfação')
    
    plt.suptitle('Análise Visual Completa do Dataset', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    # Estatísticas
    print("ESTATÍSTICAS DO DATASET:")
    print("=" * 40)
    print(df.describe().round(2))
    
    return df

# Executar desafio
dataset_visual = criar_visualizacoes_completas()

print("\n" + "=" * 60)
print("VISUALIZAÇÃO RÁPIDA CONCLUÍDA!")
print("Você domina os 20% mais importantes!")
print("=" * 60)
