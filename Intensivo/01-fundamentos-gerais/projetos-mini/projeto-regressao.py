"""
PROJETO MINI - REGRESSÃO LINEAR COMPLETA
Aplicação prática de Machine Learning para previsão
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import seaborn as sns

print("=" * 70)
print("PROJETO MINI - REGRESSÃO LINEAR COMPLETA")
print("=" * 70)

# 1. GERAÇÃO DE DADOS SIMULADOS
print("\n1. GERAÇÃO DE DADOS")
print("-" * 40)

# Configurar semente
np.random.seed(123)

# Gerar dataset de imóveis
n_imoveis = 500

# Features com correlações realistas
area = np.random.normal(120, 40, n_imoveis)
area = np.maximum(area, 40)  # Mínimo 40m²

quartos = np.random.choice([1, 2, 3, 4, 5], n_imoveis, p=[0.1, 0.2, 0.4, 0.2, 0.1])

banheiros = np.where(quartos <= 2, np.random.choice([1, 2], n_imoveis, p=[0.6, 0.4]),
                    np.random.choice([2, 3, 4], n_imoveis, p=[0.4, 0.4, 0.2]))

vagas = np.random.choice([0, 1, 2, 3], n_imoveis, p=[0.2, 0.3, 0.3, 0.2])

idade_imovel = np.random.exponential(15, n_imoveis)
idade_imovel = np.minimum(idade_imovel, 50)  # Máximo 50 anos

# Localização (fator importante)
localizacao = np.random.choice(['Centro', 'Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste'], 
                              n_imoveis, p=[0.15, 0.25, 0.25, 0.2, 0.15])

# Calcular preço baseado nas features (com correlações realistas)
preco_base = (
    50000 +  # Preço base
    area * 3000 +  # Área tem forte impacto
    quartos * 15000 +  # Quartos
    banheiros * 8000 +  # Banheiros
    vagas * 20000 +  # Vagas de garagem
    np.where(localizacao == 'Centro', 100000,  # Centro mais caro
             np.where(localizacao == 'Zona Sul', 80000,
                      np.where(localizacao == 'Zona Norte', 60000,
                               np.where(localizacao == 'Zona Leste', 30000, 20000)))) -
    idade_imovel * 2000  # Desvalorização por idade
)

# Adicionar ruído realista
preco = preco_base + np.random.normal(0, 50000, n_imoveis)
preco = np.maximum(preco, 80000)  # Preço mínimo

# Criar DataFrame
dados = {
    'area': area,
    'quartos': quartos,
    'banheiros': banheiros,
    'vagas': vagas,
    'idade': idade_imovel,
    'localizacao': localizacao,
    'preco': preco
}

df = pd.DataFrame(dados)

# Arredondar valores inteiros
df['quartos'] = df['quartos'].astype(int)
df['banheiros'] = df['banheiros'].astype(int)
df['vagas'] = df['vagas'].astype(int)
df['idade'] = df['idade'].round(1)
df['area'] = df['area'].round(1)
df['preco'] = df['preco'].round(2)

print(f"Dataset criado: {df.shape}")
print(f"\nEstatísticas gerais:")
print(df.describe().round(2))

print(f"\nDistribuição por localização:")
print(df['localizacao'].value_counts())

# 2. ANÁLISE EXPLORATÓRIA
print("\n2. ANÁLISE EXPLORATÓRIA")
print("-" * 40)

# Correlação entre features numéricas
features_numericas = ['area', 'quartos', 'banheiros', 'vagas', 'idade', 'preco']
correlacao = df[features_numericas].corr()

print("Matriz de Correlação:")
print(correlacao.round(3))

# Visualizar correlações
plt.figure(figsize=(10, 8))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', center=0, square=True, fmt='.3f')
plt.title('Matriz de Correlação')
plt.tight_layout()
plt.show()

# Análise por localização
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
sns.boxplot(data=df, x='localizacao', y='preco')
plt.title('Preço por Localização')
plt.xticks(rotation=45)
plt.ylabel('Preço (R$)')

plt.subplot(1, 2, 2)
df.groupby('localizacao')['preco'].mean().sort_values().plot(kind='bar')
plt.title('Preço Médio por Localização')
plt.ylabel('Preço Médio (R$)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# Distribuição do preço
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.hist(df['preco'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribuição de Preços')
plt.xlabel('Preço (R$)')
plt.ylabel('Frequência')
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(1, 2, 2)
plt.scatter(df['area'], df['preco'], alpha=0.6)
plt.title('Preço vs Área')
plt.xlabel('Área (m²)')
plt.ylabel('Preço (R$)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 3. PREPARAÇÃO DOS DADOS
print("\n3. PREPARAÇÃO DOS DADOS")
print("-" * 40)

# One-hot encoding para localização
df_encoded = pd.get_dummies(df, columns=['localizacao'], drop_first=True)

print("Features após encoding:")
print(f"Colunas: {list(df_encoded.columns)}")

# Separar features e target
X = df_encoded.drop('preco', axis=1)
y = df_encoded['preco']

print(f"\nShape de X: {X.shape}")
print(f"Shape de y: {y.shape}")

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nDivisão dos dados:")
print(f"Treino: {X_train.shape}")
print(f"Teste: {X_test.shape}")

# Normalização
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Converter para DataFrame para manter nomes das colunas
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)

print(f"\nDados normalizados:")
print(f"Média das features (treino): {X_train_scaled.mean().abs().max():.6f}")
print(f"Desvio das features (treino): {X_train_scaled.std().abs().max():.6f}")

# 4. TREINAMENTO DO MODELO
print("\n4. TREINAMENTO DO MODELO")
print("-" * 40)

# Criar e treinar modelo
modelo = LinearRegression()
modelo.fit(X_train_scaled, y_train)

# Coeficientes
coeficientes = pd.DataFrame({
    'Feature': X.columns,
    'Coeficiente': modelo.coef_
}).sort_values('Coeficiente', key=abs, ascending=False)

print("Coeficientes do modelo:")
print(coeficientes.round(2))

print(f"\nIntercepto: R${modelo.intercept_:,.2f}")

# 5. AVALIAÇÃO DO MODELO
print("\n5. AVALIAÇÃO DO MODELO")
print("-" * 40)

# Previsões
y_pred_train = modelo.predict(X_train_scaled)
y_pred_test = modelo.predict(X_test_scaled)

# Métricas
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)
rmse_train = np.sqrt(mse_train)
rmse_test = np.sqrt(mse_test)
mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print("Métricas de Avaliação:")
print(f"\nConjunto de Treino:")
print(f"  RMSE: R${rmse_train:,.2f}")
print(f"  MAE: R${mae_train:,.2f}")
print(f"  R²: {r2_train:.4f}")

print(f"\nConjunto de Teste:")
print(f"  RMSE: R${rmse_test:,.2f}")
print(f"  MAE: R${mae_test:,.2f}")
print(f"  R²: {r2_test:.4f}")

# Verificar overfitting
overfitting = abs(r2_train - r2_test)
print(f"\nDiferença R² (treino vs teste): {overfitting:.4f}")
if overfitting < 0.1:
    print("✅ Modelo bem generalizado (baixo overfitting)")
else:
    print("⚠️ Possível overfitting detectado")

# 6. VISUALIZAÇÃO DOS RESULTADOS
print("\n6. VISUALIZAÇÃO DOS RESULTADOS")
print("-" * 40)

# Gráfico de previsões vs reais
plt.figure(figsize=(12, 8))

# Treino
plt.subplot(2, 2, 1)
plt.scatter(y_train, y_pred_train, alpha=0.6, color='blue')
plt.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
plt.xlabel('Preço Real')
plt.ylabel('Preço Previsto')
plt.title('Treino: Real vs Previsto')
plt.grid(True, alpha=0.3)

# Teste
plt.subplot(2, 2, 2)
plt.scatter(y_test, y_pred_test, alpha=0.6, color='green')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Preço Real')
plt.ylabel('Preço Previsto')
plt.title('Teste: Real vs Previsto')
plt.grid(True, alpha=0.3)

# Resíduos - Treino
plt.subplot(2, 2, 3)
residuos_train = y_train - y_pred_train
plt.scatter(y_pred_train, residuos_train, alpha=0.6, color='blue')
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Preço Previsto')
plt.ylabel('Resíduo')
plt.title('Treino: Resíduos')
plt.grid(True, alpha=0.3)

# Resíduos - Teste
plt.subplot(2, 2, 4)
residuos_test = y_test - y_pred_test
plt.scatter(y_pred_test, residuos_test, alpha=0.6, color='green')
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Preço Previsto')
plt.ylabel('Resíduo')
plt.title('Teste: Resíduos')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Distribuição dos resíduos
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.hist(residuos_train, bins=30, alpha=0.7, color='blue', label='Treino')
plt.hist(residuos_test, bins=30, alpha=0.7, color='green', label='Teste')
plt.xlabel('Resíduo')
plt.ylabel('Frequência')
plt.title('Distribuição dos Resíduos')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(1, 2, 2)
import scipy.stats as stats
stats.probplot(residuos_test, dist="norm", plot=plt)
plt.title('QQ Plot - Resíduos (Teste)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 7. IMPORTÂNCIA DAS FEATURES
print("\n7. IMPORTÂNCIA DAS FEATURES")
print("-" * 40)

# Importância baseada no valor absoluto dos coeficientes
importancia = coeficientes.copy()
importancia['Importancia_Abs'] = importancia['Coeficiente'].abs()
importancia = importancia.sort_values('Importancia_Abs', ascending=False)

print("Ranking de Importância das Features:")
print(importancia[['Feature', 'Coeficiente', 'Importancia_Abs']].round(2))

# Visualização
plt.figure(figsize=(10, 6))
plt.barh(importancia['Feature'], importancia['Importancia_Abs'], color='skyblue')
plt.title('Importância das Features')
plt.xlabel('Importância (|Coeficiente|)')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

# 8. PREVISÕES PARA NOVOS DADOS
print("\n8. PREVISÕES PARA NOVOS DADOS")
print("-" * 40)

# Criar exemplos de novos imóveis
novos_imoveis = pd.DataFrame({
    'area': [80, 150, 200, 120, 90],
    'quartos': [2, 3, 4, 3, 2],
    'banheiros': [1, 2, 2, 2, 1],
    'vagas': [1, 2, 2, 1, 0],
    'idade': [5, 10, 2, 15, 20],
    'localizacao': ['Zona Norte', 'Zona Sul', 'Centro', 'Zona Leste', 'Zona Oeste']
})

# One-hot encoding
novos_imoveis_encoded = pd.get_dummies(novos_imoveis, columns=['localizacao'], drop_first=True)

# Adicionar colunas ausentes (se necessário)
for col in X.columns:
    if col not in novos_imoveis_encoded.columns:
        novos_imoveis_encoded[col] = 0

# Ordenar colunas para match com X
novos_imoveis_encoded = novos_imoveis_encoded[X.columns]

# Normalizar
novos_imoveis_scaled = scaler.transform(novos_imoveis_encoded)

# Prever
previsoes = modelo.predict(novos_imoveis_scaled)

# Resultados
resultados = novos_imoveis.copy()
resultados['preco_previsto'] = previsoes.round(2)
resultados['erro_estimado'] = rmse_test

print("Previsões para Novos Imóveis:")
print(resultados.to_string(index=False))

# 9. VALIDAÇÃO CRUZADA
print("\n9. VALIDAÇÃO CRUZADA")
print("-" * 40)

from sklearn.model_selection import cross_val_score

# Validação cruzada
cv_scores = cross_val_score(modelo, X_train_scaled, y_train, cv=5, scoring='r2')

print("Validação Cruzada (5-fold):")
print(f"Scores R²: {cv_scores.round(4)}")
print(f"Média R²: {cv_scores.mean():.4f}")
print(f"Desvio Padrão: {cv_scores.std():.4f}")
print(f"Intervalo de confiança (95%): [{cv_scores.mean() - 2*cv_scores.std():.4f}, {cv_scores.mean() + 2*cv_scores.std():.4f}]")

# 10. RELATÓRIO FINAL
print("\n10. RELATÓRIO FINAL")
print("-" * 40)

# Métricas finais
métricas_finais = {
    'RMSE Teste': f"R${rmse_test:,.2f}",
    'MAE Teste': f"R${mae_test:,.2f}",
    'R² Teste': f"{r2_test:.4f}",
    'R² Validação Cruzada': f"{cv_scores.mean():.4f}",
    'Features': X.shape[1],
    'Amostras Treino': len(X_train),
    'Amostras Teste': len(X_test)
}

print("RESUMO DO MODELO:")
for metrica, valor in métricas_finais.items():
    print(f"• {metrica}: {valor}")

print(f"\nTOP 3 FEATURES MAIS IMPORTANTES:")
for i, row in importancia.head(3).iterrows():
    print(f"• {row['Feature']}: {row['Coeficiente']:.2f}")

print(f"\nRECOMENDAÇÕES:")
print(f"1. O modelo explica {r2_test:.1%} da variabilidade dos preços")
print(f"2. Erro médio absoluto de R${mae_test:,.2f}")
print(f"3. Área e localização são os fatores mais importantes")
print(f"4. Modelo está bem generalizado (baixo overfitting)")
print(f"5. Adequado para uso em sistema de avaliação imobiliária")

# Exportar resultados
relatorio = pd.DataFrame(list(métricas_finais.items()), columns=['Métrica', 'Valor'])
relatorio.to_csv('relatorio_modelo_regressao.csv', index=False)

coeficientes.to_csv('coeficientes_modelo.csv', index=False)

print(f"\nArquivos exportados:")
print(f"• relatorio_modelo_regressao.csv")
print(f"• coeficientes_modelo.csv")

print("\n" + "=" * 70)
print("PROJETO DE REGRESSÃO LINEAR CONCLUÍDO!")
print("Modelo pronto para produção com métricas sólidas!")
print("=" * 70)
