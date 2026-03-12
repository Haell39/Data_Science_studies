"""
PROJETO COMPLETO - ANÁLISE DE SENTIMENTOS
Sistema completo para análise de sentimentos de reviews
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import re
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PROJETO COMPLETO - ANÁLISE DE SENTIMENTOS")
print("=" * 80)

# 1. COLETA E PREPARAÇÃO DE DADOS
print("\n1. COLETA E PREPARAÇÃO DE DADOS")
print("-" * 60)

# Dataset realista de reviews de produtos
np.random.seed(42)

# Templates de reviews por categoria e sentimento
templates = {
    'positivo': {
        'eletronicos': [
            "Produto excelente! Super recomendo.",
            "Qualidade incrível, funcionou perfeitamente.",
            "Fantástico! Valeu cada centavo investido.",
            "Maravilhoso! Atendeu todas as expectativas.",
            "Perfeito! Com certeza compraria novamente.",
            "Ótimo produto! Muito satisfeito com a compra.",
            "Sensacional! Superou minhas expectativas.",
            "Incrível! Tecnologia de ponta."
        ],
        'roupas': [
            "Adorei! Tecido de ótima qualidade.",
            "Perfeito no tamanho e no caimento.",
            "Excelente! Material muito confortável.",
            "Maravilhoso! Ficou lindo em mim.",
            "Ótimo! Exatamente como esperado.",
            "Perfeito! Cores vivas e duradouras."
        ],
        'alimentos': [
            "Delicioso! Sabor incrível.",
            "Excelente qualidade! Fresco e saboroso.",
            "Perfeito! Exatamente o que esperava.",
            "Ótimo! Valeu muito a pena.",
            "Maravilhoso! Recomendo a todos."
        ]
    },
    'negativo': {
        'eletronicos': [
            "Péssimo! Não funcionou nada.",
            "Horrível! Perdi meu dinheiro.",
            "Terrível! Produto de baixíssima qualidade.",
            "Decepcionante! Não funcionou como esperado.",
            "Ruim! Apresentou defeito rapidamente.",
            "Fraco! Material de péssima qualidade.",
            "Insatisfatório! Problemas desde o início.",
            "Desapontador! Esperava muito mais."
        ],
        'roupas': [
            "Péssimo! Tecido de péssima qualidade.",
            "Horrível! Não serviu no tamanho.",
            "Terrível! Cor totalmente diferente da foto.",
            "Ruim! Material muito desconfortável.",
            "Decepcionante! Desbotou após primeira lavagem."
        ],
        'alimentos': [
            "Péssimo! Sabor horrível.",
            "Horrível! Produto estragado.",
            "Terrível! Não era fresco.",
            "Ruim! Sabor muito artificial.",
            "Decepcionante! Veio com problema."
        ]
    },
    'neutro': [
        "Produto ok, nada especial.",
        "Funciona como esperado.",
        "Preço justo para o que oferece.",
        "Normal, sem surpresas.",
        "Razoável, poderia ser melhor.",
        "Aceitável dentro do esperado.",
        "Regular, atende o básico."
    ]
}

# Gerar dataset
n_reviews = 2000
reviews_data = []

for i in range(n_reviews):
    # Escolher categoria
    categoria = np.random.choice(['eletronicos', 'roupas', 'alimentos'])
    
    # Escolher sentimento
    sentimento_probs = [0.4, 0.4, 0.2]  # 40% positivo, 40% negativo, 20% neutro
    sentimento = np.random.choice(['positivo', 'negativo', 'neutro'], p=sentimento_probs)
    
    # Escolher review
    if sentimento == 'neutro':
        review = np.random.choice(templates['neutro'])
    else:
        review = np.random.choice(templates[sentimento][categoria])
    
    # Adicionar detalhes específicos
    if sentimento == 'positivo' and np.random.random() < 0.3:
        detalhes = ["muito bom", "excelente", "fantástico", "incrível", "perfeito"]
        review += " " + np.random.choice(detalhes)
    elif sentimento == 'negativo' and np.random.random() < 0.3:
        detalhes = ["muito ruim", "péssimo", "horrível", "terrível", "decepcionante"]
        review += " " + np.random.choice(detalhes)
    
    # Nota (consistente com sentimento)
    if sentimento == 'positivo':
        nota = np.random.choice([5, 4, 3], p=[0.6, 0.3, 0.1])
    elif sentimento == 'negativo':
        nota = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
    else:
        nota = np.random.choice([3, 4, 2], p=[0.5, 0.3, 0.2])
    
    reviews_data.append({
        'id_review': i + 1,
        'review': review,
        'categoria': categoria,
        'sentimento': sentimento,
        'nota': nota,
        'data': pd.Timestamp('2023-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
    })

df_reviews = pd.DataFrame(reviews_data)

print(f"Dataset criado: {df_reviews.shape}")
print(f"\nDistribuição por sentimento:")
print(df_reviews['sentimento'].value_counts())
print(f"\nDistribuição por categoria:")
print(df_reviews['categoria'].value_counts())

# 2. ANÁLISE EXPLORATÓRIA
print("\n2. ANÁLISE EXPLORATÓRIA")
print("-" * 60)

# Estatísticas dos reviews
df_reviews['comprimento'] = df_reviews['review'].str.len()
df_reviews['palavras'] = df_reviews['review'].str.split().str.len()

print("Estatísticas dos reviews:")
print(df_reviews.groupby('sentimento')[['comprimento', 'palavras']].describe().round(1))

# Visualizações
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Análise Exploratória de Reviews', fontsize=16)

# Distribuição de sentimentos
df_reviews['sentimento'].value_counts().plot(kind='bar', ax=axes[0,0], color=['green', 'red', 'gray'])
axes[0,0].set_title('Distribuição de Sentimentos')
axes[0,0].tick_params(axis='x', rotation=45)

# Distribuição de notas
df_reviews['nota'].value_counts().sort_index().plot(kind='bar', ax=axes[0,1])
axes[0,1].set_title('Distribuição de Notas')

# Sentimento por categoria
pd.crosstab(df_reviews['categoria'], df_reviews['sentimento']).plot(kind='bar', ax=axes[0,2])
axes[0,2].set_title('Sentimento por Categoria')
axes[0,2].tick_params(axis='x', rotation=45)

# Comprimento por sentimento
sns.boxplot(data=df_reviews, x='sentimento', y='comprimento', ax=axes[1,0])
axes[1,0].set_title('Comprimento por Sentimento')

# Nota por sentimento
sns.boxplot(data=df_reviews, x='sentimento', y='nota', ax=axes[1,1])
axes[1,1].set_title('Nota por Sentimento')

# Reviews ao longo do tempo
df_reviews.groupby(df_reviews['data'].dt.month)['id_review'].count().plot(kind='line', ax=axes[1,2])
axes[1,2].set_title('Reviews por Mês')
axes[1,2].set_xlabel('Mês')

plt.tight_layout()
plt.show()

# 3. PRÉ-PROCESSAMENTO DE TEXTO
print("\n3. PRÉ-PROCESSAMENTO DE TEXTO")
print("-" * 60)

def limpar_texto(texto):
    """Função para limpar e normalizar texto"""
    # Converter para minúsculas
    texto = texto.lower()
    
    # Remover caracteres especiais e números
    texto = re.sub(r'[^a-zA-Záàâãéêíóôõúçñ\s]', '', texto)
    
    # Remover espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

# Aplicar limpeza
df_reviews['review_limpo'] = df_reviews['review'].apply(limpar_texto)

print("Exemplo de pré-processamento:")
for i in range(3):
    print(f"\nOriginal: {df_reviews.iloc[i]['review']}")
    print(f"Limpo:    {df_reviews.iloc[i]['review_limpo']}")

# Análise de palavras mais comuns
from collections import Counter

# Palavras por sentimento
palavras_por_sentimento = {}
for sentimento in df_reviews['sentimento'].unique():
    reviews_sentimento = df_reviews[df_reviews['sentimento'] == sentimento]['review_limpo']
    todas_palavras = ' '.join(reviews_sentimento).split()
    palavras_por_sentimento[sentimento] = Counter(todas_palavras).most_common(10)

print("\nPalavras mais comuns por sentimento:")
for sentimento, palavras in palavras_por_sentimento.items():
    print(f"\n{sentimento.capitalize()}:")
    for palavra, count in palavras[:5]:
        print(f"  {palavra}: {count}")

# 4. VETORIZAÇÃO E FEATURE ENGINEERING
print("\n4. VETORIZAÇÃO E FEATURE ENGINEERING")
print("-" * 60)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words=['o', 'a', 'os', 'as', 'de', 'do', 'da', 'em', 'para', 'com', 'um', 'uma', 
                'é', 'foi', 'ser', 'está', 'estou', 'estamos', 'muito', 'mais', 'mas'],
    ngram_range=(1, 2),  # bigramas também
    min_df=2,  # mínimo de 2 documentos
    max_df=0.8  # máximo de 80% dos documentos
)

# Vetorizar texto
X_text = vectorizer.fit_transform(df_reviews['review_limpo'])

# Encoder para sentimento
le_sentimento = LabelEncoder()
y_sentimento = le_sentimento.fit_transform(df_reviews['sentimento'])

print(f"Shape da matriz TF-IDF: {X_text.shape}")
print(f"Features (vocabulário): {len(vectorizer.vocabulary_)}")
print(f"Target: {le_sentimento.classes_}")

# 5. MODELOS DE MACHINE LEARNING
print("\n5. MODELOS DE MACHINE LEARNING")
print("-" * 60)

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X_text, y_sentimento, test_size=0.2, random_state=42, stratify=y_sentimento
)

print(f"Divisão - Treino: {X_train.shape}, Teste: {X_test.shape}")

# Modelos para comparar
modelos = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='linear', random_state=42),
    'Naive Bayes': MultinomialNB()
}

# Avaliar modelos
resultados = {}
for nome, modelo in modelos.items():
    print(f"\nTreinando {nome}...")
    
    # Treinar
    modelo.fit(X_train, y_train)
    
    # Prever
    y_pred = modelo.predict(X_test)
    
    # Métricas
    acc = accuracy_score(y_test, y_pred)
    
    resultados[nome] = {
        'modelo': modelo,
        'acuracia': acc,
        'previsoes': y_pred
    }
    
    print(f"Acurácia: {acc:.4f}")

# Visualizar comparação
plt.figure(figsize=(8, 5))
nomes = list(resultados.keys())
acuracias = [resultados[nome]['acuracia'] for nome in nomes]

plt.bar(nomes, acuracias, color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparação de Modelos')
plt.ylabel('Acurácia')
plt.ylim(0, 1)
for i, acc in enumerate(acuracias):
    plt.text(i, acc + 0.01, f'{acc:.3f}', ha='center')
plt.tight_layout()
plt.show()

# 6. MELHOR MODELO - ANÁLISE DETALHADA
print("\n6. MELHOR MODELO - ANÁLISE DETALHADA")
print("-" * 60)

# Escolher melhor modelo
melhor_nome = max(resultados, key=lambda x: resultados[x]['acuracia'])
melhor_modelo = resultados[melhor_nome]['modelo']

print(f"Melhor modelo: {melhor_nome}")
print(f"Acurácia: {resultados[melhor_nome]['acuracia']:.4f}")

# Relatório detalhado
y_pred_best = resultados[melhor_nome]['previsoes']
print(f"\nRelatório de Classificação:")
print(classification_report(y_test, y_pred_best, target_names=le_sentimento.classes_))

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
           xticklabels=le_sentimento.classes_,
           yticklabels=le_sentimento.classes_)
plt.title('Matriz de Confusão')
plt.ylabel('Real')
plt.xlabel('Previsto')
plt.show()

# 7. ANÁLISE DE ERROS
print("\n7. ANÁLISE DE ERROS")
print("-" * 60)

# Analisar erros
erros = []
for i in range(len(y_test)):
    if y_test[i] != y_pred_best[i]:
        erros.append({
            'indice': i,
            'real': le_sentimento.inverse_transform([y_test[i]])[0],
            'predito': le_sentimento.inverse_transform([y_pred_best[i]])[0],
            'review': df_reviews.iloc[X_test[i].toarray().nonzero()[1][0]]['review'] if X_test[i].nnz > 0 else "Review não encontrado"
        })

print(f"Total de erros: {len(erros)} ({len(erros)/len(y_test):.2%})")

# Exemplos de erros
print(f"\nExemplos de erros de classificação:")
for i, erro in enumerate(erros[:5]):
    print(f"\nErro {i+1}:")
    print(f"  Real: {erro['real']}")
    print(f"  Previsto: {erro['predito']}")
    print(f"  Review: {erro['review'][:100]}...")

# 8. VALIDAÇÃO CRUZADA E OTIMIZAÇÃO
print("\n8. VALIDAÇÃO CRUZADA E OTIMIZAÇÃO")
print("-" * 60)

from sklearn.model_selection import cross_val_score, StratifiedKFold

# Validação cruzada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(melhor_modelo, X_text, y_sentimento, cv=cv, scoring='accuracy')

print(f"Validação Cruzada (5-fold):")
print(f"Scores: {cv_scores}")
print(f"Média: {cv_scores.mean():.4f}")
print(f"Desvio: {cv_scores.std():.4f}")

# Grid Search para otimização (simplificado)
if melhor_nome == 'Random Forest':
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5]
    }
    
    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=3,
        scoring='accuracy',
        n_jobs=-1
    )
    
    print("\nRealizando Grid Search...")
    grid_search.fit(X_train, y_train)
    
    print(f"Melhores parâmetros: {grid_search.best_params_}")
    print(f"Melhor acurácia: {grid_search.best_score_:.4f}")
    
    # Usar modelo otimizado
    melhor_modelo = grid_search.best_estimator_

# 9. SISTEMA DE PREDIÇÃO
print("\n9. SISTEMA DE PREDIÇÃO")
print("-" * 60)

def analisar_sentimento_review(review, modelo, vectorizer, label_encoder):
    """
    Sistema completo para analisar sentimento de um novo review
    """
    # Limpar texto
    review_limpo = limpar_texto(review)
    
    # Vetorizar
    review_vector = vectorizer.transform([review_limpo])
    
    # Prever
    predicao = modelo.predict(review_vector)[0]
    probabilidades = modelo.predict_proba(review_vector)[0]
    
    # Converter para labels originais
    sentimento_predito = label_encoder.inverse_transform([predicao])[0]
    
    # Obter confiança
    confianca = max(probabilidades)
    
    # Mapear probabilidades para sentimentos
    probs_dict = dict(zip(label_encoder.classes_, probabilidades))
    
    return {
        'review_original': review,
        'review_limpo': review_limpo,
        'sentimento_predito': sentimento_predito,
        'confianca': confianca,
        'probabilidades': probs_dict
    }

# Testar sistema
reviews_teste = [
    "Este produto é simplesmente incrível! Funciona perfeitamente e superou todas as minhas expectativas.",
    "Péssima experiência! O produto chegou com defeito e o atendimento ao cliente foi horrível.",
    "Produto razoável. Cumpre o que promete, mas nada extraordinário.",
    "Excelente qualidade! Recomendo a todos, vale muito a pena.",
    "Não gostei. Material de baixa qualidade e não funcionou como esperado."
]

print("Teste do Sistema de Análise:")
for i, review in enumerate(reviews_teste, 1):
    resultado = analisar_sentimento_review(review, melhor_modelo, vectorizer, le_sentimento)
    
    print(f"\nReview {i}:")
    print(f"Texto: {resultado['review_original']}")
    print(f"Sentimento: {resultado['sentimento_predito']}")
    print(f"Confiança: {resultado['confianca']:.2%}")
    print(f"Probabilidades: {resultado['probabilidades']}")

# 10. DEPLOY E PRODUÇÃO
print("\n10. DEPLOY E PRODUÇÃO")
print("-" * 60)

import joblib

# Salvar modelo e componentes
joblib.dump(melhor_modelo, 'modelo_sentimento.pkl')
joblib.dump(vectorizer, 'vectorizer_sentimento.pkl')
joblib.dump(le_sentimento, 'label_encoder_sentimento.pkl')

# Salvar dataset
df_reviews.to_csv('dataset_reviews.csv', index=False)

print("Componentes salvos:")
print("• modelo_sentimento.pkl")
print("• vectorizer_sentimento.pkl")
print("• label_encoder_sentimento.pkl")
print("• dataset_reviews.csv")

# Função para carregar e usar em produção
def carregar_sistema_sentimento():
    """Carrega todos os componentes do sistema"""
    modelo = joblib.load('modelo_sentimento.pkl')
    vectorizer = joblib.load('vectorizer_sentimento.pkl')
    label_encoder = joblib.load('label_encoder_sentimento.pkl')
    
    return modelo, vectorizer, label_encoder

# API Flask (exemplo conceitual)
print(f"\nExemplo de API Flask:")
print("""
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Carregar modelo
modelo, vectorizer, label_encoder = carregar_sistema_sentimento()

