"""## Tema Institucional

**Pergunta de Pesquisa:** Qual é a distribuição e a diferença de desempenho (nas provas objetivas e redação) entre os participantes do ENEM 2024, agrupados pela Unidade da Federação (UF) onde realizaram a prova?
"""

#@title Código do Tema Institucional
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():

    # --- Configuração Inicial ---
    dados_path = 'DADOS'
    dados_enem_file = os.path.join(dados_path, 'RESULTADOS_2024.csv')
    sns.set_theme(style="whitegrid", palette="viridis")
    
    # Cria a pasta para salvar os gráficos
    graficos_path = 'graficos_institucional'
    os.makedirs(graficos_path, exist_ok=True)

    # Lista de colunas a serem carregadas, para otimizar o uso de memória.
    cols_essenciais = [
        'SG_UF_PROVA', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
        'TP_STATUS_REDACAO', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'
    ]

    # --- Parte 1: Carregando Dados ---
    print("\n--- Parte 1: Carregando Dados ---")
    try:
        # Carrega apenas as colunas especificadas em 'usecols'.
        df = pd.read_csv(dados_enem_file, encoding='latin1', delimiter=';', usecols=cols_essenciais)
        print(f"Dados carregados com sucesso: {len(df)} registros.")
    except Exception as e:
        print(f"ERRO ao carregar CSV: {e}")
        return

    # --- Parte 2: Limpeza e Preparação dos Dados ---
    print("\n--- Parte 2: Limpando e preparando os dados ---")
    notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    # Remove linhas com valores nulos nas notas ou na UF.
    df.dropna(subset=notas_cols + ['SG_UF_PROVA'], inplace=True)

    # Filtra por presença em todas as provas e redação válida.
    df = df[
        (df['TP_PRESENCA_CN'] == 1) & (df['TP_PRESENCA_CH'] == 1) &
        (df['TP_PRESENCA_LC'] == 1) & (df['TP_PRESENCA_MT'] == 1) &
        (df['TP_STATUS_REDACAO'] == 1)
    ].copy()

    # Cria a nota média geral para cada estudante.
    df['NOTA_MEDIA_GERAL'] = df[notas_cols].mean(axis=1)

    # Mapeia cada UF para sua respectiva região geográfica, para análises agregadas.
    mapa_regioes = {
        'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
        'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
        'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
        'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
        'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
    }
    df['REGIAO'] = df['SG_UF_PROVA'].map(mapa_regioes)
    df.dropna(subset=['REGIAO'], inplace=True)
    # Converte para tipo categórico e ordena as regiões geograficamente (e por desempenho, geralmente).
    df['REGIAO'] = pd.Categorical(df['REGIAO'], categories=['Sudeste', 'Sul', 'Centro-Oeste', 'Nordeste', 'Norte'], ordered=True)

    print(f"Total de registros válidos para análise: {len(df)}")
    if df.empty: return

    # --- Parte 3: Geração dos 8 Tipos de Gráficos ---
    # Cria uma amostra para gráficos de dispersão, que podem ficar sobrecarregados.
    df_sample = df.sample(n=min(50000, len(df)))

     # 1. HISTOGRAMA
    print("[1/8] Gerando: Histograma das Notas por Região...")
    plt.figure(figsize=(12, 7)); sns.histplot(data=df.rename(columns={'REGIAO': 'Região'}), x='NOTA_MEDIA_GERAL', hue='Região', element='step', common_norm=False, linewidth=2); plt.title('Histograma: Distribuição da Nota Média Geral por Região', fontsize=16); plt.xlabel('Nota Média Geral'); plt.ylabel('Contagem de Estudantes'); plt.savefig(os.path.join(graficos_path, '01_histograma_desempenho_regiao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 2. BOXPLOT
    print("[2/8] Gerando: Boxplot do Desempenho por Região...")
    plt.figure(figsize=(12, 8)); sns.boxplot(data=df, x='REGIAO', y='NOTA_MEDIA_GERAL'); plt.title('Boxplot: Distribuição da Nota Média Geral por Região', fontsize=16); plt.xlabel('Região'); plt.ylabel('Nota Média Geral'); plt.savefig(os.path.join(graficos_path, '02_boxplot_desempenho_regiao.png'), dpi=300, bbox_inches='tight'); plt.show()

   
    # 4. GRÁFICO DE BARRAS
    print("[4/8] Gerando: Gráfico de Barras das Médias...")
    media_regiao = df.groupby('REGIAO', observed=True)[['NOTA_MEDIA_GERAL', 'NU_NOTA_REDACAO']].mean(); ax = media_regiao.plot(kind='bar', figsize=(10, 7), rot=0, title='Gráfico de Barras: Médias por Região', colormap='plasma'); plt.xlabel('Região'); plt.ylabel('Nota Média'); plt.legend(['Média Geral', 'Redação']); plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '04_barras_medias_regiao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 5. GRÁFICO DE LINHAS
    print("[5/8] Gerando: Gráfico de Linhas (média por estado)...")
    media_uf = df.groupby('SG_UF_PROVA')['NOTA_MEDIA_GERAL'].mean().sort_values(ascending=False); plt.figure(figsize=(18, 8)); media_uf.plot(kind='line', style='-o', title='Gráfico de Linhas: Desempenho Médio por UF da Prova'); plt.xlabel('Unidade da Federação'); plt.ylabel('Nota Média Geral'); plt.xticks(rotation=45, ha='right'); plt.grid(True, linestyle='--'); plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '05_linhas_desempenho_uf.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 6. HEATMAP DE CORRELAÇÃO
    print("[6/8] Gerando: Heatmap das Médias Regionais...")

    # Calcula a média das notas por região
    heatmap_data = df.groupby('REGIAO', observed=True)[notas_cols].mean()


    mapa_nomes_completos = {
        'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }
    # Aplica a renomeação
    heatmap_data.rename(columns=mapa_nomes_completos, inplace=True)

    # Gera o heatmap com os novos nomes
    plt.figure(figsize=(12, 7)) # Aumentei um pouco a largura para os novos rótulos
    sns.heatmap(heatmap_data, annot=True, cmap='cividis', fmt='.1f', linewidths=.5)
    plt.title('Heatmap: Desempenho Médio por Área e Região', fontsize=16)
    plt.xlabel('Área do Conhecimento', fontsize=12)
    plt.ylabel('Região', fontsize=12)


    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '06_heatmap_medias_regionais.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # 7. GRÁFICO DE DENSIDADE (KDE)
    print("[7/8] Gerando: Gráfico de Densidade das Notas por Região...")

    plt.figure(figsize=(12, 7)); sns.kdeplot(data=df.rename(columns={'REGIAO': 'Região'}), x='NOTA_MEDIA_GERAL', hue='Região', fill=True, common_norm=False); plt.title('Densidade: Distribuição da Nota Média Geral por Região', fontsize=16); plt.xlabel('Nota Média Geral'); plt.ylabel('Densidade'); plt.savefig(os.path.join(graficos_path, '07_densidade_notas_regiao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 8. GRÁFICO DE BARRAS EMPILHADAS
    print("[8/8] Gerando: Gráfico de Barras Empilhadas...")

    bins_desempenho = [0, 500, 600, 700, 1000]; labels_desempenho = ['Regular (<500)', 'Bom (500-600)', 'Muito Bom (600-700)', 'Excelente (>700)']; df['FAIXA_DESEMPENHO'] = pd.cut(df['NOTA_MEDIA_GERAL'], bins=bins_desempenho, labels=labels_desempenho); composicao = df.groupby('REGIAO', observed=True)['FAIXA_DESEMPENHO'].value_counts(normalize=True).unstack().fillna(0) * 100; ax = composicao.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='YlGnBu'); plt.title('Barras Empilhadas: Composição das Faixas de Desempenho por Região (%)', fontsize=16); plt.xlabel('Região'); plt.ylabel('Percentual de Estudantes (%)'); plt.xticks(rotation=0); plt.legend(title='Faixa de Desempenho', bbox_to_anchor=(1.02, 1)); plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '08_barras_empilhadas_desempenho.png'), dpi=300, bbox_inches='tight'); plt.show()

    
     # 3. GRÁFICO DE DISPERSÃO (Puro)
    print("[3/8] Gerando: Gráfico de Dispersão puro...")
    plt.figure(figsize=(12, 8)); sns.scatterplot(data=df_sample.rename(columns={'REGIAO': 'Região'}), x='NOTA_MEDIA_GERAL', y='NU_NOTA_REDACAO', hue='Região', alpha=0.3, s=20); plt.title('Dispersão: Nota Média Geral vs. Redação por Região (Amostra)', fontsize=16); plt.xlabel('Nota Média Geral'); plt.ylabel('Nota da Redação'); plt.legend(title='Região'); plt.savefig(os.path.join(graficos_path, '03_dispersao_media_redacao.png'), dpi=300, bbox_inches='tight'); plt.show()

if __name__ == "__main__":
    main()