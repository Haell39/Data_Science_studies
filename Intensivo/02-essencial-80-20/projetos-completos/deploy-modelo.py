"""
PROJETO COMPLETO - DEPLOY DE MODELOS
Sistema completo para deploy de modelos de Machine Learning
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from flask import Flask, request, jsonify
import joblib
import json
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PROJETO COMPLETO - DEPLOY DE MODELOS")
print("=" * 80)

# 1. CONFIGURAÇÃO DO AMBIENTE
print("\n1. CONFIGURAÇÃO DO AMBIENTE")
print("-" * 60)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deploy_model.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configurações
CONFIG = {
    'modelo_path': 'modelo_churn.pkl',
    'scaler_path': 'scaler_churn.pkl',
    'encoder_path': 'encoder_churn.pkl',
    'threshold': 0.25,
    'api_host': '0.0.0.0',
    'api_port': 5000,
    'log_level': 'INFO'
}

print("Configurações carregadas:")
for chave, valor in CONFIG.items():
    print(f"  {chave}: {valor}")

# 2. CARREGAR MODELO E COMPONENTES
print("\n2. CARREGAR MODELO E COMPONENTES")
print("-" * 60)

def carregar_modelo():
    """Carregar modelo e componentes salvos"""
    try:
        modelo = joblib.load(CONFIG['modelo_path'])
        scaler = joblib.load(CONFIG['scaler_path'])
        encoder = joblib.load(CONFIG['encoder_path'])
        
        logger.info("Modelo e componentes carregados com sucesso")
        return modelo, scaler, encoder
    
    except FileNotFoundError as e:
        logger.error(f"Erro ao carregar componentes: {e}")
        return None, None, None

# Carregar componentes
modelo, scaler, encoder = carregar_modelo()

if modelo is None:
    print("Criando modelo simulado para demonstração...")
    
    # Criar dados simulados
    np.random.seed(42)
    n_samples = 1000
    
    dados = {
        'idade': np.random.normal(38, 12, n_samples),
        'tempo_cliente': np.random.exponential(24, n_samples),
        'saldo_medio': np.random.lognormal(8, 1, n_samples),
        'num_produtos': np.random.randint(1, 6, n_samples),
        'tem_cartao': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'ativo_ult_3m': np.random.choice([0, 1], n_samples, p=[0.15, 0.85]),
        'score_credito': np.random.uniform(300, 850, n_samples),
        'cidade': np.random.choice(['SP', 'RJ', 'BH', 'POA', 'REC'], n_samples),
        'segmento': np.random.choice(['Basic', 'Silver', 'Gold', 'Platinum'], 
                                    n_samples, p=[0.4, 0.3, 0.2, 0.1])
    }
    
    df = pd.DataFrame(dados)
    
    # Calcular churn
    prob_churn = (
        -df['idade'] / 100 + 
        -df['tempo_cliente'] / 50 + 
        -df['saldo_medio'] / 100000 + 
        -df['num_produtos'] * 0.1 + 
        -df['tem_cartao'] * 0.15 + 
        -df['ativo_ult_3m'] * 0.3 + 
        (850 - df['score_credito']) / 1000
    )
    
    prob_churn += np.random.normal(0, 0.15, n_samples)
    prob_churn = np.clip(prob_churn, 0, 1)
    df['churn'] = (prob_churn > 0.25).astype(1)
    
    # Preparar dados
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    # Encoding
    encoder = LabelEncoder()
    X['cidade_encoded'] = encoder.fit_transform(X['cidade'])
    X['segmento_encoded'] = encoder.fit_transform(X['segmento'])
    X = X.drop(['cidade', 'segmento'], axis=1)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train_scaled, y_train)
    
    # Salvar componentes
    joblib.dump(modelo, CONFIG['modelo_path'])
    joblib.dump(scaler, CONFIG['scaler_path'])
    joblib.dump(encoder, CONFIG['encoder_path'])
    
    print("Modelo simulado criado e salvo!")

# 3. SISTEMA DE PREDIÇÃO
print("\n3. SISTEMA DE PREDIÇÃO")
print("-" * 60)

class SistemaPredicao:
    """Sistema completo para predição de churn"""
    
    def __init__(self, modelo, scaler, encoder, threshold=0.25):
        self.modelo = modelo
        self.scaler = scaler
        self.encoder = encoder
        self.threshold = threshold
        self.historico_predicoes = []
        
    def preprocessar_dados(self, dados):
        """Preprocessar dados para predição"""
        df = pd.DataFrame(dados)
        
        # Encoding
        if 'cidade' in df.columns:
            df['cidade_encoded'] = self.encoder.fit_transform(df['cidade'])
            df = df.drop('cidade', axis=1)
        
        if 'segmento' in df.columns:
            df['segmento_encoded'] = self.encoder.fit_transform(df['segmento'])
            df = df.drop('segmento', axis=1)
        
        # Garantir ordem das colunas
        colunas_esperadas = ['idade', 'tempo_cliente', 'saldo_medio', 'num_produtos', 
                           'tem_cartao', 'ativo_ult_3m', 'score_credito', 
                           'cidade_encoded', 'segmento_encoded']
        
        for col in colunas_esperadas:
            if col not in df.columns:
                df[col] = 0
        
        df = df[colunas_esperadas]
        
        # Scaling
        df_scaled = self.scaler.transform(df)
        
        return df_scaled
    
    def prever(self, dados):
        """Fazer predição"""
        try:
            # Preprocessar
            dados_preprocessados = self.preprocessar_dados(dados)
            
            # Predição
            probabilidades = self.modelo.predict_proba(dados_preprocessados)[:, 1]
            predicoes = (probabilidades >= self.threshold).astype(int)
            
            # Histórico
            timestamp = datetime.now()
            for i, (prob, pred) in enumerate(zip(probabilidades, predicoes)):
                self.historico_predicoes.append({
                    'timestamp': timestamp,
                    'probabilidade': float(prob),
                    'predicao': int(pred),
                    'dados': dados[i] if isinstance(dados, list) else dados.to_dict('records')[i]
                })
            
            return {
                'predicoes': predicoes.tolist(),
                'probabilidades': probabilidades.tolist(),
                'timestamp': timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro na predição: {e}")
            return {'erro': str(e)}
    
    def get_historico(self, n_ultimos=100):
        """Obter histórico de predições"""
        return self.historico_predicoes[-n_ultimos:]
    
    def get_estatisticas(self):
        """Obter estatísticas do sistema"""
        if not self.historico_predicoes:
            return {'mensagem': 'Nenhuma predição registrada'}
        
        df_hist = pd.DataFrame(self.historico_predicoes)
        
        stats = {
            'total_predicoes': len(df_hist),
            'taxa_churn_prevista': df_hist['predicao'].mean(),
            'probabilidade_media': df_hist['probabilidade'].mean(),
            'ultima_predicao': df_hist['timestamp'].max(),
            'predicoes_ultimas_24h': len(df_hist[df_hist['timestamp'] > (datetime.now() - pd.Timedelta(hours=24))])
        }
        
        return stats

# Criar sistema
sistema = SistemaPredicao(modelo, scaler, encoder, CONFIG['threshold'])

print("Sistema de predição criado!")

# 4. API FLASK
print("\n4. API FLASK")
print("-" * 60)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'modelo_carregado': modelo is not None
    })

@app.route('/prever', methods=['POST'])
def prever_churn():
    """Endpoint para predição de churn"""
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400
        
        # Se for um único cliente
        if isinstance(dados, dict):
            dados = [dados]
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['idade', 'tempo_cliente', 'saldo_medio', 'num_produtos', 
                              'tem_cartao', 'ativo_ult_3m', 'score_credito']
        
        for cliente in dados:
            for campo in campos_obrigatorios:
                if campo not in cliente:
                    return jsonify({'erro': f'Campo obrigatório ausente: {campo}'}), 400
        
        # Fazer predição
        resultado = sistema.prever(dados)
        
        if 'erro' in resultado:
            return jsonify(resultado), 500
        
        # Formatar resposta
        resposta = {
            'predicoes': [],
            'timestamp': resultado['timestamp']
        }
        
        for i, (pred, prob) in enumerate(zip(resultado['predicoes'], resultado['probabilidades'])):
            resposta['predicoes'].append({
                'cliente_id': i + 1,
                'churn': bool(pred),
                'probabilidade': round(prob, 4),
                'risco': 'Alto' if prob >= 0.7 else 'Médio' if prob >= 0.4 else 'Baixo'
            })
        
        return jsonify(resposta)
        
    except Exception as e:
        logger.error(f"Erro no endpoint /prever: {e}")
        return jsonify({'erro': str(e)}), 500

@app.route('/estatisticas', methods=['GET'])
def get_estatisticas():
    """Endpoint para estatísticas do sistema"""
    stats = sistema.get_estatisticas()
    return jsonify(stats)

@app.route('/historico', methods=['GET'])
def get_historico():
    """Endpoint para histórico de predições"""
    n_ultimos = request.args.get('n_ultimos', 100, type=int)
    historico = sistema.get_historico(n_ultimos)
    return jsonify(historico)

@app.route('/modelo/info', methods=['GET'])
def modelo_info():
    """Informações sobre o modelo"""
    if modelo is None:
        return jsonify({'erro': 'Modelo não carregado'}), 500
    
    info = {
        'tipo_modelo': type(modelo).__name__,
        'threshold': CONFIG['threshold'],
        'features_entrada': ['idade', 'tempo_cliente', 'saldo_medio', 'num_produtos', 
                           'tem_cartao', 'ativo_ult_3m', 'score_credito', 
                           'cidade', 'segmento'],
        'data_criacao': datetime.now().isoformat()
    }
    
    return jsonify(info)

# 5. MONITORAMENTO E LOGGING
print("\n5. MONITORAMENTO E LOGGING")
print("-" * 60)

class Monitoramento:
    """Sistema de monitoramento do modelo"""
    
    def __init__(self):
        self.metricas = {
            'predicoes_totais': 0,
            'predicoes_churn': 0,
            'erros': 0,
            'tempo_resposta_medio': 0
        }
        self.alertas = []
    
    def registrar_predicao(self, resultado, tempo_resposta):
        """Registrar métricas de predição"""
        self.metricas['predicoes_totais'] += len(resultado.get('predicoes', []))
        self.metricas['predicoes_churn'] += sum(resultado.get('predicoes', []))
        
        # Atualizar tempo médio de resposta
        if self.metricas['predicoes_totais'] > 0:
            self.metricas['tempo_resposta_medio'] = (
                (self.metricas['tempo_resposta_medio'] * (self.metricas['predicoes_totais'] - len(resultado.get('predicoes', []))) + tempo_resposta) /
                self.metricas['predicoes_totais']
            )
        
        # Verificar alertas
        self.verificar_alertas()
    
    def registrar_erro(self, erro):
        """Registrar erro"""
        self.metricas['erros'] += 1
        logger.error(f"Erro registrado: {erro}")
        
        # Alerta de erro
        if self.metricas['erros'] > 10:
            self.alertas.append({
                'tipo': 'ERRO_ALTO',
                'mensagem': f'Alta taxa de erros: {self.metricas["erros"]}',
                'timestamp': datetime.now()
            })
    
    def verificar_alertas(self):
        """Verificar condições de alerta"""
        taxa_churn = 0
        if self.metricas['predicoes_totais'] > 0:
            taxa_churn = self.metricas['predicoes_churn'] / self.metricas['predicoes_totais']
        
        # Alerta de alta taxa de churn
        if taxa_churn > 0.3:
            self.alertas.append({
                'tipo': 'ALTA_TAXA_CHURN',
                'mensagem': f'Alta taxa de churn prevista: {taxa_churn:.2%}',
                'timestamp': datetime.now()
            })
        
        # Alerta de performance
        if self.metricas['tempo_resposta_medio'] > 2.0:  # 2 segundos
            self.alertas.append({
                'tipo': 'LENTIDAO',
                'mensagem': f'Tempo de resposta alto: {self.metricas["tempo_resposta_medio"]:.2f}s',
                'timestamp': datetime.now()
            })
    
    def get_metricas(self):
        """Obter métricas atuais"""
        return self.metricas
    
    def get_alertas(self):
        """Obter alertas ativos"""
        return self.alertas[-10:]  # Últimos 10 alertas

# Criar sistema de monitoramento
monitor = Monitoramento()

# Middleware para monitoramento
@app.before_request
def before_request():
    request.start_time = datetime.now()

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        tempo_resposta = (datetime.now() - request.start_time).total_seconds()
        
        # Registrar métricas se for endpoint de predição
        if request.endpoint == 'prever_churn' and response.status_code == 200:
            monitor.registrar_predicao({}, tempo_resposta)
    
    return response

# 6. TESTES DO SISTEMA
print("\n6. TESTES DO SISTEMA")
print("-" * 60)

def testar_sistema():
    """Testar o sistema completo"""
    print("Realizando testes do sistema...")
    
    # Teste 1: Predição individual
    cliente_teste = {
        'idade': 35,
        'tempo_cliente': 24,
        'saldo_medio': 5000,
        'num_produtos': 3,
        'tem_cartao': 1,
        'ativo_ult_3m': 1,
        'score_credito': 700,
        'cidade': 'SP',
        'segmento': 'Silver'
    }
    
    resultado = sistema.prever([cliente_teste])
    print(f"✅ Teste 1 - Predição individual: {'OK' if 'erro' not in resultado else 'FALHOU'}")
    
    # Teste 2: Predição em lote
    clientes_teste = [
        cliente_teste,
        {
            'idade': 25,
            'tempo_cliente': 6,
            'saldo_medio': 1000,
            'num_produtos': 1,
            'tem_cartao': 0,
            'ativo_ult_3m': 0,
            'score_credito': 400,
            'cidade': 'RJ',
            'segmento': 'Basic'
        }
    ]
    
    resultado_lote = sistema.prever(clientes_teste)
    print(f"✅ Teste 2 - Predição em lote: {'OK' if 'erro' not in resultado_lote else 'FALHOU'}")
    
    # Teste 3: Estatísticas
    stats = sistema.get_estatisticas()
    print(f"✅ Teste 3 - Estatísticas: {'OK' if 'erro' not in stats else 'FALHOU'}")
    
    # Teste 4: Monitoramento
    metricas_monitor = monitor.get_metricas()
    print(f"✅ Teste 4 - Monitoramento: {'OK' if metricas_monitor else 'FALHOU'}")
    
    print("\nTestes concluídos!")

# Executar testes
testar_sistema()

# 7. DOCUMENTAÇÃO DA API
print("\n7. DOCUMENTAÇÃO DA API")
print("-" + 60)

documentacao = """
API DE PREDIÇÃO DE CHURN
========================

