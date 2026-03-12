"""
DEEP LEARNING ESSENCIAL - 80/20
Os 20% mais importantes para resolver 80% dos problemas reais
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("DEEP LEARNING ESSENCIAL - 80/20")
print("=" * 70)

# 1. INTRODUÇÃO A REDES NEURAIS
print("\n1. INTRODUÇÃO A REDES NEURAIS")
print("-" * 50)

print("CONCEITOS FUNDAMENTAIS:")
print("• Neurônio: Unidade básica que recebe entradas e produz uma saída")
print("• Camada: Conjunto de neurônios que processam informações")
print("• Pesos: Parâmetros que ajustam a importância das entradas")
print("• Função de Ativação: Transforma a saída do neurônio")
print("• Backpropagation: Algoritmo para treinar a rede")
print("• Gradient Descent: Otimizador para ajustar pesos")

print("\nTIPOS DE REDES:")
print("• MLP (Multi-Layer Perceptron): Para dados tabulares")
print("• CNN (Convolutional Neural Network): Para imagens")
print("• RNN (Recurrent Neural Network): Para sequências/texto")
print("• LSTM/GRU: Para sequências longas")

# Verificar TensorFlow
print(f"\nVersão TensorFlow: {tf.__version__}")
print("GPU disponível:", "Sim" if len(tf.config.list_physical_devices('GPU')) > 0 else "Não")

# 2. REDE NEURAL PARA CLASSIFICAÇÃO (MLP)
print("\n2. REDE NEURAL PARA CLASSIFICAÇÃO")
print("-" * 50)

# Gerar dados de classificação não-linear
np.random.seed(42)
n_samples = 1000

# Criar dados em formato de lua (não linearmente separável)
def make_moons_data(n_samples):
    X = np.zeros((n_samples, 2))
    y = np.zeros(n_samples)
    
    for i in range(n_samples):
        if i < n_samples // 2:
            # Lua superior
            t = np.random.uniform(0, np.pi)
            r = np.random.normal(1, 0.1)
            X[i] = [r * np.cos(t), r * np.sin(t) + 0.5]
            y[i] = 0
        else:
            # Lua inferior
            t = np.random.uniform(0, np.pi)
            r = np.random.normal(1, 0.1)
            X[i] = [r * np.cos(t), r * np.sin(t) - 0.5]
            y[i] = 1
    
    return X, y

X, y = make_moons_data(n_samples)

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Visualizar dados
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', alpha=0.6)
plt.title('Dados Originais')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

plt.subplot(1, 2, 2)
plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], c=y_train, cmap='viridis', alpha=0.6)
plt.title('Dados Normalizados')
plt.xlabel('Feature 1 (Normalizado)')
plt.ylabel('Feature 2 (Normalizado)')
plt.tight_layout()
plt.show()

# Construir rede neural
model_mlp = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(2,)),
    layers.Dense(8, activation='relu'),
    layers.Dense(4, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compilar modelo
model_mlp.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Arquitetura da Rede Neural:")
model_mlp.summary()

# Treinar modelo
print("\nTreinando a Rede Neural...")
history = model_mlp.fit(
    X_train_scaled, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Avaliar modelo
test_loss, test_accuracy = model_mlp.evaluate(X_test_scaled, y_test, verbose=0)
print(f"\nAcurácia no teste: {test_accuracy:.4f}")

# Visualizar treinamento
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Treino')
plt.plot(history.history['val_loss'], label='Validação')
plt.title('Loss durante Treinamento')
plt.xlabel('Época')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Treino')
plt.plot(history.history['val_accuracy'], label='Validação')
plt.title('Acurácia durante Treinamento')
plt.xlabel('Época')
plt.ylabel('Acurácia')
plt.legend()
plt.tight_layout()
plt.show()

# Visualizar decisões
def plot_decision_boundary(model, X, y):
    x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
    y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='black')
    plt.title('Fronteira de Decisão da Rede Neural')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

plot_decision_boundary(model_mlp, X_test_scaled, y_test)

# 3. REDE NEURAL PARA REGRESSÃO
print("\n3. REDE NEURAL PARA REGRESSÃO")
print("-" * 50)

# Gerar dados de regressão não-linear
np.random.seed(42)
n_samples = 1000

X_reg = np.random.uniform(-2, 2, (n_samples, 1))
y_reg = X_reg**3 + np.random.normal(0, 0.5, (n_samples, 1))

# Dividir dados
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# Normalizar
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_train_reg_scaled = scaler_X.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_X.transform(X_test_reg)
y_train_reg_scaled = scaler_y.fit_transform(y_train_reg)
y_test_reg_scaled = scaler_y.transform(y_test_reg)

# Visualizar dados
plt.figure(figsize=(10, 4))
plt.scatter(X_reg, y_reg, alpha=0.6)
plt.title('Dados de Regressão Não-Linear')
plt.xlabel('X')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.show()

# Construir rede para regressão
model_reg = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(1,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(1)  # Sem ativação para regressão
])

# Compilar
model_reg.compile(
    optimizer='adam',
    loss='mse',
    metrics=['mae']
)

print("Arquitetura da Rede de Regressão:")
model_reg.summary()

# Treinar
print("\nTreinando Rede de Regressão...")
history_reg = model_reg.fit(
    X_train_reg_scaled, y_train_reg_scaled,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Avaliar
test_loss, test_mae = model_reg.evaluate(X_test_reg_scaled, y_test_reg_scaled, verbose=0)
print(f"\nMAE no teste: {test_mae:.4f}")

# Visualizar resultados
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history_reg.history['loss'], label='Treino')
plt.plot(history_reg.history['val_loss'], label='Validação')
plt.title('Loss durante Treinamento')
plt.xlabel('Época')
plt.ylabel('MSE')
plt.legend()

plt.subplot(1, 2, 2)
# Previsões
y_pred_scaled = model_reg.predict(X_test_reg_scaled)
y_pred = scaler_y.inverse_transform(y_pred_scaled)

plt.scatter(X_test_reg, y_test_reg, alpha=0.6, label='Real')
plt.scatter(X_test_reg, y_pred, alpha=0.6, label='Previsto')
plt.title('Previsões vs Real')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 4. CLASSIFICAÇÃO MULTICLASSE (MNIST SIMPLIFICADO)
print("\n4. CLASSIFICAÇÃO MULTICLASSE")
print("-" * 50)

# Gerar dados multiclasse simulados
np.random.seed(42)
n_samples = 2000
n_features = 20
n_classes = 5

# Criar clusters para cada classe
X_multi = np.zeros((n_samples, n_features))
y_multi = np.zeros(n_samples)

for i in range(n_classes):
    start_idx = i * (n_samples // n_classes)
    end_idx = (i + 1) * (n_samples // n_classes)
    
    # Centro do cluster
    center = np.random.randn(n_features) * 2
    
    # Gerar pontos ao redor do centro
    X_multi[start_idx:end_idx] = center + np.random.randn(end_idx - start_idx, n_features)
    y_multi[start_idx:end_idx] = i

# Embaralhar
indices = np.random.permutation(n_samples)
X_multi = X_multi[indices]
y_multi = y_multi[indices]

# Dividir dados
X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
    X_multi, y_multi, test_size=0.2, random_state=42, stratify=y_multi
)

# Normalizar
scaler_multi = StandardScaler()
X_train_multi_scaled = scaler_multi.fit_transform(X_train_multi)
X_test_multi_scaled = scaler_multi.transform(X_test_multi)

# One-hot encoding para target
y_train_multi_onehot = keras.utils.to_categorical(y_train_multi, n_classes)
y_test_multi_onehot = keras.utils.to_categorical(y_test_multi, n_classes)

# Construir rede multiclasse
model_multi = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(n_features,)),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dense(n_classes, activation='softmax')
])

# Compilar
model_multi.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Arquitetura da Rede Multiclasse:")
model_multi.summary()

# Treinar
print("\nTreinando Rede Multiclasse...")
history_multi = model_multi.fit(
    X_train_multi_scaled, y_train_multi_onehot,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Avaliar
test_loss, test_accuracy = model_multi.evaluate(X_test_multi_scaled, y_test_multi_onehot, verbose=0)
print(f"\nAcurácia no teste: {test_accuracy:.4f}")

# Previsões e matriz de confusão
y_pred_proba = model_multi.predict(X_test_multi_scaled)
y_pred_class = np.argmax(y_pred_proba, axis=1)

plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test_multi, y_pred_class)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
           xticklabels=[f'Classe {i}' for i in range(n_classes)],
           yticklabels=[f'Classe {i}' for i in range(n_classes)])
plt.title('Matriz de Confusão - Multiclasse')
plt.ylabel('Real')
plt.xlabel('Previsto')
plt.show()

# 5. TÉCNICAS DE REGULARIZAÇÃO
print("\n5. TÉCNICAS DE REGULARIZAÇÃO")
print("-" * 50)

print("TÉCNICAS PARA EVITAR OVERFITTING:")
print("• Dropout: Desativa aleatoriamente neurônios durante treinamento")
print("• L1/L2 Regularization: Adiciona penalidade aos pesos")
print("• Early Stopping: Para treinamento quando performance para de melhorar")
print("• Batch Normalization: Normaliza ativações entre camadas")
print("• Data Augmentation: Aumenta quantidade de dados")

# Exemplo com Dropout e Early Stopping
model_regularized = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(2,)),
    layers.Dropout(0.3),
    layers.BatchNormalization(),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model_regularized.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Early Stopping
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

print("\nTreinando com Regularização e Early Stopping...")
history_reg = model_regularized.fit(
    X_train_scaled, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=0
)

print(f"Épocas treinadas: {len(history_reg.history['loss'])}")
test_loss, test_accuracy = model_regularized.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Acurácia no teste: {test_accuracy:.4f}")

# 6. SALVAR E CARREGAR MODELOS
print("\n6. SALVAR E CARREGAR MODELOS")
print("-" * 50)

# Salvar modelo completo
model_mlp.save('modelo_mlp.h5')
print("Modelo salvo como 'modelo_mlp.h5'")

# Salvar apenas pesos
model_mlp.save_weights('modelo_mlp_pesos.h5')
print("Pesos salvos como 'modelo_mlp_pesos.h5'")

# Carregar modelo
modelo_carregado = keras.models.load_model('modelo_mlp.h5')
print("Modelo carregado com sucesso")

# Verificar se funciona igual
test_loss_loaded, test_acc_loaded = modelo_carregado.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Acurácia modelo carregado: {test_acc_loaded:.4f}")

# 7. HIPERPARÂMETROS E OTIMIZAÇÃO
print("\n7. HIPERPARÂMETROS E OTIMIZAÇÃO")
print("-" * 50)

print("HIPERPARÂMETROS IMPORTANTES:")
print("• Learning Rate: Tamanho do passo do otimizador")
print("• Batch Size: Número de amostras por atualização")
print("• Número de Camadas: Profundidade da rede")
print("• Neurônios por Camada: Largura da rede")
print("• Função de Ativação: Não-linearidade")
print("• Otimizador: Algoritmo de atualização")

print("\nOTIMIZADORES COMUNS:")
print("• SGD: Gradient Descent básico")
print("• Adam: Adaptativo (mais usado)")
print("• RMSprop: Para problemas não-estacionários")
print("• Adagrad: Para features esparsas")

# Exemplo com diferentes learning rates
def testar_learning_rate(lr):
    model = keras.Sequential([
        layers.Dense(16, activation='relu', input_shape=(2,)),
        layers.Dense(8, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    history = model.fit(
        X_train_scaled, y_train,
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        verbose=0
    )
    
    return history

# Testar diferentes learning rates
learning_rates = [0.001, 0.01, 0.1]
plt.figure(figsize=(12, 4))

for i, lr in enumerate(learning_rates):
    history = testar_learning_rate(lr)
    plt.subplot(1, 3, i+1)
    plt.plot(history.history['loss'], label='Treino')
    plt.plot(history.history['val_loss'], label='Validação')
    plt.title(f'Learning Rate: {lr}')
    plt.xlabel('Época')
    plt.ylabel('Loss')
    plt.legend()

plt.tight_layout()
plt.show()

# 8. VISUALIZAÇÃO DE FEATURES
print("\n8. VISUALIZAÇÃO DE FEATURES")
print("-" * 50)

# Extrair features de uma camada intermediária
feature_extractor = keras.Model(
    inputs=model_mlp.inputs,
    outputs=model_mlp.layers[1].output  # Segunda camada
)

# Obter features
features = feature_extractor.predict(X_test_scaled)

# Reduzir dimensionalidade para visualização (PCA)
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
features_2d = pca.fit_transform(features)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], c=y_test, cmap='viridis', alpha=0.6)
plt.colorbar(scatter, label='Classe')
plt.title('Features Extraídas da Rede Neural (PCA)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.grid(True, alpha=0.3)
plt.show()

# 9. TRANSFER LEARNING (CONCEITO)
print("\n9. TRANSFER LEARNING (CONCEITO)")
print("-" * 50)

print("TRANSFER LEARNING:")
print("• Usar modelo pré-treinado em grande dataset")
print("• Adaptar para problema específico com menos dados")
print("• Economiza tempo e computação")
print("• Melhor performance com poucos dados")

print("\nFINE-TUNING:")
print("• Congelar camadas iniciais (features genéricas)")
print("• Treinar apenas camadas finais (específicas)")
print("• Ajustar learning rate menor")
print("• Descongelar gradualmente mais camadas")

# Exemplo conceitual (não executável sem modelo pré-treinado)
print("\nExemplo de Transfer Learning (conceito):")
print("""
# Carregar modelo pré-treinado
base_model = keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# Congelar camadas base
base_model.trainable = False

