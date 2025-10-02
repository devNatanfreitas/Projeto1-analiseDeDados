"""## Tema Acadêmico


**Pergunta de Pesquisa:** Qual o impacto da dependência administrativa da escola de conclusão (Federal, Estadual, Municipal, Privada) no desempenho médio dos estudantes nas diferentes áreas de conhecimento do ENEM 2024?
"""

#@title Código do Tema Acadêmico
# --- Importação das Bibliotecas ---
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():

    # --- Configuração Inicial ---
    dados_path = 'DADOS'
    dados_enem_file = os.path.join(dados_path, 'RESULTADOS_2024.csv')
    sns.set_theme(style="whitegrid") # Define o estilo dos gráficos.
    
    # Cria a pasta para salvar os gráficos
    graficos_path = 'graficos_academico'
    os.makedirs(graficos_path, exist_ok=True)

    # --- Parte 1: Carregar Dados do CSV ---
    print(f"\n--- Parte 1: Carregando Dados do arquivo: {dados_enem_file} ---")
    try:
        df_resultados = pd.read_csv(dados_enem_file, encoding='latin1', delimiter=';')
        print(f"Dados carregados com sucesso: {len(df_resultados)} registros.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{dados_enem_file}' não encontrado.")
        return
    except Exception as e:
        print(f"ERRO ao carregar o arquivo CSV: {e}")
        return
    if df_resultados.empty:
        print("DataFrame está vazio. Finalizando.")
        return

    # --- Parte 2: Limpar e Preparar os Dados ---
    print("\n--- Parte 2: Limpeza e Preparação dos Dados ---")

    # Filtra o DataFrame para incluir apenas estudantes que:
    # 1. Têm tipo de escola declarado (códigos 1 a 4).
    # 2. Estiveram presentes em todas as 4 provas objetivas.
    # 3. Tiveram a redação avaliada (status 1 = sem problemas).
    df_presentes = df_resultados[
        (df_resultados['TP_DEPENDENCIA_ADM_ESC'].isin([1, 2, 3, 4])) &
        (df_resultados['TP_PRESENCA_CN'] == 1) &
        (df_resultados['TP_PRESENCA_CH'] == 1) &
        (df_resultados['TP_PRESENCA_LC'] == 1) &
        (df_resultados['TP_PRESENCA_MT'] == 1) &
        (df_resultados['TP_STATUS_REDACAO'] == 1)
    ].copy() # .copy() evita o SettingWithCopyWarning.

    # Remove aspas duplas dos nomes das colunas, caso existam.
    df_presentes.columns = df_presentes.columns.str.replace('"', '')
    # Lista de colunas de notas para facilitar a manipulação.
    notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    # Remove qualquer linha que tenha valor nulo em qualquer uma das colunas de nota.
    df_presentes.dropna(subset=notas_cols, inplace=True)

    # Mapeia os códigos de dependência da escola para textos e define uma ordem lógica.
    mapa_dependencia = {1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'}
    ordem_escolas = ['Federal', 'Privada', 'Estadual', 'Municipal'] # Ordena por desempenho esperado.
    df_presentes['TIPO_ESCOLA'] = df_presentes['TP_DEPENDENCIA_ADM_ESC'].map(mapa_dependencia)
    df_presentes['TIPO_ESCOLA'] = pd.Categorical(df_presentes['TIPO_ESCOLA'], categories=ordem_escolas, ordered=True)

    # Calcula a média geral das notas de cada estudante para análises agregadas.
    df_presentes['NOTA_MEDIA_GERAL'] = df_presentes[notas_cols].mean(axis=1)

    print(f"Registros válidos para análise: {len(df_presentes)}.")

    # --- Parte 3: Análise Descritiva ---
    print("\n--- Parte 3: Análise Descritiva por Tipo de Escola ---")
    # Calcula e exibe a média de cada prova, agrupada por tipo de escola.
    estatisticas_por_escola = df_presentes.groupby('TIPO_ESCOLA')[notas_cols].mean().round(2)
    print("\nMédia das Notas por Tipo de Escola:")
    print(estatisticas_por_escola)

    # --- Parte 4: Visualização Completa dos Resultados ---
    print("\n--- Parte 4: Visualização dos Resultados ---")

    # 1. GRÁFICO DE BARRAS: Compara as notas médias de cada área de conhecimento por tipo de escola.
    print("[1/8] Gerando: Gráfico de Barras (Médias por Área)...")
    media_por_escola = df_presentes.groupby('TIPO_ESCOLA')[notas_cols].mean()
    # Mapeia nomes técnicos das colunas para nomes amigáveis para a legenda.
    mapa_nomes_notas = {
        'NU_NOTA_CN': 'Ciências da Natureza', 'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos', 'NU_NOTA_MT': 'Matemática', 'NU_NOTA_REDACAO': 'Redação'
    }
    media_por_escola.rename(columns=mapa_nomes_notas, inplace=True)
    # Plota as médias. O pandas cria um gráfico de barras agrupado automaticamente.
    media_por_escola.plot(kind='bar', figsize=(16, 9), colormap='viridis')
    plt.title('Gráfico de Barras: Média de Notas por Área e Dependência da Escola', fontsize=16)
    plt.xlabel('Dependência Administrativa da Escola', fontsize=12)
    plt.ylabel('Nota Média', fontsize=12)
    plt.xticks(rotation=0) # Mantém os nomes das escolas na horizontal.
    plt.legend(title='Área de Conhecimento')
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '01_barras_notas_medias.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # 2. BOXPLOT: Analisa a distribuição (mediana, quartis, outliers) das notas de Matemática e Redação.
    print("[2/8] Gerando: Boxplots (Distribuição de Notas)...")
    fig, axes = plt.subplots(1, 2, figsize=(18, 8)) # Dois gráficos lado a lado.
    sns.boxplot(ax=axes[0], data=df_presentes, x='TIPO_ESCOLA', y='NU_NOTA_MT', palette='viridis')
    axes[0].set_title('Distribuição da Nota de Matemática por Tipo de Escola')
    axes[0].set_xlabel('Dependência da Escola'), axes[0].set_ylabel('Nota de Matemática')
    sns.boxplot(ax=axes[1], data=df_presentes, x='TIPO_ESCOLA', y='NU_NOTA_REDACAO', palette='viridis')
    axes[1].set_title('Distribuição da Nota de Redação por Tipo de Escola')
    axes[1].set_xlabel('Dependência da Escola'), axes[1].set_ylabel('Nota de Redação')
    plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '02_boxplots_distribuicao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 3. HISTOGRAMA: Mostra a frequência das notas médias gerais para cada tipo de escola.
    print("[3/8] Gerando: Histograma (Distribuição da Nota Média Geral)...")
    plt.figure(figsize=(12, 7))
    # Renomeia a coluna 'TIPO_ESCOLA' temporariamente para ter um título de legenda mais limpo ("Tipo de Escola").
    df_temp_plot_hist = df_presentes.rename(columns={'TIPO_ESCOLA': 'Tipo de Escola'})
    # 'element=step' cria um histograma de linhas, que é melhor para comparar distribuições.
    sns.histplot(data=df_temp_plot_hist, x='NOTA_MEDIA_GERAL', hue='Tipo de Escola', element='step', common_norm=False, palette='viridis')
    plt.title('Histograma: Distribuição da Nota Média Geral por Tipo de Escola')
    plt.xlabel('Nota Média Geral'), plt.ylabel('Contagem de Estudantes')
    plt.legend(title='Tipo de Escola', labels=ordem_escolas) # Garante que a legenda esteja correta.
    plt.savefig(os.path.join(graficos_path, '03_histograma_nota_media.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 4. GRÁFICO DE DENSIDADE (KDE): Visão suavizada da distribuição da nota média geral.
    print("[4/8] Gerando: Gráfico de Densidade (Distribuição da Nota Média Geral)...")
    plt.figure(figsize=(12, 7))
    df_temp_plot_kde = df_presentes.rename(columns={'TIPO_ESCOLA': 'Tipo de Escola'})
    sns.kdeplot(data=df_temp_plot_kde, x='NOTA_MEDIA_GERAL', hue='Tipo de Escola', fill=True, common_norm=False, palette='viridis')
    plt.title('Gráfico de Densidade: Distribuição da Nota Média Geral por Tipo de Escola')
    plt.xlabel('Nota Média Geral'), plt.ylabel('Densidade')
    plt.savefig(os.path.join(graficos_path, '04_densidade_nota_media.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 5. GRÁFICO DE BARRAS EMPILHADAS: Mostra a composição de faixas de desempenho dentro de cada tipo de escola.
    print("[5/8] Gerando: Gráfico de Barras Empilhadas (Faixas de Desempenho)...")
    # Cria faixas de desempenho ('bins') usando a nota média geral.
    bins = [0, 450, 600, 750, 1000]
    labels = ['Baixo (<450)', 'Médio (450-600)', 'Bom (600-750)', 'Excelente (>750)']
    df_presentes['FAIXA_DESEMPENHO'] = pd.cut(df_presentes['NOTA_MEDIA_GERAL'], bins=bins, labels=labels, right=False)
    # Calcula a porcentagem de alunos em cada faixa, por tipo de escola.
    dados_empilhados = df_presentes.groupby('TIPO_ESCOLA')['FAIXA_DESEMPENHO'].value_counts(normalize=True).unstack().fillna(0) * 100
    dados_empilhados = dados_empilhados[labels] # Garante a ordem correta das faixas.
    ax = dados_empilhados.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='tab20c')
    plt.title('Barras Empilhadas: Composição do Desempenho por Dependência da Escola (%)')
    plt.xlabel('Dependência da Escola'), plt.ylabel('Percentual de Estudantes (%)')
    plt.xticks(rotation=0), plt.legend(title='Faixa de Desempenho', bbox_to_anchor=(1.02, 1)), plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '05_barras_empilhadas_desempenho.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 6. HEATMAP DE CORRELAÇÃO: Mostra a correlação entre as notas das diferentes áreas do conhecimento.
    print("[6/8] Gerando: Heatmap de Correlação entre as Notas...")
    correlation_matrix = df_presentes[notas_cols].corr()
    correlation_matrix.rename(columns=mapa_nomes_notas, index=mapa_nomes_notas, inplace=True) # Renomeia eixos para clareza.
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap: Correlação entre as Notas das Diferentes Áreas'), plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '06_heatmap_correlacao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 7. GRÁFICO DE DISPERSÃO: Relaciona as notas de Matemática e Linguagens, colorindo por tipo de escola.
    print("[7/8] Gerando: Gráfico de Dispersão (Matemática vs. Linguagens)...")
    # Usa uma amostra aleatória dos dados para evitar um gráfico muito poluído e lento.
    amostra_df = df_presentes.sample(n=min(5000, len(df_presentes)), random_state=42)
    plt.figure(figsize=(12, 8))
    amostra_temp_plot = amostra_df.rename(columns={'TIPO_ESCOLA': 'Tipo de Escola'}) # Renomeia para a legenda.
    sns.scatterplot(data=amostra_temp_plot, x='NU_NOTA_MT', y='NU_NOTA_LC', hue='Tipo de Escola', palette='viridis', alpha=0.7)
    plt.title('Gráfico de Dispersão: Nota de Matemática vs. Nota de Linguagens por Tipo de Escola (Amostra)')
    plt.xlabel('Nota de Matemática'), plt.ylabel('Nota de Linguagens e Códigos')
    plt.savefig(os.path.join(graficos_path, '07_dispersao_matematica_linguagens.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 8. GRÁFICO DE LINHAS: Mostra a proporção de cada tipo de escola dentro de cada faixa de desempenho.
    print("[8/8] Gerando: Gráfico de Linhas (Composição por Faixa de Desempenho)...")
    df_temp_plot_line = df_presentes.rename(columns={'TIPO_ESCOLA': 'Tipo de Escola'})
    # Calcula a proporção (normalize=True) de cada tipo de escola DENTRO de cada faixa de desempenho.
    composicao_por_faixa = df_temp_plot_line.groupby('FAIXA_DESEMPENHO')['Tipo de Escola'].value_counts(normalize=True).unstack().fillna(0) * 100
    # Plota a evolução dessas proporções ao longo das faixas de desempenho.
    ax = composicao_por_faixa[ordem_escolas].plot(kind='line', marker='o', figsize=(16, 8), colormap='viridis')
    plt.title('Gráfico de Linhas: Proporção de Cada Tipo de Escola por Faixa de Desempenho', fontsize=16)
    plt.xlabel('Faixa de Desempenho (Nota Média Geral)', fontsize=12)
    plt.ylabel('Percentual de Estudantes na Faixa (%)', fontsize=12)
    plt.legend(title='Tipo de Escola')
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '08_linhas_composicao_faixas.png'), dpi=300, bbox_inches='tight'); plt.show()
    print("\nAnálise completa com 8 tipos de gráficos foi concluída!")

if __name__ == "__main__":
    main()