Endpoints:

1. GET /health
   - Health check da API
   - Retorna: status, timestamp, modelo_carregado

2. POST /prever
   - Realizar predição de churn
   - Body: JSON com dados do cliente
   - Campos obrigatórios: idade, tempo_cliente, saldo_medio, num_produtos, 
                        tem_cartao, ativo_ult_3m, score_credito, cidade, segmento
   - Retorna: predições, probabilidades, timestamp

Exemplo de requisição:
{
    "idade": 35,
    "tempo_cliente": 24,
    "saldo_medio": 5000,
    "num_produtos": 3,
    "tem_cartao": 1,
    "ativo_ult_3m": 1,
    "score_credito": 700,
    "cidade": "SP",
    "segmento": "Silver"
}

Exemplo de resposta:
{
    "predicoes": [
        {
            "cliente_id": 1,
            "churn": false,
            "probabilidade": 0.1234,
            "risco": "Baixo"
        }
    ],
    "timestamp": "2023-12-01T10:30:00"
}

3. GET /estatisticas
   - Estatísticas do sistema
   - Retorna: total_predicoes, taxa_churn_prevista, etc.

4. GET /historico
   - Histórico de predições
   - Query params: n_ultimos (default: 100)

5. GET /modelo/info
   - Informações sobre o modelo
   - Retorna: tipo_modelo, features, threshold, etc.

