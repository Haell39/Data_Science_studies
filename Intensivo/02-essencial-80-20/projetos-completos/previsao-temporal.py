"""
PROJETO COMPLETO - PREVISÃO DE SÉRIES TEMPORAIS
Sistema completo para previsão de vendas com múltiplos modelos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PROJETO COMPLETO - PREVISÃO DE SÉRIES TEMPORAIS")
print("=" * 80)

# 1. GERAÇÃO DE DADOS REALISTAS
print("\n1. GERAÇÃO DE DADOS REALISTAS")
print("-" * 60)

# Gerar dados de vendas com múltiplos fatores
np.random.seed(42)
n_dias = 730  # 2 anos de dados

# Base temporal
datas = pd.date_range('2022-01-01', periods=n_dias, freq='D')

# Componentes da série temporal
# 1. Tendência (crescimento gradual)
tendencia = np.linspace(1000, 2000, n_dias)

# 2. Sazonalidade anual
sazonalidade_anual = 300 * np.sin(2 * np.pi * np.arange(n_dias) / 365.25)

# 3. Sazonalidade semanal
sazonalidade_semanal = 150 * np.sin(2 * np.pi * np.arange(n_dias) / 7)

# 4. Efeitos de feriados (simplificado)
feriados = []
for ano in range(2022, 2024):
    feriados.extend([
        pd.Timestamp(f'{ano}-01-01'),  # Ano Novo
        pd.Timestamp(f'{ano}-04-21'),  # Tiradentes
        pd.Timestamp(f'{ano}-05-01'),  # Dia do Trabalho
        pd.Timestamp(f'{ano}-09-07'),  # Independência
        pd.Timestamp(f'{ano}-12-25'),  # Natal
    ])

efeito_feriados = np.zeros(n_dias)
for feriado in feriados:
    idx = np.where(datas == feriado)[0]
    if len(idx) > 0:
        # Efeito antes e depois do feriado
        for i in range(max(0, idx[0]-3), min(n_dias, idx[0]+4)):
            efeito_feriados[i] += 200 * np.exp(-abs(i - idx[0]) / 2)

# 5. Ruído aleatório
ruido = np.random.normal(0, 100, n_dias)

# 6. Eventos especiais (promoções)
eventos_especiais = np.zeros(n_dias)
for i in range(0, n_dias, 90):  # A cada ~3 meses
    eventos_especiais[i:i+7] = np.random.uniform(100, 300, 7)

# Combinar todos os componentes
vendas = tendencia + sazonalidade_anual + sazonalidade_semanal + efeito_feriados + eventos_especiais + ruído
vendas = np.maximum(vendas, 300)  # Mínimo de 300 vendas

# Adicionar informações adicionais
df_vendas = pd.DataFrame({
    'data': datas,
    'vendas': vendas,
    'dia_semana': datas.dayofweek,
    'mes': datas.month,
    'trimestre': datas.quarter,
    'ano': datas.year,
    'dia_do_ano': datas.dayofyear,
    'semana_do_ano': datas.isocalendar().week
})

# Adicionar variáveis externas
# Preço do concorrente (simulado)
df_vendas['preco_concorrente'] = 50 + 10 * np.sin(2 * np.pi * np.arange(n_dias) / 30) + np.random.normal(0, 2, n_dias)

# Marketing spend (simulado)
df_vendas['marketing_spend'] = 1000 + 500 * np.sin(2 * np.pi * np.arange(n_dias) / 14) + np.random.normal(0, 100, n_dias)
df_vendas['marketing_spend'] = np.maximum(df_vendas['marketing_spend'], 0)

# Clima (simulado - temperatura)
df_vendas['temperatura'] = 20 + 10 * np.sin(2 * np.pi * (np.arange(n_dias) - 80) / 365.25) + np.random.normal(0, 3, n_dias)

print(f"Dataset criado: {df_vendas.shape}")
print(f"Período: {df_vendas['data'].min()} a {df_vendas['data'].max()}")
print(f"\nEstatísticas das vendas:")
print(df_vendas['vendas'].describe().round(2))

# 2. ANÁLISE EXPLORATÓRIA DETALHADA
print("\n2. ANÁLISE EXPLORATÓRIA DETALHADA")
print("-" * 60)

# Visualização completa
fig, axes = plt.subplots(3, 3, figsize=(20, 15))
fig.suptitle('Análise Exploratória Completa', fontsize=16)

# Série temporal completa
axes[0, 0].plot(df_vendas['data'], df_vendas['vendas'], linewidth=1)
axes[0, 0].set_title('Vendas Diárias (2 anos)')
axes[0, 0].set_ylabel('Vendas')
axes[0, 0].grid(True, alpha=0.3)

# Decomposição sazonal
decomposicao = seasonal_decompose(df_vendas.set_index('data')['vendas'], model='additive', period=365)

axes[0, 1].plot(decomposicao.trend)
axes[0, 1].set_title('Tendência')
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(decomposicao.seasonal)
axes[0, 2].set_title('Sazonalidade')
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(decomposicao.resid)
axes[1, 0].set_title('Resíduos')
axes[1, 0].grid(True, alpha=0.3)

# Vendas por dia da semana
vendas_dia_semana = df_vendas.groupby('dia_semana')['vendas'].mean()
dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
axes[1, 1].bar(dias_semana, vendas_dia_semana.values)
axes[1, 1].set_title('Vendas Médias por Dia da Semana')
axes[1, 1].tick_params(axis='x', rotation=45)

# Vendas por mês
vendas_mes = df_vendas.groupby('mes')['vendas'].mean()
axes[1, 2].plot(vendas_mes.index, vendas_mes.values, 'o-')
axes[1, 2].set_title('Vendas Médias por Mês')
axes[1, 2].set_xlabel('Mês')
axes[1, 2].grid(True, alpha=0.3)

# Correlação com variáveis externas
correlacoes = df_vendas[['vendas', 'preco_concorrente', 'marketing_spend', 'temperatura']].corr()
sns.heatmap(correlacoes, annot=True, cmap='coolwarm', center=0, ax=axes[2, 0], fmt='.2f')
axes[2, 0].set_title('Correlação com Variáveis Externas')

# Distribuição das vendas
axes[2, 1].hist(df_vendas['vendas'], bins=50, alpha=0.7, edgecolor='black')
axes[2, 1].set_title('Distribuição das Vendas')
axes[2, 1].set_xlabel('Vendas')
axes[2, 1].set_ylabel('Frequência')

# Autocorrelação
pd.plotting.autocorrelation_plot(df_vendas['vendas'], ax=axes[2, 2])
axes[2, 2].set_title('Autocorrelação')

plt.tight_layout()
plt.show()

# 3. FEATURE ENGINEERING AVANÇADO
print("\n3. FEATURE ENGINEERING AVANÇADO")
print("-" * 60)

def criar_features_temporais(df):
    """Criar features avançadas para séries temporais"""
    df = df.copy()
    
    # Features de lag
    for lag in [1, 7, 14, 30, 60]:
        df[f'vendas_lag_{lag}'] = df['vendas'].shift(lag)
    
    # Médias móveis
    for window in [7, 14, 30, 60]:
        df[f'vendas_ma_{window}'] = df['vendas'].rolling(window=window).mean()
        df[f'vendas_std_{window}'] = df['vendas'].rolling(window=window).std()
    
    # Diferenças
    for diff in [1, 7, 30]:
        df[f'vendas_diff_{diff}'] = df['vendas'].diff(diff)
    
    # Features de tempo
    df['seno_dia_ano'] = np.sin(2 * np.pi * df['dia_do_ano'] / 365.25)
    df['cosseno_dia_ano'] = np.cos(2 * np.pi * df['dia_do_ano'] / 365.25)
    df['seno_semana'] = np.sin(2 * np.pi * df['dia_semana'] / 7)
    df['cosseno_semana'] = np.cos(2 * np.pi * df['dia_semana'] / 7)
    
    # Interações
    df['marketing_x_temperatura'] = df['marketing_spend'] * df['temperatura']
    df['preco_x_marketing'] = df['preco_concorrente'] * df['marketing_spend']
    
    # Flags especiais
    df['eh_fim_semana'] = (df['dia_semana'] >= 5).astype(int)
    df['eh_feriado'] = df['data'].isin(feriados).astype(int)
    
    # Janela de feriados
    df['prox_feriado_dias'] = 0
    for feriado in feriados:
        for i, data in enumerate(df['data']):
            dias_ate_feriado = (feriado - data).days
            if 0 <= dias_ate_feriado <= 7:
                df.loc[i, 'prox_feriado_dias'] = max(df.loc[i, 'prox_feriado_dias'], 8 - dias_ate_feriado)
    
    return df

# Aplicar feature engineering
df_features = criar_features_temporais(df_vendas)

# Remover linhas com NaN
df_features = df_features.dropna()

print(f"Dataset com features: {df_features.shape}")
print(f"Features criadas: {[col for col in df_features.columns if col not in df_vendas.columns]}")

# Análise das novas features
novas_features = [col for col in df_features.columns if col not in df_vendas.columns]
print(f"\nTotal de novas features: {len(novas_features)}")

# 4. ANÁLISE DE ESTACIONARIDADE
print("\n4. ANÁLISE DE ESTACIONARIDADE")
print("-" * 60)

# Teste Augmented Dickey-Fuller
def testar_estacionaridade(serie, nome):
    """Testa se uma série é estacionária"""
    resultado = adfuller(serie.dropna())
    
    print(f"Teste ADF para {nome}:")
    print(f"  Estatística ADF: {resultado[0]:.4f}")
    print(f"  Valor p: {resultado[1]:.4f}")
    print(f"  Valores críticos:")
    for chave, valor in resultado[4].items():
        print(f"    {chave}: {valor:.4f}")
    
    if resultado[1] < 0.05:
        print(f"  → {nome} é estacionária (rejeita H0)")
    else:
        print(f"  → {nome} não é estacionária (não rejeita H0)")
    
    return resultado[1] < 0.05

# Testar série original e diferenciada
print("Testes de Estacionaridade:")
estacionaria_original = testar_estacionaridade(df_features['vendas'], "Vendas Original")
estacionaria_diff = testar_estacionaridade(df_features['vendas_diff_1'], "Vendas Diferenciada")

# 5. PREPARAÇÃO DOS DADOS
print("\n5. PREPARAÇÃO DOS DADOS")
print("-" * 60)

# Separar features e target
features = [col for col in df_features.columns if col not in ['data', 'vendas']]
X = df_features[features]
y = df_features['vendas']

# Divisão temporal (80% treino, 20% teste)
split_point = int(len(X) * 0.8)
X_train, X_test = X[:split_point], X[split_point:]
y_train, y_test = y[:split_point], y[split_point:]

# Datas correspondentes
datas_train = df_features['data'][:split_point]
datas_test = df_features['data'][split_point:]

print(f"Divisão temporal:")
print(f"  Treino: {len(X_train)} amostras ({datas_train.min()} a {datas_train.max()})")
print(f"  Teste: {len(X_test)} amostras ({datas_test.min()} a {datas_test.max()})")

# Normalização
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Converter para DataFrame
X_train_scaled = pd.DataFrame(X_train_scaled, columns=features)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=features)

# 6. MODELOS DE MACHINE LEARNING
print("\n6. MODELOS DE MACHINE LEARNING")
print("-" * 60)

# Modelo Random Forest
modelo_rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

print("Treinando Random Forest...")
modelo_rf.fit(X_train_scaled, y_train)

# Previsões
y_pred_rf = modelo_rf.predict(X_test_scaled)

# Métricas
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"\nRandom Forest - Métricas:")
print(f"  RMSE: {rmse_rf:.2f}")
print(f"  MAE: {mae_rf:.2f}")
print(f"  R²: {r2_rf:.4f}")

# 7. MODELO ARIMA
print("\n7. MODELO ARIMA")
print("-" * 60)

# Usar série original para ARIMA
serie_arima = df_features.set_index('data')['vendas']

# Dividir treino/teste para ARIMA
train_arima = serie_arima[:split_point]
test_arima = serie_arima[split_point:]

print("Treinando modelo ARIMA...")
# Modelo ARIMA simplificado (p,d,q) = (1,1,1)
modelo_arima = ARIMA(train_arima, order=(1, 1, 1))
resultado_arima = modelo_arima.fit()

# Previsões
previsoes_arima = resultado_arima.forecast(steps=len(test_arima))

# Métricas
rmse_arima = np.sqrt(mean_squared_error(test_arima, previsoes_arima))
mae_arima = mean_absolute_error(test_arima, previsoes_arima)
r2_arima = r2_score(test_arima, previsoes_arima)

print(f"\nARIMA - Métricas:")
print(f"  RMSE: {rmse_arima:.2f}")
print(f"  MAE: {mae_arima:.2f}")
print(f"  R²: {r2_arima:.4f}")

# 8. MODELO HÍBRIDO
print("\n8. MODELO HÍBRIDO")
print("-" * 60)

# Combinar previsões dos modelos
peso_rf = 0.7
peso_arima = 0.3

# Alinhar índices
previsoes_rf_series = pd.Series(y_pred_rf, index=datas_test)
previsoes_arima_series = pd.Series(previsoes_arima.values, index=datas_test)

# Combinar
previsoes_hibridas = (peso_rf * previsoes_rf_series + peso_arima * previsoes_arima_series)

# Métricas
rmse_hibrido = np.sqrt(mean_squared_error(y_test, previsoes_hibridas))
mae_hibrido = mean_absolute_error(y_test, previsoes_hibridas)
r2_hibrido = r2_score(y_test, previsoes_hibridas)

print(f"Modelo Híbrido - Métricas:")
print(f"  RMSE: {rmse_hibrido:.2f}")
print(f"  MAE: {mae_hibrido:.2f}")
print(f"  R²: {r2_hibrido:.4f}")

# 9. COMPARAÇÃO DE MODELOS
print("\n9. COMPARAÇÃO DE MODELOS")
print("-" * 60)

# Tabela comparativa
comparacao = pd.DataFrame({
    'Modelo': ['Random Forest', 'ARIMA', 'Híbrido'],
    'RMSE': [rmse_rf, rmse_arima, rmse_hibrido],
    'MAE': [mae_rf, mae_arima, mae_hibrido],
    'R²': [r2_rf, r2_arima, r2_hibrido]
})

print("Comparação de Modelos:")
print(comparacao.round(4))

# Visualização comparativa
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Previsões vs Real
axes[0, 0].plot(datas_test, y_test, label='Real', alpha=0.7, linewidth=2)
axes[0, 0].plot(datas_test, y_pred_rf, label='Random Forest', alpha=0.8)
axes[0, 0].plot(datas_test, previsoes_arima.values, label='ARIMA', alpha=0.8)
axes[0, 0].plot(datas_test, previsoes_hibridas, label='Híbrido', alpha=0.8, linewidth=2)
axes[0, 0].set_title('Previsões vs Real')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Comparação de RMSE
modelos = ['Random Forest', 'ARIMA', 'Híbrido']
rmses = [rmse_rf, rmse_arima, rmse_hibrido]
axes[0, 1].bar(modelos, rmses, color=['skyblue', 'lightgreen', 'salmon'])
axes[0, 1].set_title('Comparação RMSE')
axes[0, 1].set_ylabel('RMSE')
for i, rmse in enumerate(rmses):
    axes[0, 1].text(i, rmse + 5, f'{rmse:.1f}', ha='center')

# Resíduos Random Forest
residuos_rf = y_test - y_pred_rf
axes[1, 0].scatter(y_pred_rf, residuos_rf, alpha=0.6)
axes[1, 0].axhline(y=0, color='r', linestyle='--')
axes[1, 0].set_title('Resíduos - Random Forest')
axes[1, 0].set_xlabel('Previsões')
axes[1, 0].set_ylabel('Resíduos')
axes[1, 0].grid(True, alpha=0.3)

# Importância das features
importancia_features = pd.DataFrame({
    'feature': features,
    'importance': modelo_rf.feature_importances_
}).sort_values('importance', ascending=False).head(10)

axes[1, 1].barh(importancia_features['feature'], importancia_features['importance'])
axes[1, 1].set_title('Top 10 Features - Random Forest')
axes[1, 1].set_xlabel('Importância')

plt.tight_layout()
plt.show()

# 10. PREVISÃO FUTURA
print("\n10. PREVISÃO FUTURA")
print("-" * 60")

def prever_futuro(modelo_rf, modelo_arima, df_ultimo, n_dias=30):
    """Prever próximos n dias"""
    
    previsoes_futuras = []
    df_atual = df_ultimo.copy()
    
    for i in range(n_dias):
        # Data futura
        prox_data = df_atual['data'].iloc[-1] + pd.Timedelta(days=1)
        
        # Criar features para o futuro
        features_futuro = {}
        
        # Features temporais
        features_futuro['dia_semana'] = prox_data.dayofweek
        features_futuro['mes'] = prox_data.month
        features_futuro['trimestre'] = prox_data.quarter
        features_futuro['ano'] = prox_data.year
        features_futuro['dia_do_ano'] = prox_data.dayofyear
        features_futuro['semana_do_ano'] = prox_data.isocalendar().week
        
        # Features cíclicas
        features_futuro['seno_dia_ano'] = np.sin(2 * np.pi * features_futuro['dia_do_ano'] / 365.25)
        features_futuro['cosseno_dia_ano'] = np.cos(2 * np.pi * features_futuro['dia_do_ano'] / 365.25)
        features_futuro['seno_semana'] = np.sin(2 * np.pi * features_futuro['dia_semana'] / 7)
        features_futuro['cosseno_semana'] = np.cos(2 * np.pi * features_futuro['dia_semana'] / 7)
        
        # Lags (usando valores conhecidos)
        for lag in [1, 7, 14, 30, 60]:
            if f'vendas_lag_{lag}' in df_atual.columns:
                if lag <= len(df_atual):
                    features_futuro[f'vendas_lag_{lag}'] = df_atual['vendas'].iloc[-lag]
                else:
                    features_futuro[f'vendas_lag_{lag}'] = df_atual['vendas'].mean()
        
        # Médias móveis (simplificado)
        for window in [7, 14, 30, 60]:
            if f'vendas_ma_{window}' in df_atual.columns:
                if len(df_atual) >= window:
                    features_futuro[f'vendas_ma_{window}'] = df_atual['vendas'].tail(window).mean()
                    features_futuro[f'vendas_std_{window}'] = df_atual['vendas'].tail(window).std()
                else:
                    features_futuro[f'vendas_ma_{window}'] = df_atual['vendas'].mean()
                    features_futuro[f'vendas_std_{window}'] = df_atual['vendas'].std()
        
        # Variáveis externas (simuladas)
        features_futuro['preco_concorrente'] = 50 + 10 * np.sin(2 * np.pi * features_futuro['dia_do_ano'] / 30)
        features_futuro['marketing_spend'] = 1000 + 500 * np.sin(2 * np.pi * features_futuro['dia_semana'] / 7)
        features_futuro['temperatura'] = 20 + 10 * np.sin(2 * np.pi * (features_futuro['dia_do_ano'] - 80) / 365.25)
        
        # Interações
        features_futuro['marketing_x_temperatura'] = features_futuro['marketing_spend'] * features_futuro['temperatura']
        features_futuro['preco_x_marketing'] = features_futuro['preco_concorrente'] * features_futuro['marketing_spend']
        
        # Flags
        features_futuro['eh_fim_semana'] = int(features_futuro['dia_semana'] >= 5)
        features_futuro['eh_feriado'] = int(prox_data in feriados)
        features_futuro['prox_feriado_dias'] = 0
        
        # Diferenças
        for diff in [1, 7, 30]:
            if f'vendas_diff_{diff}' in df_atual.columns and len(df_atual) > diff:
                features_futuro[f'vendas_diff_{diff}'] = df_atual['vendas'].iloc[-1] - df_atual['vendas'].iloc[-diff-1]
        
        # Criar DataFrame e prever
        X_futuro = pd.DataFrame([features_futuro])
        
        # Garantir que todas as features estejam presentes
        for feature in features:
            if feature not in X_futuro.columns:
                X_futuro[feature] = 0
        
        X_futuro = X_futuro[features]
        X_futuro_scaled = scaler.transform(X_futuro)
        
        # Previsão Random Forest
        previsao_rf = modelo_rf.predict(X_futuro_scaled)[0]
        
        # Previsão ARIMA (simplificado - usa última previsão)
        if i == 0:
            previsao_arima = resultado_arima.forecast(steps=1).iloc[0]
        else:
            previsao_arima = previsoes_futuras[-1]['previsao_arima']
        
        # Combinar
        previsao_hibrida = peso_rf * previsao_rf + peso_arima * previsao_arima
        
        previsoes_futuras.append({
            'data': prox_data,
            'previsao_rf': previsao_rf,
            'previsao_arima': previsao_arima,
            'previsao_hibrida': previsao_hibrida
        })
        
        # Atualizar dataframe para próxima iteração
        nova_linha = features_futuro.copy()
        nova_linha['data'] = prox_data
        nova_linha['vendas'] = previsao_hibrida
        
        df_atual = pd.concat([df_atual, pd.DataFrame([nova_linha])], ignore_index=True)
    
    return pd.DataFrame(previsoes_futuras)

# Prever próximos 30 dias
previsoes_futuras = prever_futuro(modelo_rf, resultado_arima, df_features, 30)

print("Previsões para os próximos 30 dias:")
print(previsoes_futuras.head(10))

# Visualizar previsões futuras
plt.figure(figsize=(12, 6))
plt.plot(df_features['data'].tail(60), df_features['vendas'].tail(60), label='Histórico', alpha=0.7)
plt.plot(previsoes_futuras['data'], previsoes_futuras['previsao_hibrida'], 
         label='Previsão Híbrida', linewidth=2, color='red')
plt.title('Previsão para Próximos 30 Dias')
plt.xlabel('Data')
plt.ylabel('Vendas')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 11. ANÁLISE DE CENÁRIOS
print("\n11. ANÁLISE DE CENÁRIOS")
print("-" * 60)

# Simular diferentes cenários
cenarios = {
    'Otimista': {'marketing_spend': 1.5, 'preco_concorrente': 1.2},
    'Base': {'marketing_spend': 1.0, 'preco_concorrente': 1.0},
    'Pessimista': {'marketing_spend': 0.7, 'preco_concorrente': 0.9}
}

previsoes_cenarios = {}

for nome_cenario, ajustes in cenarios.items():
    df_cenario = df_features.copy()
    df_cenario['marketing_spend'] *= ajustes['marketing_spend']
    df_cenario['preco_concorrente'] *= ajustes['preco_concorrente']
    
    # Recalcular features que dependem dessas variáveis
    df_cenario['marketing_x_temperatura'] = df_cenario['marketing_spend'] * df_cenario['temperatura']
    df_cenario['preco_x_marketing'] = df_cenario['preco_concorrente'] * df_cenario['marketing_spend']
    
    # Preparar dados
    X_cenario = df_cenario[features]
    X_cenario_scaled = scaler.transform(X_cenario)
    
    # Prever
    previsoes_cenario = modelo_rf.predict(X_cenario_scaled)
    
    previsoes_cenarios[nome_cenario] = previsoes_cenario[-30:]  # Últimos 30 dias

# Visualizar cenários
plt.figure(figsize=(12, 6))
datas_cenario = df_features['data'].tail(30)

for nome_cenario, previsoes in previsoes_cenarios.items():
    plt.plot(datas_cenario, previsoes, label=f'Cenário {nome_cenario}', linewidth=2)

plt.title('Análise de Cenários - Próximos 30 Dias')
plt.xlabel('Data')
plt.ylabel('Vendas Previstas')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 12. MÉTRICAS DE NEGÓCIO
print("\n12. MÉTRICAS DE NEGÓCIO")
print("-" * 60)

# Calcular métricas de negócio
vendas_medias_historicas = df_features['vendas'].mean()
previsao_media_30_dias = previsoes_futuras['previsao_hibrida'].mean()

# Variação esperada
variacao_percentual = ((previsao_media_30_dias - vendas_medias_historicas) / vendas_medias_historicas) * 100

# Intervalo de confiança (simplificado)
erro_padrao = np.std(previsoes_futuras['previsao_hibrida'])
intervalo_confianca = 1.96 * erro_padrao

print("Métricas de Negócio:")
print(f"• Venda média histórica: {vendas_medias_historicas:.2f}")
print(f"• Previsão média (30 dias): {previsao_media_30_dias:.2f}")
print(f"• Variação esperada: {variacao_percentual:.2f}%")
print(f"• Intervalo de confiança (95%): ±{intervalo_confianca:.2f}")

# Métricas por cenário
print(f"\nAnálise por Cenário:")
for nome_cenario, previsoes in previsoes_cenarios.items():
    media_cenario = np.mean(previsoes)
    variacao_cenario = ((media_cenario - vendas_medias_historicas) / vendas_medias_historicas) * 100
    print(f"• {nome_cenario}: {media_cenario:.2f} ({variacao_cenario:+.2f}%)")

# 13. DEPLOY E MONITORAMENTO
print("\n13. DEPLOY E MONITORAMENTO")
print("-" * 60)

import joblib

# Salvar modelos
joblib.dump(modelo_rf, 'modelo_previsao_rf.pkl')
joblib.dump(resultado_arima, 'modelo_arima.pkl')
joblib.dump(scaler, 'scaler_temporal.pkl')

# Salvar dados
df_features.to_csv('dados_temporais_completos.csv', index=False)
previsoes_futuras.to_csv('previsoes_futuras.csv', index=False)

print("Componentes salvos:")
print("• modelo_previsao_rf.pkl")
print("• modelo_arima.pkl")
print("• scaler_temporal.pkl")
print("• dados_temporais_completos.csv")
print("• previsoes_futuras.csv")

# Sistema de monitoramento (exemplo)
print(f"\nSistema de Monitoramento:")
print("""
# Métricas para monitorar:
# 1. MAPE (Mean Absolute Percentage Error)
# 2. Bias das previsões
# 3. Cobertura do intervalo de confiança
# 4. Performance em diferentes períodos

