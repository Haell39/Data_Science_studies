"""
PROJETO COMPLETO - SISTEMA DE RECOMENDAÇÃO
Sistema completo de recomendação de filmes com múltiplas abordagens
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PROJETO COMPLETO - SISTEMA DE RECOMENDAÇÃO")
print("=" * 80)

# 1. GERAÇÃO DE DADOS REALISTAS
print("\n1. GERAÇÃO DE DADOS REALISTAS")
print("-" * 60)

# Dataset de filmes
filmes_data = [
    # Ação/Aventura
    {"id": 1, "titulo": "Vingadores: Ultimato", "genero": "Ação", "ano": 2019, "duracao": 181, "descricao": "Os Vingadores se reúnem para derrotar Thanos."},
    {"id": 2, "titulo": "Mad Max: Estrada da Fúria", "genero": "Ação", "ano": 2015, "duracao": 120, "descricao": "Em um mundo pós-apocalíptico, uma mulher luta pela liberdade."},
    {"id": 3, "titulo": "John Wick", "genero": "Ação", "ano": 2014, "duracao": 101, "descricao": "Um assassino de aluguel busca vingança."},
    
    # Comédia
    {"id": 4, "titulo": "Todo Mundo em Pânico", "genero": "Comédia", "ano": 2000, "duracao": 88, "descricao": "Paródia de filmes de terror."},
    {"id": 5, "titulo": "Se Beber, Não Case", "genero": "Comédia", "ano": 2009, "duracao": 100, "descricao": "Amigos perdem a memória após uma festa."},
    {"id": 6, "titulo": "A Grande Ideia", "genero": "Comédia", "ano": 2011, "duracao": 109, "descricao": "Dois amigos criam um aplicativo de sucesso."},
    
    # Drama
    {"id": 7, "titulo": "A Paixão de Cristo", "genero": "Drama", "ano": 2004, "duracao": 127, "descricao": "História dos últimos dias de Jesus Cristo."},
    {"id": 8, "titulo": "Coração Valente", "genero": "Drama", "ano": 1995, "duracao": 177, "descricao": "Guerreiro escocês luta pela independência."},
    {"id": 9, "titulo": "O Poderoso Chefão", "genero": "Drama", "ano": 1972, "duracao": 175, "descricao": "História de uma família mafiosa."},
    
    # Ficção Científica
    {"id": 10, "titulo": "Matrix", "genero": "Ficção Científica", "ano": 1999, "duracao": 136, "descricao": "Um hacker descobre a verdade sobre a realidade."},
    {"id": 11, "titulo": "Blade Runner 2049", "genero": "Ficção Científica", "ano": 2017, "duracao": 164, "descricao": "Um policial caça replicantes no futuro."},
    {"id": 12, "titulo": "Interestelar", "genero": "Ficção Científica", "ano": 2014, "duracao": 169, "descricao": "Exploradores buscam novo lar para a humanidade."},
    
    # Terror
    {"id": 13, "titulo": "O Exorcista", "genero": "Terror", "ano": 1973, "duracao": 122, "descricao": "Menina é possuída por demônio."},
    {"id": 14, "titulo": "O Sexto Sentido", "genero": "Terror", "ano": 1999, "duracao": 107, "descricao": "Menino vê espíritos."},
    {"id": 15, "titulo": "Hereditário", "genero": "Terror", "ano": 2018, "duracao": 127, "descricao": "Família enfrenta maldição hereditária."},
    
    # Romance
    {"id": 16, "titulo": "Titanic", "genero": "Romance", "ano": 1997, "duracao": 194, "descricao": "História de amor no navio Titanic."},
    {"id": 17, "titulo": "A Culpa é das Estrelas", "genero": "Romance", "ano": 2014, "duracao": 126, "descricao": "Jovens com câncer se apaixonam."},
    {"id": 18, "titulo": "Orgulho e Preconceito", "genero": "Romance", "ano": 2005, "duracao": 129, "descricao": "História de amor na Inglaterra do século XIX."}
]

df_filmes = pd.DataFrame(filmes_data)

# Gerar avaliações de usuários
np.random.seed(42)
n_usuarios = 200
n_avaliacoes = 5000

avaliacoes = []
for i in range(n_avaliacoes):
    usuario_id = np.random.randint(1, n_usuarios + 1)
    filme_id = np.random.randint(1, len(df_filmes) + 1)
    
    # Usuários têm preferências por gêneros
    usuario_preferencia = usuario_id % len(df_filmes['genero'].unique())
    filme_genero = df_filmes.loc[df_filmes['id'] == filme_id, 'genero'].iloc[0]
    
    # Probabilidade baseada na preferência
    if df_filmes['genero'].unique()[usuario_preferencia] == filme_genero:
        nota_probs = [0.05, 0.05, 0.1, 0.3, 0.5]  # Mais provável dar nota alta
    else:
        nota_probs = [0.3, 0.3, 0.2, 0.15, 0.05]  # Mais provável dar nota baixa
    
    nota = np.random.choice([1, 2, 3, 4, 5], p=nota_probs)
    
    # Adicionar algum ruído
    if np.random.random() < 0.1:  # 10% de chance de nota aleatória
        nota = np.random.choice([1, 2, 3, 4, 5])
    
    avaliacoes.append({
        'usuario_id': usuario_id,
        'filme_id': filme_id,
        'nota': nota,
        'data_avaliacao': pd.Timestamp('2023-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
    })

df_avaliacoes = pd.DataFrame(avaliacoes)

# Remover duplicatas
df_avaliacoes = df_avaliacoes.drop_duplicates(['usuario_id', 'filme_id'])

print(f"Dataset de filmes: {df_filmes.shape}")
print(f"Dataset de avaliações: {df_avaliacoes.shape}")
print(f"Usuários únicos: {df_avaliacoes['usuario_id'].nunique()}")
print(f"Filmes únicos: {df_avaliacoes['filme_id'].nunique()}")

# 2. ANÁLISE EXPLORATÓRIA
print("\n2. ANÁLISE EXPLORATÓRIA")
print("-" * 60)

# Estatísticas das avaliações
print("Estatísticas das avaliações:")
print(df_avaliacoes['nota'].describe())

# Distribuição de notas
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
df_avaliacoes['nota'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribuição de Notas')
plt.xlabel('Nota')
plt.ylabel('Frequência')

# Filmes mais avaliados
plt.subplot(2, 3, 2)
filmes_populares = df_avaliacoes.merge(df_filmes, left_on='filme_id', right_on='id')
filmes_populares['titulo'].value_counts().head(10).plot(kind='barh')
plt.title('Top 10 Filmes Mais Avaliados')

# Gêneros mais populares
plt.subplot(2, 3, 3)
genero_popular = filmes_populares.groupby('genero')['nota'].count().sort_values(ascending=False)
genero_popular.plot(kind='bar')
plt.title('Avaliações por Gênero')
plt.xticks(rotation=45)

# Nota média por gênero
plt.subplot(2, 3, 4)
genero_nota = filmes_populares.groupby('genero')['nota'].mean().sort_values(ascending=False)
genero_nota.plot(kind='bar', color='orange')
plt.title('Nota Média por Gênero')
plt.xticks(rotation=45)

# Avaliações por usuário
plt.subplot(2, 3, 5)
avaliacoes_por_usuario = df_avaliacoes['usuario_id'].value_counts()
plt.hist(avaliacoes_por_usuario, bins=20, alpha=0.7)
plt.title('Distribuição de Avaliações por Usuário')
plt.xlabel('Número de Avaliações')
plt.ylabel('Número de Usuários')

# Avaliações ao longo do tempo
plt.subplot(2, 3, 6)
avaliacoes_tempo = df_avaliacoes.set_index('data_avaliacao').resample('M').size()
avaliacoes_tempo.plot(kind='line')
plt.title('Avaliações ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('Número de Avaliações')

plt.tight_layout()
plt.show()

# 3. SISTEMA DE RECOMENDAÇÃO - FILTRO COLABORATIVO
print("\n3. SISTEMA DE RECOMENDAÇÃO - FILTRO COLABORATIVO")
print("-" * 60)

# Criar matriz usuário-filme
matriz_usuario_filme = df_avaliacoes.pivot_table(
    index='usuario_id',
    columns='filme_id',
    values='nota'
).fillna(0)

print(f"Matriz usuário-filme: {matriz_usuario_filme.shape}")

# Calcular similaridade entre usuários
similaridade_usuarios = cosine_similarity(matriz_usuario_filme)
similaridade_usuarios_df = pd.DataFrame(
    similaridade_usuarios,
    index=matriz_usuario_filme.index,
    columns=matriz_usuario_filme.index
)

print(f"Matriz de similaridade: {similaridade_usuarios_df.shape}")

# Função de recomendação colaborativa
def recomendar_colaborativo(usuario_id, n_recomendacoes=5):
    """Recomenda filmes baseado em usuários similares"""
    
    if usuario_id not in matriz_usuario_filme.index:
        return "Usuário não encontrado"
    
    # Encontrar usuários similares (excluindo o próprio)
    usuarios_similares = similaridade_usuarios_df[usuario_id].sort_values(ascending=False)[1:11]
    
    # Filmes que o usuário ainda não avaliou
    filmes_avaliados = matriz_usuario_filme.loc[usuario_id]
    filmes_nao_avaliados = filmes_avaliados[filmes_avaliados == 0].index
    
    # Calcular previsão de notas para filmes não avaliados
    recomendacoes = {}
    
    for filme_id in filmes_nao_avaliados:
        nota_prevista = 0
        peso_total = 0
        
        for outro_usuario, similaridade in usuarios_similares.items():
            if matriz_usuario_filme.loc[outro_usuario, filme_id] > 0:
                nota_prevista += similaridade * matriz_usuario_filme.loc[outro_usuario, filme_id]
                peso_total += similaridade
        
        if peso_total > 0:
            recomendacoes[filme_id] = nota_prevista / peso_total
    
    # Retornar top N recomendações
    recomendacoes_ordenadas = sorted(recomendacoes.items(), key=lambda x: x[1], reverse=True)
    
    return recomendacoes_ordenadas[:n_recomendacoes]

# Testar sistema colaborativo
print("Teste do Sistema Colaborativo:")
for usuario in [1, 25, 50, 100]:
    print(f"\nRecomendações para Usuário {usuario}:")
    
    # Mostrar preferências do usuário
    avaliacoes_usuario = df_avaliacoes[df_avaliacoes['usuario_id'] == usuario]
    filmes_gostados = avaliacoes_usuario[avaliacoes_usuario['nota'] >= 4]
    
    if len(filmes_gostados) > 0:
        filmes_gostados_titulos = filmes_gostados.merge(df_filmes, left_on='filme_id', right_on='id')['titulo']
        print(f"  Filmes que gostou: {', '.join(filmes_gostados_titulos.head(3).tolist())}")
    
    # Recomendações
    recomendacoes = recomendar_colaborativo(usuario, 3)
    if isinstance(recomendacoes, list):
        for i, (filme_id, nota_prevista) in enumerate(recomendacoes, 1):
            filme_titulo = df_filmes[df_filmes['id'] == filme_id]['titulo'].iloc[0]
            print(f"  {i}. {filme_titulo} (nota prevista: {nota_prevista:.2f})")
    else:
        print(recomendacoes)

# 4. SISTEMA DE RECOMENDAÇÃO - BASEADO EM CONTEÚDO
print("\n\n4. SISTEMA DE RECOMENDAÇÃO - BASEADO EM CONTEÚDO")
print("-" * 60)

# Preparar features de conteúdo
df_filmes['features_conteudo'] = (
    df_filmes['genero'] + ' ' + 
    df_filmes['descricao'] + ' ' + 
    df_filmes['ano'].astype(str)
)

# Vetorizar conteúdo
vectorizer_conteudo = TfidfVectorizer(
    max_features=1000,
    stop_words=['o', 'a', 'os', 'as', 'de', 'do', 'da', 'em', 'para', 'com', 'um', 'uma'],
    ngram_range=(1, 2)
)

matriz_conteudo = vectorizer_conteudo.fit_transform(df_filmes['features_conteudo'])

# Calcular similaridade entre filmes
similaridade_filmes = cosine_similarity(matriz_conteudo)
similaridade_filmes_df = pd.DataFrame(
    similaridade_filmes,
    index=df_filmes['id'],
    columns=df_filmes['id']
)

print(f"Matriz de similaridade de conteúdo: {similaridade_filmes_df.shape}")

# Função de recomendação baseada em conteúdo
def recomendar_conteudo(usuario_id, n_recomendacoes=5):
    """Recomenda filmes baseado no conteúdo dos filmes que o usuário gostou"""
    
    # Obter filmes que o usuário gostou (nota >= 4)
    avaliacoes_usuario = df_avaliacoes[df_avaliacoes['usuario_id'] == usuario_id]
    filmes_gostados = avaliacoes_usuario[avaliacoes_usuario['nota'] >= 4]['filme_id'].tolist()
    
    if not filmes_gostados:
        return "Usuário não tem avaliações positivas suficientes"
    
    # Calcular perfil do usuário (média das similaridades dos filmes que gostou)
    perfil_usuario = np.zeros(len(df_filmes))
    
    for filme_gostado in filmes_gostados:
        if filme_gostado in similaridade_filmes_df.index:
            perfil_usuario += similaridade_filmes_df[filme_gostado].values
    
    perfil_usuario /= len(filmes_gostados)
    
    # Remover filmes que o usuário já avaliou
    filmes_ja_avaliados = set(avaliacoes_usuario['filme_id'].tolist())
    
    # Calcular scores de recomendação
    recomendacoes = []
    for i, filme_id in enumerate(df_filmes['id']):
        if filme_id not in filmes_ja_avaliados:
            score = perfil_usuario[i]
            recomendacoes.append((filme_id, score))
    
    # Ordenar e retornar top N
    recomendacoes.sort(key=lambda x: x[1], reverse=True)
    
    return recomendacoes[:n_recomendacoes]

# Testar sistema baseado em conteúdo
print("Teste do Sistema Baseado em Conteúdo:")
for usuario in [1, 25, 50, 100]:
    print(f"\nRecomendações para Usuário {usuario}:")
    
    # Recomendações
    recomendacoes = recomendar_conteudo(usuario, 3)
    if isinstance(recomendacoes, list):
        for i, (filme_id, score) in enumerate(recomendacoes, 1):
            filme_titulo = df_filmes[df_filmes['id'] == filme_id]['titulo'].iloc[0]
            print(f"  {i}. {filme_titulo} (score: {score:.3f})")
    else:
        print(recomendacoes)

# 5. SISTEMA HÍBRIDO
print("\n\n5. SISTEMA HÍBRIDO")
print("-" * 60)

def recomendar_hibrido(usuario_id, n_recomendacoes=5, peso_colaborativo=0.6, peso_conteudo=0.4):
    """Sistema híbrido que combina colaborativo e conteúdo"""
    
    # Obter recomendações colaborativas
    rec_colaborativo = recomendar_colaborativo(usuario_id, n_recomendacoes * 2)
    
    # Obter recomendações baseadas em conteúdo
    rec_conteudo = recomendar_conteudo(usuario_id, n_recomendacoes * 2)
    
    # Combinar recomendações
    recomendacoes_combinadas = {}
    
    # Adicionar recomendações colaborativas com peso
    if isinstance(rec_colaborativo, list):
        for filme_id, nota in rec_colaborativo:
            recomendacoes_combinadas[filme_id] = peso_colaborativo * nota
    
    # Adicionar recomendações de conteúdo com peso
    if isinstance(rec_conteudo, list):
        for filme_id, score in rec_conteudo:
            if filme_id in recomendacoes_combinadas:
                recomendacoes_combinadas[filme_id] += peso_conteudo * score * 5  # Normalizar para escala de notas
            else:
                recomendacoes_combinadas[filme_id] = peso_conteudo * score * 5
    
    # Ordenar e retornar top N
    recomendacoes_finais = sorted(recomendacoes_combinadas.items(), key=lambda x: x[1], reverse=True)
    
    return recomendacoes_finais[:n_recomendacoes]

# Testar sistema híbrido
print("Teste do Sistema Híbrido:")
for usuario in [1, 25, 50, 100]:
    print(f"\nRecomendações Híbridas para Usuário {usuario}:")
    
    recomendacoes = recomendar_hibrido(usuario, 3)
    if recomendacoes:
        for i, (filme_id, score) in enumerate(recomendações, 1):
            filme_titulo = df_filmes[df_filmes['id'] == filme_id]['titulo'].iloc[0]
            print(f"  {i}. {filme_titulo} (score: {score:.3f})")
    else:
        print("  Não foi possível gerar recomendações")

# 6. FACTORIZAÇÃO DE MATRIZ (SVD)
print("\n\n6. FACTORIZAÇÃO DE MATRIZ (SVD)")
print("-" * 60)

# Preparar dados para SVD
from scipy.sparse import csr_matrix

# Criar matriz esparsa
matriz_esparsa = csr_matrix(matriz_usuario_filme.values)

# Aplicar SVD
n_components = 50  # Número de fatores latentes
svd = TruncatedSVD(n_components=n_components, random_state=42)

# Treinar SVD
matriz_svd = svd.fit_transform(matriz_esparsa)

print(f"Matriz SVD: {matriz_svd.shape}")
print(f"Variância explicada: {svd.explained_variance_ratio_.sum():.3f}")

# Reconstruir matriz aproximada
matriz_reconstruida = svd.inverse_transform(matriz_svd)

# Função de recomendação SVD
def recomendar_svd(usuario_id, n_recomendacoes=5):
    """Recomenda usando SVD"""
    
    if usuario_id not in matriz_usuario_filme.index:
        return "Usuário não encontrado"
    
    # Índice do usuário na matriz
    usuario_idx = matriz_usuario_filme.index.get_loc(usuario_id)
    
    # Obter previsões para todos os filmes
    previsoes_usuario = matriz_reconstruida[usuario_idx]
    
    # Filmes que o usuário já avaliou
    filmes_avaliados = matriz_usuario_filme.loc[usuario_id]
    filmes_nao_avaliados = filmes_avaliados[filmes_avaliados == 0].index
    
    # Obter previsões para filmes não avaliados
    recomendacoes = []
    for filme_id in filmes_nao_avaliados:
        filme_idx = matriz_usuario_filme.columns.get_loc(filme_id)
        nota_prevista = previsoes_usuario[filme_idx]
        recomendacoes.append((filme_id, nota_prevista))
    
    # Ordenar e retornar top N
    recomendacoes.sort(key=lambda x: x[1], reverse=True)
    
    return recomendacoes[:n_recomendacoes]

# Testar SVD
print("Teste do Sistema SVD:")
for usuario in [1, 25, 50, 100]:
    print(f"\nRecomendações SVD para Usuário {usuario}:")
    
    recomendacoes = recomendar_svd(usuario, 3)
    if recomendacoes:
        for i, (filme_id, nota) in enumerate(recomendações, 1):
            filme_titulo = df_filmes[df_filmes['id'] == filme_id]['titulo'].iloc[0]
            print(f"  {i}. {filme_titulo} (nota prevista: {nota:.2f})")
    else:
        print("  Não foi possível gerar recomendações")

# 7. AVALIAÇÃO DOS SISTEMAS
print("\n\n7. AVALIAÇÃO DOS SISTEMAS")
print("-" * 60)

# Dividir dados para avaliação
treino, teste = train_test_split(df_avaliacoes, test_size=0.2, random_state=42)

# Criar matriz de treino
matriz_treino = treino.pivot_table(
    index='usuario_id',
    columns='filme_id',
    values='nota'
).fillna(0)

# Função para calcular RMSE
def calcular_rmse(previsoes, reais):
    """Calcula RMSE das previsões"""
    mse = mean_squared_error(reais, previsoes)
    return np.sqrt(mse)

# Avaliar SVD
print("Avaliação do Sistema SVD:")

# Treinar SVD nos dados de treino
matriz_treino_esparsa = csr_matrix(matriz_treino.values)
svd_treino = TruncatedSVD(n_components=50, random_state=42)
svd_treino.fit(matriz_treino_esparsa)

# Fazer previsões no conjunto de teste
previsoes_teste = []
reais_teste = []

for _, row in teste.iterrows():
    usuario_id = row['usuario_id']
    filme_id = row['filme_id']
    nota_real = row['nota']
    
    if usuario_id in matriz_treino.index and filme_id in matriz_treino.columns:
        usuario_idx = matriz_treino.index.get_loc(usuario_id)
        filme_idx = matriz_treino.columns.get_loc(filme_id)
        
        matriz_svd_teste = svd_treino.inverse_transform(svd_treino.transform(matriz_treino_esparsa))
        nota_prevista = matriz_svd_teste[usuario_idx, filme_idx]
        
        previsoes_teste.append(nota_prevista)
        reais_teste.append(nota_real)

if previsoes_teste:
    rmse_svd = calcular_rmse(previsoes_teste, reais_teste)
    print(f"RMSE SVD: {rmse_svd:.4f}")

# 8. SISTEMA COMPLETO DE RECOMENDAÇÃO
print("\n\n8. SISTEMA COMPLETO DE RECOMENDAÇÃO")
print("-" * 60)

class SistemaRecomendacao:
    """Sistema completo de recomendação com múltiplas abordagens"""
    
    def __init__(self):
        self.df_filmes = df_filmes
        self.df_avaliacoes = df_avaliacoes
        self.matriz_usuario_filme = matriz_usuario_filme
        self.similaridade_usuarios = similaridade_usuarios_df
        self.similaridade_filmes = similaridade_filmes_df
        self.vectorizer_conteudo = vectorizer_conteudo
        self.svd = svd
        self.matriz_svd = matriz_svd
    
    def recomendar(self, usuario_id, metodo='hibrido', n_recomendacoes=5):
        """Método principal de recomendação"""
        
        if metodo == 'colaborativo':
            return recomendar_colaborativo(usuario_id, n_recomendacoes)
        elif metodo == 'conteudo':
            return recomendar_conteudo(usuario_id, n_recomendacoes)
        elif metodo == 'svd':
            return recomendar_svd(usuario_id, n_recomendacoes)
        elif metodo == 'hibrido':
            return recomendar_hibrido(usuario_id, n_recomendacoes)
        else:
            return "Método não reconhecido"
    
    def explicar_recomendacao(self, usuario_id, filme_id):
        """Explica por que um filme foi recomendado"""
        
        explicacao = []
        
        # Verificar se há usuários similares que gostaram
        if usuario_id in self.similaridade_usuarios.index:
            usuarios_similares = self.similaridade_usuarios[usuario_id].sort_values(ascending=False)[1:6]
            
            for outro_usuario, similaridade in usuarios_similares.items():
                if self.matriz_usuario_filme.loc[outro_usuario, filme_id] >= 4:
                    explicacao.append(f"Usuários similares a você deram notas altas para este filme")
                    break
        
        # Verificar similaridade de conteúdo
        if usuario_id in self.matriz_usuario_filme.index:
            avaliacoes_usuario = self.df_avaliacoes[self.df_avaliacoes['usuario_id'] == usuario_id]
            filmes_gostados = avaliacoes_usuario[avaliacoes_usuario['nota'] >= 4]['filme_id'].tolist()
            
            if filmes_gostados:
                similaridade_media = 0
                for filme_gostado in filmes_gostados:
                    if filme_gostado in self.similaridade_filmes.index and filme_id in self.similaridade_filmes.columns:
                        similaridade_media += self.similaridade_filmes.loc[filme_gostado, filme_id]
                
                similaridade_media /= len(filmes_gostados)
                
                if similaridade_media > 0.3:
                    explicacao.append(f"Este filme é similar a outros que você gostou (similaridade: {similaridade_media:.2f})")
        
        return explicacao if explicacao else ["Recomendação baseada em múltiplos fatores"]
    
    def get_usuario_info(self, usuario_id):
        """Retorna informações sobre o usuário"""
        
        if usuario_id not in self.matriz_usuario_filme.index:
            return "Usuário não encontrado"
        
        avaliacoes_usuario = self.df_avaliacoes[self.df_avaliacoes['usuario_id'] == usuario_id]
        
        info = {
            'usuario_id': usuario_id,
            'total_avaliacoes': len(avaliacoes_usuario),
            'nota_media': avaliacoes_usuario['nota'].mean(),
            'generos_preferidos': [],
            'filmes_gostados': []
        }
        
        # Gêneros preferidos
        filmes_gostados = avaliacoes_usuario[avaliacoes_usuario['nota'] >= 4]
        if len(filmes_gostados) > 0:
            generos_gostados = filmes_gostados.merge(self.df_filmes, left_on='filme_id', right_on='id')['genero']
            info['generos_preferidos'] = generos_gostados.value_counts().head(3).index.tolist()
            
            filmes_gostados_titulos = filmes_gostados.merge(self.df_filmes, left_on='filme_id', right_on='id')['titulo']
            info['filmes_gostados'] = filmes_gostados_titulos.head(5).tolist()
        
        return info

# Criar sistema
sistema = SistemaRecomendacao()

# Testar sistema completo
print("Teste do Sistema Completo:")
usuario_teste = 1

print(f"\nInformações do Usuário {usuario_teste}:")
info_usuario = sistema.get_usuario_info(usuario_teste)
for chave, valor in info_usuario.items():
    print(f"  {chave}: {valor}")

print(f"\nRecomendações para Usuário {usuario_teste}:")
for metodo in ['colaborativo', 'conteudo', 'svd', 'hibrido']:
    print(f"\nMétodo: {metodo}")
    recomendacoes = sistema.recomendar(usuario_teste, metodo=metodo, n_recomendacoes=3)
    
    if isinstance(recomendacoes, list):
        for i, (filme_id, score) in enumerate(recomendacoes, 1):
            filme_titulo = df_filmes[df_filmes['id'] == filme_id]['titulo'].iloc[0]
            print(f"  {i}. {filme_titulo} (score: {score:.3f})")
            
            # Explicação
            explicacoes = sistema.explicar_recomendacao(usuario_teste, filme_id)
            for exp in explicacoes:
                print(f"     • {exp}")
    else:
        print(f"  {recomendacoes}")

# 9. DEPLOY E PRODUÇÃO
print("\n\n9. DEPLOY E PRODUÇÃO")
print("-" * 60)

import joblib

# Salvar componentes
joblib.dump(sistema, 'sistema_recomendacao.pkl')
df_filmes.to_csv('filmes.csv', index=False)
df_avaliacoes.to_csv('avaliacoes.csv', index=False)

print("Componentes salvos:")
print("• sistema_recomendacao.pkl")
print("• filmes.csv")
print("• avaliacoes.csv")

# API Flask (exemplo)
print(f"\nExemplo de API Flask:")
print("""
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Carregar sistema
sistema = joblib.load('sistema_recomendacao.pkl')