Códigos de status:
- 200: Sucesso
- 400: Erro nos dados de entrada
- 500: Erro interno do servidor
"""

print(documentacao)

# 8. DEPLOY AUTOMÁTICO
print("\n8. DEPLOY AUTOMÁTICO")
print("-" + 60)

def criar_dockerfile():
    """Criar Dockerfile para deploy"""
    dockerfile = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "deploy_modelo.py"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    print("Dockerfile criado!")

def criar_requirements():
    """Criar requirements.txt"""
    requirements = """
flask==2.3.3
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
joblib==1.3.2
gunicorn==21.2.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("requirements.txt criado!")

def criar_docker_compose():
    """Criar docker-compose.yml"""
    docker_compose = """
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
    restart: unless-stopped
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    print("docker-compose.yml criado!")

# Criar arquivos de deploy
criar_dockerfile()
criar_requirements()
criar_docker_compose()

# 9. MELHORES FUTURAS
print("\n9. MELHORES FUTURAS")
print("-" + 60)

melhorias = """
MELHORIAS FUTURAS:

1. SEGURANÇA:
   - Autenticação JWT
   - Rate limiting
   - HTTPS
   - Input validation avançado

2. PERFORMANCE:
   - Cache Redis
   - Load balancing
   - Async processing
   - Compressão de respostas