@app.route('/analisar', methods=['POST'])
def analisar_sentimento_api():
    data = request.get_json()
    review = data.get('review', '')
    
    resultado = analisar_sentimento_review(review, modelo, vectorizer, label_encoder)
    
    return jsonify({
        'sentimento': resultado['sentimento_predito'],
        'confianca': resultado['confianca'],
        'probabilidades': resultado['probabilidades']
    })

if __name__ == '__main__':
    app.run(debug=True)
""")

# 11. MONITORAMENTO E MELHORIAS
print("\n11. MONITORAMENTO E MELHORIAS")
print("-" * 60)

print("MÉTRICAS PARA MONITORAR:")
print("• Acurácia do modelo em produção")
print("• Distribuição das previsões")
print("• Confiança média das previsões")
print("• Volume de análises por dia")
print("• Feedback dos usuários")

print("\nMELHORIAS FUTURAS:")
print("• Adicionar mais categorias de produtos")
print("• Implementar análise de aspecto (feature-based)")
print("• Usar modelos mais avançados (BERT, GPT)")
print("• Adicionar suporte a múltiplos idiomas")
print("• Implementar aprendizado contínuo")

# 12. RELATÓRIO FINAL
print("\n12. RELATÓRIO FINAL")
print("-" * 60)

# Métricas finais
metricas_finais = {
    'Dataset': f"{len(df_reviews)} reviews",
    'Categorias': df_reviews['categoria'].nunique(),
    'Sentimentos': df_reviews['sentimento'].nunique(),
    'Features': len(vectorizer.vocabulary_),
    'Modelo': melhor_nome,
    'Acurácia': f"{resultados[melhor_nome]['acuracia']:.4f}",
    'CV Média': f"{cv_scores.mean():.4f}",
    'CV Desvio': f"{cv_scores.std():.4f}"
}

print("RELATÓRIO FINAL DO PROJETO:")
for metrica, valor in metricas_finais.items():
    print(f"• {metrica}: {valor}")

print(f"\nINSIGHTS PRINCIPAIS:")
print("✅ Sistema completo de análise de sentimentos")
print("✅ Pré-processamento robusto de texto")
print("✅ Comparação de múltiplos modelos")
print("✅ Validação cruzada e otimização")
print("✅ Sistema pronto para deploy")

print(f"\nAPLICAÇÕES PRÁTICAS:")
print("🏢 Análise de feedback de clientes")
print("🏢 Monitoramento de redes sociais")
print("🏢 Análise de reviews de produtos")
print("🏢 Suporte ao cliente automatizado")

print("\n" + "=" * 80)
print("PROJETO DE ANÁLISE DE SENTIMENTOS CONCLUÍDO!")
print("Sistema completo pronto para produção!")
print("=" * 80)