# Adicionar camadas customizadas
model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])
""")

# 10. DEPLOY E PRODUÇÃO
print("\n10. DEPLOY E PRODUÇÃO")
print("-" * 50)

print("CONSIDERAÇÕES PARA PRODUÇÃO:")
print("• Modelo serializado (.h5 ou SavedModel)")
print("• Pipeline de pré-processamento")
print("• API REST (Flask/FastAPI)")
print("• Monitoramento de performance")
print("• Versionamento de modelos")
print("• Retreinamento periódico")

# Função para inferência
def fazer_previsao(modelo, dados, scaler):
    """Função para fazer previsões em produção"""
    # Pré-processar
    dados_scaled = scaler.transform(dados)
    
    # Prever
    previsao = modelo.predict(dados_scaled)
    
    return previsao

# Exemplo de uso
exemplo_dados = X_test[:5]
previsoes = fazer_previsao(modelo_carregado, exemplo_dados, scaler)

print("\nExemplo de previsões:")
for i, (real, pred) in enumerate(zip(y_test[:5], previsoes.flatten())):
    print(f"Amostra {i+1}: Real={int(real)}, Previsto={pred:.3f} ({'Churn' if pred > 0.5 else 'Não Churn'})")

# 11. MELHORES PRÁTICAS
print("\n11. MELHORES PRÁTICAS")
print("-" * 50)

print("MELHORES PRÁTICAS:")
print("1. DADOS:")
print("   • Limpar e normalizar dados")
print("   • Dividir em treino/validação/teste")
print("   • Usar data augmentation quando possível")

print("\n2. ARQUITETURA:")
print("   • Começar simples e aumentar complexidade")
print("   • Usar regularização para evitar overfitting")
print("   • Experimentar diferentes funções de ativação")

print("\n3. TREINAMENTO:")
print("   • Usar early stopping")
print("   • Monitorar loss de validação")
print("   • Ajustar learning rate se necessário")

print("\n4. AVALIAÇÃO:")
print("   • Usar múltiplas métricas")
print("   • Analisar erros específicos")
print("   • Testar com dados não vistos")

# 12. RESUMO E PRÓXIMOS PASSOS
print("\n12. RESUMO E PRÓXIMOS PASSOS")
print("-" * 50)

print("RESUMO DO APRENDIZADO:")
print("✅ Redes Neurais básicas (MLP)")
print("✅ Classificação binária e multiclasse")
print("✅ Regressão com redes neurais")
print("✅ Regularização e prevenção de overfitting")
print("✅ Salvar e carregar modelos")
print("✅ Otimização de hiperparâmetros")
print("✅ Visualização de features")

print("\nPRÓXIMOS PASSOS:")
print("📚 Aprender CNN para imagens")
print("📚 Estudar RNN/LSTM para sequências")
print("📚 Explorar Transformers para NLP")
print("📚 Praticar com datasets reais")
print("📚 Implementar em projetos pessoais")

print("\n" + "=" * 70)
print("DEEP LEARNING ESSENCIAL 80/20 CONCLUÍDO!")
print("Você tem a base para resolver problemas reais com Deep Learning!")
print("=" * 70)