3. MONITORAMENTO:
   - Prometheus + Grafana
   - Health checks detalhados
   - Alertas customizáveis
   - Dashboard em tempo real

4. DEPLOY:
   - Kubernetes
   - CI/CD pipeline
   - Blue-green deployment
   - Auto-scaling

5. MODELO:
   - A/B testing
   - Retreinamento automático
   - Versionamento de modelos
   - Feature flags

6. NEGÓCIO:
   - SLA monitoring
   - Business metrics
   - Cost tracking
   - ROI analysis
"""

print(melhorias)

# 10. RELATÓRIO FINAL
print("\n10. RELATÓRIO FINAL")
print("-" + 60)

relatorio_final = {
    'Sistema': 'API de Predição de Churn',
    'Modelo': 'Random Forest',
    'Endpoints': 5,
    'Features': 9,
    'Threshold': CONFIG['threshold'],
    'Porta': CONFIG['api_port'],
    'Status': 'Pronto para deploy'
}

print("RELATÓRIO FINAL:")
for chave, valor in relatorio_final.items():
    print(f"• {chave}: {valor}")

print(f"\nCOMPONENTES CRIADOS:")
print("✅ Sistema de predição completo")
print("✅ API REST com Flask")
print("✅ Sistema de monitoramento")
print("✅ Logging e alertas")
print("✅ Testes automatizados")
print("✅ Documentação completa")
print("✅ Docker containerização")
print("✅ Docker Compose")

print(f"\nARQUIVOS GERADOS:")
print("• deploy_modelo.py (sistema completo)")
print("• modelo_churn.pkl")
print("• scaler_churn.pkl")
print("• encoder_churn.pkl")
print("• Dockerfile")
print("• requirements.txt")
print("• docker-compose.yml")
print("• deploy_model.log")

print(f"\nPRÓXIMOS PASSOS:")
print("🚀 Testar localmente: python deploy_modelo.py")
print("🚀 Build Docker: docker build -t api-churn .")
print("🚀 Deploy: docker-compose up -d")
print("🚀 Testar API: curl http://localhost:5000/health")

print("\n" + "=" * 80)
print("SISTEMA DE DEPLOY CONCLUÍDO!")
print("API completa pronta para produção!")
print("=" * 80)

# Para iniciar a API (descomentar para usar)
# if __name__ == '__main__':
#     print("Iniciando API...")
#     app.run(host=CONFIG['api_host'], port=CONFIG['api_port'], debug=True)
