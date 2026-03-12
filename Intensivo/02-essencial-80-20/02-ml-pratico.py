"""
MACHINE LEARNING PRÁTICO - 80/20
Os 20% mais importantes para resolver 80% dos problemas reais
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("MACHINE LEARNING PRÁTICO - 80/20")
print("=" * 70)

# 1. PROBLEMA REAL - CHURN DE CLIENTES
print("\n1. PROBLEMA REAL - CHURN DE CLIENTES")
print("-" * 50)

# Gerar dataset realista de churn
np.random.seed(42)
n_clientes = 2000

# Features realistas
dados = {
    'idade': np.random.normal(38, 12, n_clientes),
    'tempo_cliente': np.random.exponential(24, n_clientes),  # meses
    'saldo_medio': np.random.lognormal(8, 1, n_clientes),
    'num_produtos': np.random.randint(1, 6, n_clientes),
    'tem_cartao': np.random.choice([0, 1], n_clientes, p=[0.3, 0.7]),
    'ativo_ult_3m': np.random.choice([0, 1], n_clientes, p=[0.15, 0.85]),
    'reclamacoes': np.random.poisson(0.5, n_clientes),
    'score_credito': np.random.uniform(300, 850, n_clientes),
    'renda_estimada': np.random.lognormal(10, 0.5, n_clientes),
    'cidade': np.random.choice(['SP', 'RJ', 'BH', 'POA', 'REC'], n_clientes),
    'segmento': np.random.choice(['Basic', 'Silver', 'Gold', 'Platinum'], 
                                n_clientes, p=[0.4, 0.3, 0.2, 0.1])
}

df = pd.DataFrame(dados)

# Ajustar dados
df['idade'] = np.maximum(df['idade'], 18)
df['tempo_cliente'] = np.maximum(df['tempo_cliente'], 1)
df['saldo_medio'] = np.maximum(df['saldo_medio'], 100)
df['reclamacoes'] = np.minimum(df['reclamacoes'], 5)

# Calcular probabilidade de churn (realista)
prob_churn = (
    -df['idade'] / 100 +  # Mais velho = menos churn
    -df['tempo_cliente'] / 50 +  # Mais tempo = menos churn
    -df['saldo_medio'] / 100000 +  # Mais saldo = menos churn
    -df['num_produtos'] * 0.1 +  # Mais produtos = menos churn
    -df['tem_cartao'] * 0.15 +  # Tem cartão = menos churn
    -df['ativo_ult_3m'] * 0.3 +  # Ativo = menos churn
    df['reclamacoes'] * 0.2 +  # Mais reclamações = mais churn
    (850 - df['score_credito']) / 1000 +  # Score baixo = mais churn
    np.where(df['segmento'] == 'Basic', 0.3,  # Basic = mais churn
             np.where(df['segmento'] == 'Platinum', -0.2, 0))  # Platinum = menos churn
)

# Adicionar ruído e normalizar
prob_churn += np.random.normal(0, 0.15, n_clientes)
prob_churn = np.clip(prob_churn, 0, 1)

# Criar target
df['churn'] = (prob_churn > 0.25).astype(int)

# Adicionar valores ausentes (realista)
df.loc[np.random.choice(df.index, 50, replace=False), 'renda_estimada'] = np.nan
df.loc[np.random.choice(df.index, 30, replace=False), 'score_credito'] = np.nan

print(f"Dataset criado: {df.shape}")
print(f"\nDistribuição de churn:")
print(df['churn'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

print(f"\nEstatísticas por churn:")
print(df.groupby('churn').agg({
    'idade': 'mean',
    'tempo_cliente': 'mean',
    'saldo_medio': 'mean',
    'score_credito': 'mean',
    'reclamacoes': 'mean'
}).round(2))

# 2. PREPARAÇÃO DE DADOS AVANÇADA
print("\n2. PREPARAÇÃO DE DADOS AVANÇADA")
print("-" * 50)

# Separar features e target
X = df.drop('churn', axis=1)
y = df['churn']

# Identificar tipos de colunas
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

print(f"Features numéricas: {list(numeric_features)}")
print(f"Features categóricas: {list(categorical_features)}")

# Pipeline de pré-processamento
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=42, stratify=y)

print(f"\nDivisão dos dados:")
print(f"Treino: {X_train.shape}")
print(f"Teste: {X_test.shape}")
print(f"Churn treino: {y_train.mean():.2%}")
print(f"Churn teste: {y_test.mean():.2%}")

# 3. COMPARAÇÃO DE MÚLTIPLOS MODELOS
print("\n3. COMPARAÇÃO DE MÚLTIPLOS MODELOS")
print("-" * 50)

# Modelos para comparar
modelos = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42)
}

# Avaliar modelos
resultados = {}
for nome, modelo in modelos.items():
    # Pipeline completo
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', modelo)
    ])
    
    # Validação cruzada
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='roc_auc')
    
    resultados[nome] = {
        'mean_auc': cv_scores.mean(),
        'std_auc': cv_scores.std(),
        'scores': cv_scores
    }
    
    print(f"{nome}:")
    print(f"  AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# Visualizar comparação
plt.figure(figsize=(10, 6))
nomes = list(resultados.keys())
aucs = [resultados[nome]['mean_auc'] for nome in nomes]
stds = [resultados[nome]['std_auc'] for nome in nomes]

plt.bar(nomes, aucs, yerr=stds, capsize=5, alpha=0.7)
plt.title('Comparação de Modelos - AUC Score')
plt.ylabel('AUC Score')
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 4. MELHOR MODELO - RANDOM FOREST
print("\n4. MELHOR MODELO - RANDOM FOREST")
print("-" * 50)

# Escolher melhor modelo (Random Forest geralmente performs bem)
melhor_modelo = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Treinar
melhor_modelo.fit(X_train, y_train)

# Previsões
y_pred = melhor_modelo.predict(X_test)
y_pred_proba = melhor_modelo.predict_proba(X_test)[:, 1]

# Métricas
auc = roc_auc_score(y_test, y_pred_proba)
print(f"AUC Score: {auc:.4f}")

print(f"\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
           xticklabels=['Não Churn', 'Churn'], 
           yticklabels=['Não Churn', 'Churn'])
plt.title('Matriz de Confusão')
plt.ylabel('Real')
plt.xlabel('Previsto')
plt.show()

# Curva ROC
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--', linewidth=1)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Curva ROC')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 5. FEATURE ENGINEERING E SELEÇÃO
print("\n5. FEATURE ENGINEERING E SELEÇÃO")
print("-" * 50)

# Obter nomes das features após preprocessing
# Para isso, precisamos fitar o preprocessor
X_train_processed = melhor_modelo.named_steps['preprocessor'].fit_transform(X_train)

# Obter nomes das features
feature_names = []
# Features numéricas
feature_names.extend(numeric_features)
# Features categóricas (one-hot)
ohe = melhor_modelo.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
feature_names.extend(ohe.get_feature_names_out(categorical_features))

# Importância das features
importancias = melhor_modelo.named_steps['classifier'].feature_importances_
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importancias
}).sort_values('importance', ascending=False)

print("Top 10 Features Mais Importantes:")
print(feature_importance_df.head(10))

# Visualizar importância
plt.figure(figsize=(10, 6))
top_features = feature_importance_df.head(10)
plt.barh(top_features['feature'], top_features['importance'], color='skyblue')
plt.title('Top 10 Features Mais Importantes')
plt.xlabel('Importância')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 6. OTIMIZAÇÃO DE HIPERPARÂMETROS
print("\n6. OTIMIZAÇÃO DE HIPERPARÂMETROS")
print("-" * 50)

# Grid Search simplificado (para demonstração)
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [10, 20, None],
    'classifier__min_samples_split': [2, 5],
    'classifier__min_samples_leaf': [1, 2]
}

# Pipeline com GridSearch
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='roc_auc', 
                          n_jobs=-1, verbose=1)

print("Realizando Grid Search...")
grid_search.fit(X_train, y_train)

print(f"\nMelhores parâmetros: {grid_search.best_params_}")
print(f"Melhor AUC: {grid_search.best_score_:.4f}")

# Usar modelo otimizado
modelo_otimizado = grid_search.best_estimator_

# 7. ANÁLISE DE ERROS
print("\n7. ANÁLISE DE ERROS")
print("-" * 50)

# Previsões com modelo otimizado
y_pred_opt = modelo_otimizado.predict(X_test)
y_pred_proba_opt = modelo_otimizado.predict_proba(X_test)[:, 1]

# Analisar erros
erros = X_test.copy()
erros['churn_real'] = y_test
erros['churn_pred'] = y_pred_opt
erros['probabilidade'] = y_pred_proba_opt
erros['erro'] = erros['churn_real'] != erros['churn_pred']

print("Análise de Erros:")
print(f"Total de erros: {erros['erro'].sum()}")
print(f"Taxa de erro: {erros['erro'].mean():.2%}")

# Analisar falsos positivos e falsos negativos
falsos_positivos = erros[(erros['churn_real'] == 0) & (erros['churn_pred'] == 1)]
falsos_negativos = erros[(erros['churn_real'] == 1) & (erros['churn_pred'] == 0)]

print(f"\nFalsos Positivos: {len(falsos_positivos)}")
print(f"Falsos Negativos: {len(falsos_negativos)}")

# Características dos erros
print(f"\nCaracterísticas dos Falsos Negativos (clientes que churn mas não previmos):")
print(falsos_negativos[numeric_features].describe().round(2))

print(f"\nCaracterísticas dos Falsos Positivos (clientes que não churn mas previmos que sim):")
print(falsos_positivos[numeric_features].describe().round(2))

# 8. THRESHOLD OTIMIZAÇÃO
print("\n8. THRESHOLD OTIMIZAÇÃO")
print("-" * 50)

# Encontrar melhor threshold
thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = []

for threshold in thresholds:
    y_pred_thresh = (y_pred_proba_opt >= threshold).astype(int)
    from sklearn.metrics import f1_score
    f1 = f1_score(y_test, y_pred_thresh)
    f1_scores.append(f1)

# Melhor threshold
melhor_threshold = thresholds[np.argmax(f1_scores)]
melhor_f1 = max(f1_scores)

print(f"Melhor threshold: {melhor_threshold:.2f}")
print(f"F1 Score correspondente: {melhor_f1:.4f}")

# Visualizar
plt.figure(figsize=(10, 6))
plt.plot(thresholds, f1_scores, 'o-', linewidth=2, markersize=8)
plt.axvline(melhor_threshold, color='red', linestyle='--', label=f'Melhor Threshold = {melhor_threshold:.2f}')
plt.xlabel('Threshold')
plt.ylabel('F1 Score')
plt.title('Otimização de Threshold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Aplicar melhor threshold
y_pred_final = (y_pred_proba_opt >= melhor_threshold).astype(int)

print(f"\nRelatório com threshold otimizado:")
print(classification_report(y_test, y_pred_final))

# 9. VALIDAÇÃO CRUZADA ESTRATIFICADA
print("\n9. VALIDAÇÃO CRUZADA ESTRATIFICADA")
print("-" * 50)

from sklearn.model_selection import StratifiedKFold

# Validação cruzada estratificada
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_scores_stratified = cross_val_score(modelo_otimizado, X, y, cv=skf, scoring='roc_auc')

print("Validação Cruzada Estratificada:")
print(f"Scores: {cv_scores_stratified}")
print(f"Média: {cv_scores_stratified.mean():.4f}")
print(f"Desvio: {cv_scores_stratified.std():.4f}")
print(f"Intervalo 95%: [{cv_scores_stratified.mean() - 2*cv_scores_stratified.std():.4f}, {cv_scores_stratified.mean() + 2*cv_scores_stratified.std():.4f}]")

# 10. INTERPRETAÇÃO E BUSINESS INSIGHTS
print("\n10. INTERPRETAÇÃO E BUSINESS INSIGHTS")
print("-" * 50)

# Calcular métricas de negócio
total_clientes = len(df)
taxa_churn_real = df['churn'].mean()
taxa_churn_pred = y_pred_final.mean()

# Calcular economia potencial
custo_aquisicao_cliente = 500  # valor hipotético
custo_retention = 50  # valor hipotético

# Clientes em risco que podemos salvar
clientes_em_risco = (y_pred_proba_opt >= melhor_threshold).sum()
economia_potencial = clientes_em_risco * (custo_aquisicao_cliente - custo_retention)

print("INSIGHTS DE NEGÓCIO:")
print(f"• Taxa de churn real: {taxa_churn_real:.2%}")
print(f"• Taxa de churn prevista: {taxa_churn_pred:.2%}")
print(f"• Clientes em risco detectados: {clientes_em_risco}")
print(f"• Economia potencial: R${economia_potencial:,.2f}")

# Perfil do cliente churn
perfil_churn = df[df['churn'] == 1][numeric_features].mean()
perfil_nao_churn = df[df['churn'] == 0][numeric_features].mean()

print(f"\nPERFIL DO CLIENTE CHURN:")
for col in numeric_features:
    diff = ((perfil_churn[col] - perfil_nao_churn[col]) / perfil_nao_churn[col]) * 100
    print(f"• {col}: {perfil_churn[col]:.2f} ({diff:+.1f}% vs não-churn)")

# Recomendações
print(f"\nRECOMENDAÇÕES ESTRATÉGICAS:")
print(f"1. PREVENÇÃO:")
print(f"   • Focar em clientes com score de crédito < 600")
print(f"   • Monitorar clientes com > 2 reclamações")
print(f"   • Engajar clientes inativos nos últimos 3 meses")

print(f"\n2. RETENÇÃO:")
print(f"   • Oferecer benefícios para segmento Basic")
print(f"   • Criar programa de fidelidade para clientes < 2 anos")
print(f"   • Personalizar comunicação baseada no risco")

print(f"\n3. MONITORAMENTO:")
print(f"   • Implementar alertas automáticos para clientes em risco")
print(f"   • Acompanhar métricas de churn semanalmente")
print(f"   • Re-treinar modelo mensalmente com novos dados")

# 11. EXPORTAÇÃO DO MODELO
print("\n11. EXPORTAÇÃO DO MODELO")
print("-" * 50)

import joblib

# Salvar modelo
joblib.dump(modelo_otimizado, 'modelo_churn.pkl')
joblib.dump(preprocessor, 'preprocessor_churn.pkl')

# Salvar métricas
metricas = {
    'auc': roc_auc_score(y_test, y_pred_proba_opt),
    'f1_score': melhor_f1,
    'threshold': melhor_threshold,
    'taxa_churn_real': taxa_churn_real,
    'taxa_churn_prevista': taxa_churn_pred
}

pd.DataFrame(list(metricas.items()), columns=['Métrica', 'Valor']).to_csv('metricas_modelo.csv', index=False)

# Salvar importância das features
feature_importance_df.to_csv('feature_importance.csv', index=False)

print("Modelo e artefatos salvos:")
print("• modelo_churn.pkl")
print("• preprocessor_churn.pkl")
print("• metricas_modelo.csv")
print("• feature_importance.csv")

# 12. FUNÇÃO DE PREDIÇÃO
print("\n12. FUNÇÃO DE PREDIÇÃO")
print("-" * 50)

def prever_churn(dados_cliente):
    """
    Função para prever churn de novos clientes
    dados_cliente: DataFrame com as mesmas colunas do treino
    """
    # Carregar modelo
    modelo = joblib.load('modelo_churn.pkl')
    
    # Prever
    prob_churn = modelo.predict_proba(dados_cliente)[:, 1]
    churn_pred = (prob_churn >= melhor_threshold).astype(int)
    
    return prob_churn, churn_pred

# Exemplo de uso
exemplo_cliente = X_test.head(1)
prob, pred = prever_churn(exemplo_cliente)

print(f"Exemplo de predição:")
print(f"Probabilidade de churn: {prob[0]:.2%}")
print(f"Previsão de churn: {'Sim' if pred[0] else 'Não'}")

print("\n" + "=" * 70)
print("MACHINE LEARNING PRÁTICO 80/20 CONCLUÍDO!")
print("Você domina as técnicas essenciais para problemas reais!")
print("=" * 70)
