"""
PROJETOS REAIS - 80/20
Aplicações práticas que resolvem problemas do mundo real
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("PROJETOS REAIS - 80/20")
print("=" * 70)

# 1. PROJETO 1: ANÁLISE DE SENTIMENTOS
print("\n1. PROJETO 1: ANÁLISE DE SENTIMENTOS")
print("-" * 50)

# Gerar dados de reviews
np.random.seed(42)
n_reviews = 1000

# Templates de reviews positivos e negativos
positivos = [
    "Excelente produto! Super recomendo.",
    "Adorei! Qualidade incrível.",
    "Fantástico! Atendeu todas as expectativas.",
    "Perfeito! Com certeza compraria novamente.",
    "Maravilhoso! Vale cada centavo.",
    "Ótimo! Muito satisfeito com a compra.",
    "Sensacional! Superou minhas expectativas.",
    "Incrível! Produto de alta qualidade."
]

negativos = [
    "Péssimo! Não recomendo a ninguém.",
    "Horrível! Perdi meu dinheiro.",
    "Terrível! Produto de baixa qualidade.",
    "Decepcionante! Não funcionou como esperado.",
    "Ruim! Não vale o preço.",
    "Fraco! Material de péssima qualidade.",
    "Insatisfatório! Problemas desde o início.",
    "Desapontador! Esperava muito mais."
]

neutros = [
    "Produto ok, nada especial.",
    "Funciona como esperado.",
    "Preço justo para o que oferece.",
    "Normal, sem surpresas.",
    "Razoável, poderia ser melhor.",
    "Aceitável dentro do esperado."
]

# Gerar reviews
reviews = []
sentimentos = []

for i in range(n_samples):
    if i < n_samples * 0.4:  # 40% positivos
        reviews.append(np.random.choice(positivos))
        sentimentos.append('positivo')
    elif i < n_samples * 0.8:  # 40% negativos
        reviews.append(np.random.choice(negativos))
        sentimentos.append('negativo')
    else:  # 20% neutros
        reviews.append(np.random.choice(neutros))
        sentimentos.append('neutro')

# Adicionar um pouco de ruído
for i in range(len(reviews)):
    if np.random.random() < 0.1:
        reviews[i] += " " + np.random.choice(["muito bom", "bom", "razoável", "pode melhorar"])

df_sentimento = pd.DataFrame({
    'review': reviews,
    'sentimento': sentimentos,
    'nota': [np.random.choice([5, 4, 3, 2, 1], p=[0.4, 0.3, 0.2, 0.08, 0.02]) if s == 'positivo' 
             else np.random.choice([5, 4, 3, 2, 1], p=[0.02, 0.08, 0.2, 0.3, 0.4]) if s == 'negativo'
             else np.random.choice([5, 4, 3, 2, 1], p=[0.1, 0.3, 0.4, 0.15, 0.05]) 
             for s in sentimentos]
})

print(f"Dataset de reviews: {df_sentimento.shape}")
print(f"\nDistribuição de sentimentos:")
print(df_sentimento['sentimento'].value_counts())

# Análise de texto
print(f"\nEstatísticas dos reviews:")
df_sentimento['comprimento'] = df_sentimento['review'].str.len()
print(df_sentimento.groupby('sentimento')['comprimento'].describe().round(1))

# Visualização
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
df_sentimento['sentimento'].value_counts().plot(kind='bar', color=['green', 'red', 'gray'])
plt.title('Distribuição de Sentimentos')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.boxplot(data=df_sentimento, x='sentimento', y='nota')
plt.title('Nota por Sentimento')
plt.tight_layout()
plt.show()

# Processamento de texto
vectorizer = TfidfVectorizer(max_features=1000, stop_words=['o', 'a', 'os', 'as', 'de', 'do', 'da', 'em', 'para', 'com', 'um', 'uma'])
X_text = vectorizer.fit_transform(df_sentimento['review'])

# Encoder para sentimentos
le_sentimento = LabelEncoder()
y_sentimento = le_sentimento.fit_transform(df_sentimento['sentimento'])

# Divisão treino/teste
X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(
    X_text, y_sentimento, test_size=0.2, random_state=42, stratify=y_sentimento
)

# Modelo de classificação
modelo_sentimento = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_sentimento.fit(X_train_text, y_train_text)

# Avaliação
y_pred_sentimento = modelo_sentimento.predict(X_test_text)
print(f"\nAcurácia: {modelo_sentimento.score(X_test_text, y_test_text):.4f}")
print(f"\nRelatório de Classificação:")
print(classification_report(y_test_text, y_pred_sentimento, 
                           target_names=le_sentimento.classes_))

# Função para analisar novo review
def analisar_sentimento(review):
    review_vector = vectorizer.transform([review])
    pred = modelo_sentimento.predict(review_vector)[0]
    prob = modelo_sentimento.predict_proba(review_vector)[0]
    sentimento = le_sentimento.inverse_transform([pred])[0]
    return sentimento, prob.max()

# Teste
test_reviews = [
    "Este produto é incrível! Adorei comprar!",
    "Péssima experiência, não funcionou!",
    "Produto razoável, poderia ser melhor."
]

print(f"\nTeste de novos reviews:")
for review in test_reviews:
    sentimento, confianca = analisar_sentimento(review)
    print(f"Review: '{review}' -> Sentimento: {sentimento} (confiança: {confianca:.2%})")

# 2. PROJETO 2: SISTEMA DE RECOMENDAÇÃO
print("\n\n2. PROJETO 2: SISTEMA DE RECOMENDAÇÃO")
print("-" * 50)

# Gerar dados de filmes e avaliações
np.random.seed(42)
n_usuarios = 100
n_filmes = 50

# Filmes
filmes = [
    "Vingadores: Ultimato", "Avatar", "Titanic", "Star Wars: O Despertar da Força",
    "Vingadores: Guerra Infinita", "Jurassic World", "Fúria de Titãs", "Velozes e Furiosos 7",
    "Os Vingadores", "Harry Potter e as Relíquias da Morte", "Frozen: Uma Aventura Congelante",
    "Homem-Aranha: Sem Volta para Casa", "Coração de Cavaleiro", "Minions", "Guerra Civil"
] * 3 + ["Matrix", "O Senhor dos Anéis", "Clube da Luta", "Forrest Gump", "Gladiador"]

# Avaliações dos usuários
avaliacoes = []
for usuario in range(1, n_usuarios + 1):
    n_avaliacoes = np.random.randint(5, 20)  # Cada usuário avalia 5-20 filmes
    
    for _ in range(n_avaliacoes):
        filme = np.random.choice(filmes)
        nota = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.1, 0.2, 0.3, 0.3])
        
        # Usuários têm preferências (simulação)
        if usuario % 3 == 0 and "Vingadores" in filme:
            nota = min(5, nota + 1)
        elif usuario % 3 == 1 and "Harry Potter" in filme:
            nota = min(5, nota + 1)
        elif usuario % 3 == 2 and "Star Wars" in filme:
            nota = min(5, nota + 1)
            
        avaliacoes.append([usuario, filme, nota])

df_recomendacao = pd.DataFrame(avaliacoes, columns=['usuario', 'filme', 'nota'])
df_recomendacao = df_recomendacao.drop_duplicates()

print(f"Dataset de recomendação: {df_recomendacao.shape}")
print(f"\nEstatísticas:")
print(f"Usuários únicos: {df_recomendacao['usuario'].nunique()}")
print(f"Filmes únicos: {df_recomendacao['filme'].nunique()}")
print(f"Avaliações totais: {len(df_recomendacao)}")

# Análise dos dados
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
df_recomendacao['nota'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribuição de Notas')
plt.xlabel('Nota')
plt.ylabel('Frequência')

plt.subplot(1, 2, 2)
filmes_populares = df_recomendacao['filme'].value_counts().head(10)
filmes_populares.plot(kind='barh')
plt.title('Top 10 Filmes Mais Avaliados')
plt.tight_layout()
plt.show()

# Sistema de recomendação baseado em conteúdo
# Criar matriz usuário-filme
matriz_usuario_filme = df_recomendacao.pivot_table(
    index='usuario', 
    columns='filme', 
    values='nota'
).fillna(0)

print(f"\nMatriz usuário-filme: {matriz_usuario_filme.shape}")

# Calcular similaridade entre usuários
similaridade_usuarios = cosine_similarity(matriz_usuario_filme)
similaridade_usuarios_df = pd.DataFrame(
    similaridade_usuarios, 
    index=matriz_usuario_filme.index, 
    columns=matriz_usuario_filme.index
)

# Sistema de recomendação
def recomendar_filmes(usuario_id, n_recomendacoes=5):
    """Recomenda filmes para um usuário baseado em usuários similares"""
    
    if usuario_id not in matriz_usuario_filme.index:
        return "Usuário não encontrado"
    
    # Encontrar usuários similares
    usuarios_similares = similaridade_usuarios_df[usuario_id].sort_values(ascending=False)[1:11]
    
    # Filmes que o usuário ainda não avaliou
    filmes_nao_avaliados = matriz_usuario_filme.columns[
        matriz_usuario_filme.loc[usuario_id] == 0
    ]
    
    # Calcular previsão de notas para filmes não avaliados
    recomendacoes = {}
    
    for filme in filmes_nao_avaliados:
        nota_prevista = 0
        peso_total = 0
        
        for outro_usuario, similaridade in usuarios_similares.items():
            if matriz_usuario_filme.loc[outro_usuario, filme] > 0:
                nota_prevista += similaridade * matriz_usuario_filme.loc[outro_usuario, filme]
                peso_total += similaridade
        
        if peso_total > 0:
            recomendacoes[filme] = nota_prevista / peso_total
    
    # Retornar top N recomendações
    recomendacoes_ordenadas = sorted(recomendacoes.items(), key=lambda x: x[1], reverse=True)
    
    return recomendacoes_ordenadas[:n_recomendacoes]

# Testar sistema
print(f"\nTeste do Sistema de Recomendação:")
for usuario in [1, 25, 50]:
    print(f"\nRecomendações para Usuário {usuario}:")
    
    # Mostrar filmes que o usuário gostou (nota >= 4)
    filmes_gostados = df_recomendacao[
        (df_recomendacao['usuario'] == usuario) & 
        (df_recomendacao['nota'] >= 4)
    ]['filme'].tolist()
    
    if filmes_gostados:
        print(f"  Filmes que gostou: {', '.join(filmes_gostados[:3])}")
    
    # Recomendações
    recomendacoes = recomendar_filmes(usuario, 3)
    if isinstance(recomendacoes, list):
        for i, (filme, nota_prevista) in enumerate(recomendacoes, 1):
            print(f"  {i}. {filme} (nota prevista: {nota_prevista:.2f})")
    else:
        print(recomendacoes)

# 3. PROJETO 3: PREVISÃO DE SÉRIES TEMPORAIS
print("\n\n3. PROJETO 3: PREVISÃO DE SÉRIES TEMPORAIS")
print("-" * 50)

# Gerar dados de vendas mensais com sazonalidade
np.random.seed(42)
n_meses = 48  # 4 anos de dados

# Base trend + sazonalidade + ruído
trend = np.linspace(1000, 2000, n_meses)
sazonalidade = 200 * np.sin(2 * np.pi * np.arange(n_meses) / 12)  # Sazonalidade anual
ruído = np.random.normal(0, 100, n_meses)

vendas = trend + sazonalidade + ruído
vendas = np.maximum(vendas, 500)  # Mínimo de 500

# Criar DataFrame
datas = pd.date_range('2020-01-01', periods=n_meses, freq='M')
df_temporal = pd.DataFrame({
    'data': datas,
    'vendas': vendas
})

print(f"Dataset temporal: {df_temporal.shape}")
print(f"\nPrimeiras linhas:")
print(df_temporal.head())

# Análise exploratória
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(df_temporal['data'], df_temporal['vendas'])
plt.title('Vendas Mensais')
plt.ylabel('Vendas')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
# Decomposição sazonal simplificada
media_movel = df_temporal['vendas'].rolling(window=12).mean()
plt.plot(df_temporal['data'], df_temporal['vendas'], alpha=0.5, label='Original')
plt.plot(df_temporal['data'], media_movel, label='Média Móvel 12 meses')
plt.title('Tendência')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 3)
# Boxplot por mês
df_temporal['mes'] = df_temporal['data'].dt.month
sns.boxplot(data=df_temporal, x='mes', y='vendas')
plt.title('Vendas por Mês')
plt.xlabel('Mês')

plt.subplot(2, 2, 4)
# Autocorrelação
pd.plotting.autocorrelation_plot(df_temporal['vendas'])
plt.title('Autocorrelação')
plt.tight_layout()
plt.show()

# Feature engineering para previsão
def criar_features_temporais(df):
    """Criar features para modelo de previsão"""
    df = df.copy()
    
    # Lags
    for lag in [1, 2, 3, 6, 12]:
        df[f'vendas_lag_{lag}'] = df['vendas'].shift(lag)
    
    # Médias móveis
    for window in [3, 6, 12]:
        df[f'vendas_ma_{window}'] = df['vendas'].rolling(window=window).mean()
    
    # Features temporais
    df['mes'] = df['data'].dt.month
    df['trimestre'] = df['data'].dt.quarter
    df['ano'] = df['data'].dt.year
    
    # Diferenças
    df['vendas_diff_1'] = df['vendas'].diff(1)
    df['vendas_diff_12'] = df['vendas'].diff(12)
    
    return df

df_features = criar_features_temporais(df_temporal)

# Remover linhas com NaN (devido aos lags)
df_features = df_features.dropna()

print(f"\nDataset com features: {df_features.shape}")
print(f"Features criadas: {[col for col in df_features.columns if col not in ['data', 'vendas']]}")

# Modelo de previsão
features = [col for col in df_features.columns if col not in ['data', 'vendas']]
X = df_features[features]
y = df_features['vendas']

# Divisão treino/teste (temporal)
split_point = int(len(X) * 0.8)
X_train, X_test = X[:split_point], X[split_point:]
y_train, y_test = y[:split_point], y[split_point:]

# Modelo Random Forest para regressão
modelo_temporal = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_temporal.fit(X_train, y_train)

# Previsões
y_pred = modelo_temporal.predict(X_test)

# Métricas
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\nMétricas do Modelo:")
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.4f}")

# Visualizar previsões
plt.figure(figsize=(12, 6))
plt.plot(df_features['data'].iloc[split_point:], y_test, label='Real', alpha=0.7)
plt.plot(df_features['data'].iloc[split_point:], y_pred, label='Previsto', alpha=0.7)
plt.title('Previsão de Vendas')
plt.xlabel('Data')
plt.ylabel('Vendas')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Importância das features
importancia_features = pd.DataFrame({
    'feature': features,
    'importance': modelo_temporal.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nTop 10 Features Mais Importantes:")
print(importancia_features.head(10))

# Função para prever próximos meses
def prever_proximos_meses(modelo, df_ultimo, n_meses=3):
    """Prever próximos n meses"""
    previsoes = []
    
    for i in range(n_meses):
        # Criar features para o próximo mês
        prox_data = df_ultimo['data'] + pd.DateOffset(months=1)
        
        # Simplificado - em produção seria mais complexo
        features_prox = {
            'mes': prox_data.month,
            'trimestre': prox_data.quarter,
            'ano': prox_data.year
        }
        
        # Adicionar lags (usando valores conhecidos)
        for lag in [1, 2, 3, 6, 12]:
            if f'vendas_lag_{lag}' in df_ultimo.columns:
                features_prox[f'vendas_lag_{lag}'] = df_ultimo['vendas'].iloc[-lag] if lag <= len(df_ultimo) else df_ultimo['vendas'].mean()
        
        # Prever
        X_prox = pd.DataFrame([features_prox])
        previsao = modelo.predict(X_prox)[0]
        
        previsoes.append({
            'data': prox_data,
            'previsao': previsao
        })
        
        # Atualizar dataframe para próxima iteração
        df_ultimo = pd.concat([df_ultimo, pd.DataFrame({
            'data': [prox_data],
            'vendas': [previsao]
        })], ignore_index=True)
    
    return pd.DataFrame(previsoes)

# Prever próximos 3 meses
previsoes_futuras = prever_proximos_meses(modelo_temporal, df_features, 3)
print(f"\nPrevisões para próximos 3 meses:")
print(previsoes_futuras)

# 4. PROJETO 4: DETECÇÃO DE ANOMALIAS
print("\n\n4. PROJETO 4: DETECÇÃO DE ANOMALIAS")
print("-" * 50)

# Gerar dados de transações com anomalias
np.random.seed(42)
n_transacoes = 1000

# Transações normais
transacoes_normais = np.random.lognormal(7, 0.5, int(n_transacoes * 0.95))

# Anomalias (valores muito altos)
transacoes_anomalas = np.random.lognormal(10, 0.3, int(n_transacoes * 0.05))

# Combinar
valores = np.concatenate([transacoes_normais, transacoes_anomalas])
np.random.shuffle(valores)

# Criar DataFrame
df_anomalias = pd.DataFrame({
    'id_transacao': range(1, n_transacoes + 1),
    'valor': valores,
    'data_hora': pd.date_range('2023-01-01', periods=n_transacoes, freq='H'),
    'tipo': np.random.choice(['transferencia', 'pagamento', 'saque'], n_transacoes)
})

# Marcar anomalias (baseado em valor alto)
threshold = np.percentile(valores, 95)
df_anomalias['eh_anomalia'] = df_anomalias['valor'] > threshold

print(f"Dataset de anomalias: {df_anomalias.shape}")
print(f"\nEstatísticas:")
print(df_anomalias['valor'].describe().round(2))
print(f"\nAnomalias detectadas: {df_anomalias['eh_anomalia'].sum()} ({df_anomalias['eh_anomalia'].mean():.2%})")

# Visualização
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(df_anomalias['valor'], bins=50, alpha=0.7)
plt.axvline(threshold, color='red', linestyle='--', label=f'Threshold: R${threshold:.2f}')
plt.title('Distribuição de Valores')
plt.xlabel('Valor (R$)')
plt.ylabel('Frequência')
plt.legend()

plt.subplot(1, 2, 2)
cores = ['red' if anom else 'blue' for anom in df_anomalias['eh_anomalia']]
plt.scatter(range(len(df_anomalias)), df_anomalias['valor'], c=cores, alpha=0.6)
plt.title('Transações (Vermelho = Anomalia)')
plt.xlabel('Índice da Transação')
plt.ylabel('Valor (R$)')
plt.tight_layout()
plt.show()

# Modelo para detecção de anomalias
# Usaremos Isolation Forest (simplificado)
from sklearn.ensemble import IsolationForest

# Features para detecção
features_anomalia = ['valor']
X_anomalia = df_anomalia[features_anomalia].values.reshape(-1, 1)

# Modelo
modelo_anomalia = IsolationForest(contamination=0.05, random_state=42)
modelo_anomalia.fit(X_anomalia)

# Previsões
df_anomalias['anomalia_predita'] = modelo_anomalia.predict(X_anomalia) == -1

# Avaliação
from sklearn.metrics import classification_report, confusion_matrix

print(f"\nAvaliação do Detector de Anomalias:")
print(classification_report(df_anomalias['eh_anomalia'], df_anomalias['anomalia_predita']))

print(f"Matriz de Confusão:")
print(confusion_matrix(df_anomalias['eh_anomalia'], df_anomalias['anomalia_predita']))

# Análise das anomalias detectadas
anomalias_detectadas = df_anomalias[df_anomalias['anomalia_predita']]
print(f"\nAnálise das Anomalias Detectadas:")
print(f"Total: {len(anomalias_detectadas)}")
print(f"Valor médio: R${anomalias_detectadas['valor'].mean():.2f}")
print(f"Por tipo:")
print(anomalias_detectadas['tipo'].value_counts())

# 5. RESUMO DOS PROJETOS
print("\n\n5. RESUMO DOS PROJETOS")
print("-" * 50)

print("PROJETOS IMPLEMENTADOS:")
print("✅ 1. ANÁLISE DE SENTIMENTOS")
print("   • Processamento de texto com TF-IDF")
print("   • Classificação de reviews")
print("   • Aplicação em tempo real")

print("\n✅ 2. SISTEMA DE RECOMENDAÇÃO")
print("   • Filtragem colaborativa")
print("   • Similaridade entre usuários")
print("   • Recomendações personalizadas")

print("\n✅ 3. PREVISÃO DE SÉRIES TEMPORAIS")
print("   • Feature engineering temporal")
print("   • Modelo Random Forest")
print("   • Previsão de vendas")

print("\n✅ 4. DETECÇÃO DE ANOMALIAS")
print("   • Isolation Forest")
print("   • Detecção em transações")
print("   • Sistema de alerta")

print("\nAPLICAÇÕES NO MUNDO REAL:")
print("🏢 EMPRESAS:")
print("   • Análise de feedback de clientes")
print("   • Recomendação de produtos")
print("   • Previsão de demanda")
print("   • Detecção de fraudes")

print("\n💡 INSIGHTS OBTIDOS:")
print("   • Técnicas de NLP para texto")
print("   • Algoritmos de recomendação")
print("   • Modelos de séries temporais")
print("   • Métodos de detecção de anomalias")

print("\n🚀 PRÓXIMOS PASSOS:")
print("   • Deploy com APIs (Flask/FastAPI)")
print("   • Integração com bancos de dados")
print("   • Monitoramento e logging")
print("   • Retreinamento automático")

print("\n" + "=" * 70)
print("PROJETOS REAIS 80/20 CONCLUÍDOS!")
print("Você tem projetos prontos para o portfólio!")
print("=" * 70)
