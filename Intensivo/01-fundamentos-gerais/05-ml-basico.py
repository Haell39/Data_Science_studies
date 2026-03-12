"""
MACHINE LEARNING BÁSICO - FUNDAMENTOS GERAIS
Os 20% mais importantes para 80% do uso em Data Science
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression, make_classification

print("=" * 60)
print("MACHINE LEARNING BÁSICO - FUNDAMENTOS")
print("=" * 60)

# 1. CONCEITOS FUNDAMENTAIS
print("\n1. CONCEITOS FUNDAMENTAIS")
print("-" * 30)

print("TIPOS DE MACHINE LEARNING:")
print("1. Aprendizado Supervisionado:")
print("   - Regressão: Prever valores contínuos (ex: preço, temperatura)")
print("   - Classificação: Prever categorias (ex: sim/não, spam/não spam)")
print("\n2. Aprendizado Não Supervisionado:")
print("   - Clustering: Agrupar dados similares")
print("   - Redução de dimensionalidade: Simplificar dados")
print("\n3. Aprendizado por Reforço:")
print("   - Agentes aprendem através de recompensas")

print("\nFLUXO DE TRABALHO EM ML:")
print("1. Coleta de dados")
print("2. Pré-processamento")
print("3. Divisão treino/teste")
print("4. Treinamento do modelo")
print("5. Avaliação")
print("6. Ajuste e deploy")

# 2. PREPARAÇÃO DE DADOS
print("\n2. PREPARAÇÃO DE DADOS")
print("-" * 30)

# Gerar dados de regressão
X_reg, y_reg = make_regression(n_samples=100, n_features=1, noise=10, random_state=42)

print(f"Dados de regressão:")
print(f"Shape de X: {X_reg.shape}")
print(f"Shape de y: {y_reg.shape}")
print(f"Primeiros 5 valores de X: {X_reg[:5].flatten()}")
print(f"Primeiros 5 valores de y: {y_reg[:5]}")

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

print(f"\nDivisão dos dados:")
print(f"Treino: {len(X_train)} amostras")
print(f"Teste: {len(X_test)} amostras")

# Normalização
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nDados normalizados:")
print(f"Média X_train: {X_train_scaled.mean():.4f}")
print(f"Desvio X_train: {X_train_scaled.std():.4f}")

# 3. REGRESSÃO LINEAR
print("\n3. REGRESSÃO LINEAR")
print("-" * 30)

# Criar e treinar modelo
modelo_reg = LinearRegression()
modelo_reg.fit(X_train_scaled, y_train)

# Previsões
y_pred_train = modelo_reg.predict(X_train_scaled)
y_pred_test = modelo_reg.predict(X_test_scaled)

# Métricas
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print("Resultados da Regressão Linear:")
print(f"Coeficiente: {modelo_reg.coef_[0]:.4f}")
print(f"Intercepto: {modelo_reg.intercept_:.4f}")
print(f"MSE Treino: {mse_train:.2f}")
print(f"MSE Teste: {mse_test:.2f}")
print(f"R² Treino: {r2_train:.4f}")
print(f"R² Teste: {r2_test:.4f}")

# Visualização
plt.figure(figsize=(12, 4))

# Gráfico de treino
plt.subplot(1, 2, 1)
plt.scatter(X_train, y_train, alpha=0.6, label='Dados reais')
plt.plot(X_train, y_pred_train, 'r-', linewidth=2, label='Previsões')
plt.title('Regressão Linear - Treino')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)

# Gráfico de teste
plt.subplot(1, 2, 2)
plt.scatter(X_test, y_test, alpha=0.6, label='Dados reais')
plt.plot(X_test, y_pred_test, 'r-', linewidth=2, label='Previsões')
plt.title('Regressão Linear - Teste')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 4. CLASSIFICAÇÃO
print("\n4. CLASSIFICAÇÃO")
print("-" * 30)

# Gerar dados de classificação
X_clf, y_clf = make_classification(n_samples=200, n_features=2, n_redundant=0, 
                                   n_informative=2, n_clusters_per_class=1, 
                                   random_state=42)

print(f"Dados de classificação:")
print(f"Shape de X: {X_clf.shape}")
print(f"Shape de y: {y_clf.shape}")
print(f"Classes únicas: {np.unique(y_clf)}")
print(f"Distribuição das classes: {np.bincount(y_clf)}")

# Divisão treino/teste
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

# Normalização
scaler_clf = StandardScaler()
X_train_clf_scaled = scaler_clf.fit_transform(X_train_clf)
X_test_clf_scaled = scaler_clf.transform(X_test_clf)

# Criar e treinar modelo
modelo_clf = LogisticRegression(random_state=42)
modelo_clf.fit(X_train_clf_scaled, y_train_clf)

# Previsões
y_pred_train_clf = modelo_clf.predict(X_train_clf_scaled)
y_pred_test_clf = modelo_clf.predict(X_test_clf_scaled)

# Métricas
acc_train = accuracy_score(y_train_clf, y_pred_train_clf)
acc_test = accuracy_score(y_test_clf, y_pred_test_clf)

print("\nResultados da Classificação:")
print(f"Acurácia Treino: {acc_train:.4f}")
print(f"Acurácia Teste: {acc_test:.4f}")

print(f"\nRelatório de Classificação (Teste):")
print(classification_report(y_test_clf, y_pred_test_clf))

# Matriz de confusão
cm = confusion_matrix(y_test_clf, y_pred_test_clf)
print(f"Matriz de Confusão:\n{cm}")

# Visualização
plt.figure(figsize=(12, 4))

# Gráfico de treino
plt.subplot(1, 2, 1)
scatter = plt.scatter(X_train_clf[:, 0], X_train_clf[:, 1], c=y_train_clf, 
                    cmap='viridis', alpha=0.6, label='Dados reais')
plt.title('Classificação - Treino')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(scatter, label='Classe')
plt.grid(True, alpha=0.3)

# Gráfico de teste
plt.subplot(1, 2, 2)
scatter = plt.scatter(X_test_clf[:, 0], X_test_clf[:, 1], c=y_pred_test_clf, 
                    cmap='viridis', alpha=0.6, label='Previsões')
plt.title('Classificação - Teste (Previsões)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(scatter, label='Classe')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 5. APLICAÇÃO PRÁTICA - PREVISÃO DE PREÇOS
print("\n5. APLICAÇÃO PRÁTICA - PREVISÃO DE PREÇOS")
print("-" * 30)

# Gerar dados simulados de imóveis
np.random.seed(42)
n_imoveis = 200

dados_imoveis = {
    'area': np.random.normal(120, 40, n_imoveis),
    'quartos': np.random.randint(1, 5, n_imoveis),
    'idade': np.random.randint(0, 30, n_imoveis),
    'localizacao': np.random.choice(['A', 'B', 'C'], n_imoveis)
}

# Preço baseado nas features
preco_base = 1000 + dados_imoveis['area'] * 50 + dados_imoveis['quartos'] * 200
preco_base -= dados_imoveis['idade'] * 30
preco_base += np.where(dados_imoveis['localizacao'] == 'A', 50000, 
                      np.where(dados_imoveis['localizacao'] == 'B', 20000, 0))

# Adicionar ruído
preco = preco_base + np.random.normal(0, 20000, n_imoveis)
preco = np.maximum(preco, 50000)  # Preço mínimo

df_imoveis = pd.DataFrame(dados_imoveis)
df_imoveis['preco'] = preco

print("Dataset de Imóveis:")
print(df_imoveis.head())
print(f"\nEstatísticas:")
print(df_imoveis.describe())

# Preparar dados
X = df_imoveis[['area', 'quartos', 'idade']]
y = df_imoveis['preco']

# One-hot encoding para localização
X = pd.get_dummies(df_imoveis[['area', 'quartos', 'idade', 'localizacao']], 
                   columns=['localizacao'], drop_first=True)

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalização
scaler_imoveis = StandardScaler()
X_train_scaled = scaler_imoveis.fit_transform(X_train)
X_test_scaled = scaler_imoveis.transform(X_test)

# Modelo
modelo_imoveis = LinearRegression()
modelo_imoveis.fit(X_train_scaled, y_train)

# Previsões
y_pred = modelo_imoveis.predict(X_test_scaled)

# Métricas
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"\nResultados do Modelo de Preços:")
print(f"RMSE: R${rmse:.2f}")
print(f"R²: {r2:.4f}")

# Visualização
plt.figure(figsize=(10, 4))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Preço Real')
plt.ylabel('Preço Previsto')
plt.title('Preços Reais vs Previstos')
plt.grid(True, alpha=0.3)
plt.show()

# 6. APLICAÇÃO PRÁTICA - CLASSIFICAÇÃO DE CLIENTES
print("\n6. APLICAÇÃO PRÁTICA - CLASSIFICAÇÃO DE CLIENTES")
print("-" * 30)

# Gerar dados de clientes
np.random.seed(42)
n_clientes = 300

dados_clientes = {
    'idade': np.random.normal(35, 10, n_clientes),
    'renda': np.random.normal(5000, 2000, n_clientes),
    'score': np.random.uniform(0, 100, n_clientes),
    'produtos': np.random.randint(1, 10, n_clientes)
}

# Ajustar dados
dados_clientes['idade'] = np.maximum(dados_clientes['idade'], 18)
dados_clientes['renda'] = np.maximum(dados_clientes['renda'], 1000)

# Classificar clientes (0: não compraria, 1: compraria)
prob_compra = (dados_clientes['renda'] / 10000 + 
              dados_clientes['score'] / 100 + 
              dados_clientes['produtos'] / 20 - 
              dados_clientes['idade'] / 100)

dados_clientes['compraria'] = (prob_compra > 0.5).astype(int)

df_clientes = pd.DataFrame(dados_clientes)

print("Dataset de Clientes:")
print(df_clientes.head())
print(f"\nDistribuição:")
print(df_clientes['compraria'].value_counts())

# Preparar dados
X = df_clientes[['idade', 'renda', 'score', 'produtos']]
y = df_clientes['compraria']

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=42, stratify=y)

# Normalização
scaler_clientes = StandardScaler()
X_train_scaled = scaler_clientes.fit_transform(X_train)
X_test_scaled = scaler_clientes.transform(X_test)

# Modelo
modelo_clientes = LogisticRegression(random_state=42)
modelo_clientes.fit(X_train_scaled, y_train)

# Previsões
y_pred = modelo_clientes.predict(X_test_scaled)
y_pred_proba = modelo_clientes.predict_proba(X_test_scaled)[:, 1]

# Métricas
accuracy = accuracy_score(y_test, y_pred)

print(f"\nResultados do Modelo de Classificação:")
print(f"Acurácia: {accuracy:.4f}")
print(f"\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

print(f"Matriz de Confusão:")
print(confusion_matrix(y_test, y_pred))

# Visualização das probabilidades
plt.figure(figsize=(10, 4))
plt.hist(y_pred_proba[y_test == 0], bins=20, alpha=0.6, label='Classe 0', color='red')
plt.hist(y_pred_proba[y_test == 1], bins=20, alpha=0.6, label='Classe 1', color='blue')
plt.xlabel('Probabilidade de Compra')
plt.ylabel('Frequência')
plt.title('Distribuição das Probabilidades Previstas')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 7. VALIDAÇÃO CRUZADA (SIMPLIFICADA)
print("\n7. VALIDAÇÃO CRUZADA")
print("-" * 30)

from sklearn.model_selection import cross_val_score

# Validação cruzada para regressão
cv_scores_reg = cross_val_score(modelo_reg, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"Validação Cruzada - Regressão (R²):")
print(f"Scores: {cv_scores_reg}")
print(f"Média: {cv_scores_reg.mean():.4f}")
print(f"Desvio: {cv_scores_reg.std():.4f}")

# Validação cruzada para classificação
cv_scores_clf = cross_val_score(modelo_clf, X_train_clf_scaled, y_train_clf, cv=5, scoring='accuracy')
print(f"\nValidação Cruzada - Classificação (Acurácia):")
print(f"Scores: {cv_scores_clf}")
print(f"Média: {cv_scores_clf.mean():.4f}")
print(f"Desvio: {cv_scores_clf.std():.4f}")

# 8. IMPORTÂNCIA DE FEATURES
print("\n8. IMPORTÂNCIA DE FEATURES")
print("-" * 30)

# Para o modelo de clientes
feature_names = ['idade', 'renda', 'score', 'produtos']
feature_importance = np.abs(modelo_clientes.coef_[0])

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print("Importância das Features (Classificação de Clientes):")
print(importance_df)

# Visualização
plt.figure(figsize=(8, 4))
plt.bar(importance_df['feature'], importance_df['importance'], color='skyblue')
plt.title('Importância das Features')
plt.xlabel('Features')
plt.ylabel('Importância (|Coeficiente|)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 9. OVERFITTING E UNDERFITTING
print("\n9. OVERFITTING E UNDERFITTING")
print("-" * 30)

print("SINAIS DE OVERFITTING:")
print("- Performance muito melhor no treino que no teste")
print("- Modelo muito complexo para poucos dados")
print("- Baixa generalização")

print("\nSINAIS DE UNDERFITTING:")
print("- Performance ruim no treino e no teste")
print("- Modelo muito simples")
print("- Alto viés (bias)")

print("\nCOMO EVITAR:")
print("- Validação cruzada")
print("- Regularização")
print("- Mais dados")
print("- Feature engineering adequado")

# 10. DESAFIO INTEGRADOR
print("\n10. DESAFIO INTEGRADOR")
print("-" * 30)

def projeto_ml_completo():
    """Projeto completo de Machine Learning do início ao fim."""
    
    print("PROJETO ML COMPLETO - PREVISÃO DE CHURN")
    print("=" * 50)
    
    # 1. Gerar dados
    np.random.seed(123)
    n_clientes = 500
    
    dados = {
        'idade': np.random.normal(38, 12, n_clientes),
        'meses_cliente': np.random.exponential(24, n_clientes),
        'saldo': np.random.normal(10000, 5000, n_clientes),
        'produtos_ativos': np.random.randint(1, 5, n_clientes),
        'tem_cartao': np.random.choice([0, 1], n_clientes, p=[0.3, 0.7]),
        'score_credito': np.random.uniform(300, 850, n_clientes)
    }
    
    # Ajustar dados
    dados['idade'] = np.maximum(dados['idade'], 18)
    dados['saldo'] = np.maximum(dados['saldo'], 0)
    dados['meses_cliente'] = np.maximum(dados['meses_cliente'], 1)
    
    # Calcular probabilidade de churn
    prob_churn = (
        -dados['idade'] / 100 +  # Mais velho = menos churn
        -dados['meses_cliente'] / 100 +  # Mais tempo = menos churn
        dados['saldo'] / 50000 +  # Alto saldo = menos churn
        -dados['produtos_ativos'] * 0.1 +  # Mais produtos = menos churn
        dados['tem_cartao'] * 0.2 +  # Tem cartão = menos churn
        (850 - dados['score_credito']) / 1000  # Score baixo = mais churn
    )
    
    # Adicionar ruído e normalizar
    prob_churn += np.random.normal(0, 0.2, n_clientes)
    prob_churn = np.clip(prob_churn, 0, 1)
    
    # Criar target
    dados['churn'] = (prob_churn > 0.3).astype(int)
    
    df = pd.DataFrame(dados)
    
    print(f"1. Dataset criado: {df.shape}")
    print(f"   Taxa de churn: {df['churn'].mean():.2%}")
    
    # 2. Análise exploratória
    print(f"\n2. Análise Exploratória:")
    print(f"   Estatísticas por churn:")
    print(df.groupby('churn').agg({
        'idade': 'mean',
        'meses_cliente': 'mean',
        'saldo': 'mean',
        'produtos_ativos': 'mean',
        'score_credito': 'mean'
    }).round(2))
    
    # 3. Preparação dos dados
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"\n3. Dados preparados:")
    print(f"   Treino: {X_train_scaled.shape}")
    print(f"   Teste: {X_test_scaled.shape}")
    
    # 4. Treinamento do modelo
    modelo = LogisticRegression(random_state=42)
    modelo.fit(X_train_scaled, y_train)
    
    # 5. Avaliação
    y_pred = modelo.predict(X_test_scaled)
    y_pred_proba = modelo.predict_proba(X_test_scaled)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n4. Modelo treinado e avaliado:")
    print(f"   Acurácia: {accuracy:.4f}")
    print(f"\n   Relatório de Classificação:")
    print(classification_report(y_test, y_pred))
    
    # 6. Importância das features
    feature_importance = np.abs(modelo.coef_[0])
    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print(f"\n5. Importância das Features:")
    print(importance_df)
    
    # 7. Visualização
    plt.figure(figsize=(12, 8))
    
    # Distribuição das probabilidades
    plt.subplot(2, 2, 1)
    plt.hist(y_pred_proba[y_test == 0], bins=20, alpha=0.6, label='Não Churn', color='green')
    plt.hist(y_pred_proba[y_test == 1], bins=20, alpha=0.6, label='Churn', color='red')
    plt.xlabel('Probabilidade de Churn')
    plt.ylabel('Frequência')
    plt.title('Distribuição de Probabilidades')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Importância das features
    plt.subplot(2, 2, 2)
    plt.barh(importance_df['feature'], importance_df['importance'], color='skyblue')
    plt.title('Importância das Features')
    plt.xlabel('Importância')
    plt.grid(True, alpha=0.3, axis='x')
    
    # Matriz de confusão
    plt.subplot(2, 2, 3)
    cm = confusion_matrix(y_test, y_pred)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Matriz de Confusão')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Não Churn', 'Churn'])
    plt.yticks(tick_marks, ['Não Churn', 'Churn'])
    plt.xlabel('Previsto')
    plt.ylabel('Real')
    
    # Adicionar números
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black")
    
    # Score vs Churn
    plt.subplot(2, 2, 4)
    plt.scatter(df['score_credito'], df['churn'] + np.random.normal(0, 0.05, len(df)), 
               alpha=0.3, c=df['churn'], cmap='viridis')
    plt.xlabel('Score de Crédito')
    plt.ylabel('Churn')
    plt.title('Score de Crédito vs Churn')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 8. Validação cruzada
    cv_scores = cross_val_score(modelo, X_train_scaled, y_train, cv=5, scoring='accuracy')
    print(f"\n6. Validação Cruzada:")
    print(f"   Scores: {cv_scores}")
    print(f"   Média: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    print(f"\nPROJETO CONCLUÍDO COM SUCESSO!")
    
    return modelo, scaler, importance_df

# Executar desafio
modelo_final, scaler_final, importancia_final = projeto_ml_completo()

print("\n" + "=" * 60)
print("MACHINE LEARNING BÁSICO CONCLUÍDO!")
print("Você domina os 20% mais importantes!")
print("=" * 60)