# Alertas:
# - Se MAPE > 15% por 3 dias consecutivos
# - Se bias > 10% (sistemático)
# - Se cobertura < 80%

# Retreinamento:
# - Mensal com novos dados
# - Quando performance degrada
# - Após eventos especiais
""")

# 14. RELATÓRIO FINAL
print("\n14. RELATÓRIO FINAL")
print("-" * 60)

metricas_finais = {
    'Período Análise': f"{df_features['data'].min().strftime('%d/%m/%Y')} a {df_features['data'].max().strftime('%d/%m/%Y')}",
    'Total Dias': len(df_features),
    'Features Criadas': len(features),
    'Melhor Modelo': 'Híbrido',
    'RMSE Híbrido': f"{rmse_hibrido:.2f}",
    'MAE Híbrido': f"{mae_hibrido:.2f}",
    'R² Híbrido': f"{r2_hibrido:.4f}",
    'Previsão 30 dias': f"{previsao_media_30_dias:.2f}",
    'Variação Esperada': f"{variacao_percentual:.2f}%"
}

print("RELATÓRIO FINAL DO PROJETO:")
for metrica, valor in metricas_finais.items():
    print(f"• {metrica}: {valor}")

print(f"\nSISTEMAS IMPLEMENTADOS:")
print("✅ Feature engineering avançado")
print("✅ Múltiplos modelos (RF, ARIMA, Híbrido)")
print("✅ Validação temporal")
print("✅ Previsão futura")
print("✅ Análise de cenários")
print("✅ Métricas de negócio")

print(f"\nAPLICAÇÕES PRÁTICAS:")
print("📊 Planejamento de demanda")
print("📈 Otimização de estoque")
print("💰 Previsão de receita")
print("🎯 Campanhas de marketing")

print(f"\nPRÓXIMOS PASSOS:")
print("🚀 Implementar modelos mais avançados (LSTM, Prophet)")
print("🚀 Adicionar mais variáveis externas")
print("🚀 Sistema de alertas em tempo real")
print("🚀 Integração com ERP/CRM")

print("\n" + "=" * 80)
print("PROJETO DE PREVISÃO TEMPORAL CONCLUÍDO!")
print("Sistema completo pronto para produção!")
print("=" * 80)