@app.route('/recomendar', methods=['POST'])
def recomendar_api():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    metodo = data.get('metodo', 'hibrido')
    n_recomendacoes = data.get('n_recomendacoes', 5)
    
    recomendacoes = sistema.recomendar(usuario_id, metodo, n_recomendacoes)
    
    if isinstance(recomendacoes, list):
        resultado = []
        for filme_id, score in recomendacoes:
            filme_info = sistema.df_filmes[sistema.df_filmes['id'] == filme_id].iloc[0]
            resultado.append({
                'filme_id': filme_id,
                'titulo': filme_info['titulo'],
                'genero': filme_info['genero'],
                'score': score
            })
        
        return jsonify({
            'usuario_id': usuario_id,
            'metodo': metodo,
            'recomendacoes': resultado
        })
    else:
        return jsonify({'erro': recomendacoes})

@app.route('/usuario/<int:usuario_id>', methods=['GET'])
def usuario_info(usuario_id):
    info = sistema.get_usuario_info(usuario_id)
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)
""")

# 10. MELHORIAS FUTURAS
print("\n\n10. MELHORIAS FUTURAS")
print("-" * 60)

print("MELHORIAS POSSÍVEIS:")
print("🚀 DEEP LEARNING:")
print("   • Redes neurais para recomendações")
print("   • Autoencoders para fatoração")
print("   • Modelos híbridos avançados")

print("\n📊 DADOS ENRIQUECIDOS:")
print("   • Informações demográficas dos usuários")
print("   • Contexto (horário, dispositivo, localização)")
print("   • Interações implícitas (visualizações, tempo)")

print("\n🎯 PERSONALIZAÇÃO:")
print("   • Sistemas multi-armed bandit")
print("   • Recomendações contextuais")
print("   • Aprendizado online em tempo real")

print("\n📈 ESCALABILIDADE:")
print("   • Processamento distribuído")
print("   • Cache inteligente")
print("   • Microserviços")

# 11. RELATÓRIO FINAL
print("\n\n11. RELATÓRIO FINAL")
print("-" * 60)

metricas_finais = {
    'Filmes': len(df_filmes),
    'Usuários': df_avaliacoes['usuario_id'].nunique(),
    'Avaliações': len(df_avaliacoes),
    'Métodos Implementados': 4,
    'RMSE SVD': f"{rmse_svd:.4f}" if 'rmse_svd' in locals() else "N/A",
    'Gêneros': df_filmes['genero'].nunique()
}

print("RELATÓRIO FINAL DO SISTEMA:")
for metrica, valor in metricas_finais.items():
    print(f"• {metrica}: {valor}")

print(f"\nSISTEMAS IMPLEMENTADOS:")
print("✅ Filtro Colaborativo (usuário-usuário)")
print("✅ Baseado em Conteúdo")
print("✅ Fatoração de Matriz (SVD)")
print("✅ Sistema Híbrido")
print("✅ Explicações de recomendações")

print(f"\nAPLICAÇÕES PRÁTICAS:")
print("🎬 Plataformas de streaming")
print("🛒 E-commerce")
print("📚 Recomendação de conteúdo")
print("🎵 Música e podcasts")

print("\n" + "=" * 80)
print("SISTEMA DE RECOMENDAÇÃO CONCLUÍDO!")
print("Sistema completo com múltiplas abordagens!")
print("=" * 80)
