#@title Código do Tema Desempenho

# --- 1. Importação das Bibliotecas Essenciais ---
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# --- 2. Configuração Inicial do Ambiente ---
# Define um estilo visual padrão para todos os gráficos gerados pelo Seaborn. 'whitegrid' é limpo e profissional.
sns.set_theme(style="whitegrid")

def main():

    # --- 3. Carregamento e Preparação dos Dados ---
    dados_path = 'DADOS'  # Define o diretório onde o arquivo CSV está localizado
    resultados_file = os.path.join(dados_path, 'RESULTADOS_2024.csv')  # Cria o caminho completo para o arquivo
    
    # Cria a pasta para salvar os gráficos
    graficos_path = 'graficos_desempenho'
    os.makedirs(graficos_path, exist_ok=True)

    # Lista das colunas que são relevantes para esta análise. Carregar apenas o necessário economiza memória.
    cols_wanted = [
        'NU_INSCRICAO', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
        'TP_STATUS_REDACAO', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'
    ]

    # Verificação de robustez: Checa se o arquivo de dados realmente existe antes de tentar lê-lo.
    if not os.path.isfile(resultados_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {resultados_file}")

    # Leitura otimizada do CSV:
    # 1. Lê apenas o cabeçalho (nrows=0) para obter a lista de colunas existentes no arquivo.
    hdrs = pd.read_csv(resultados_file, nrows=0, delimiter=';', encoding='latin1').columns
    # 2. Cria uma lista 'usecols' contendo apenas as colunas de 'cols_wanted' que de fato existem no arquivo.
    usecols = [c for c in cols_wanted if c in hdrs]
    # 3. Carrega o DataFrame usando apenas as colunas validadas, otimizando o processo.
    df = pd.read_csv(resultados_file, usecols=usecols, delimiter=';', encoding='latin1', low_memory=False)

    # --- 4. Filtragem dos Participantes Válidos ---
    # Cria uma máscara booleana para selecionar apenas os estudantes que:
    # - Compareceram a todas as 4 provas objetivas (presença = 1).
    # - Tiveram sua redação avaliada sem problemas (status = 1).
    pres_cols = ['TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'TP_STATUS_REDACAO']
    mask = pd.Series(True, index=df.index)  # Começa com todos os registros como True
    for col in pres_cols:
        if col in df.columns:
            mask &= (df[col] == 1)  # Atualiza a máscara, mantendo apenas os True onde a condição é atendida
    df = df.loc[mask].copy()  # Aplica a máscara e usa .copy() para evitar avisos e garantir um novo DataFrame.
    print(f"Registros após filtro de presença+redação: {len(df)}")

    # --- 5. Limpeza e Engenharia de Features ---
    # Converte as colunas de notas para o tipo numérico. 'errors='coerce'' transforma textos ou erros em NaN (Not a Number).
    obj_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']
    for c in obj_cols + ['NU_NOTA_REDACAO']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Validação para garantir que todas as colunas de notas objetivas foram encontradas no arquivo.
    if any(c not in df.columns for c in obj_cols):
        raise RuntimeError("Faltam colunas de notas objetivas obrigatórias para a análise.")

    # Cria uma nova coluna 'MEDIA_OBJETIVAS' calculando a média das notas das provas objetivas para cada aluno.
    # axis=1 indica que a média deve ser calculada horizontalmente (ao longo das colunas de cada linha).
    df['MEDIA_OBJETIVAS'] = df[obj_cols].mean(axis=1)

    # Remove qualquer linha que tenha valor NaN na média ou na redação, pois são inúteis para a correlação.
    df = df.dropna(subset=['MEDIA_OBJETIVAS', 'NU_NOTA_REDACAO']).reset_index(drop=True)
    if df.empty:
        raise RuntimeError("Nenhum registro válido restou após a limpeza das notas.")

    # --- 6. Análise Estatística ---
    # Calcula as correlações e a regressão linear entre a média das objetivas e a nota da redação.
    pearson_r, _ = stats.pearsonr(df['MEDIA_OBJETIVAS'], df['NU_NOTA_REDACAO']) # Correlação linear
    spearman_rho, _ = stats.spearmanr(df['MEDIA_OBJETIVAS'], df['NU_NOTA_REDACAO']) # Correlação monotônica (não necessariamente linear)
    lr = stats.linregress(df['MEDIA_OBJETIVAS'], df['NU_NOTA_REDACAO']) # Modelo de regressão linear simples

    # Imprime um resumo com os principais resultados estatísticos.
    print("\n--- Resumo da análise estatística ---")
    print(f"Total de registros analisados: {len(df)}")
    print(f"Correlação de Pearson (r): {pearson_r:.4f}")
    print(f"Correlação de Spearman (rho): {spearman_rho:.4f}")
    print(f"Coeficiente de Determinação (R²): {lr.rvalue**2:.4f}") # R² indica a % da variação da redação explicada pela média objetiva.
    print("--------------------------------------\n")

    # --- 7. Criação de Grupos para Análise Comparativa ---
    # `pd.qcut`: Divide os alunos em 4 grupos (quartis) de tamanho igual com base na média das objetivas.
    df['GRUPO_DESEMPENHO'] = pd.qcut(df['MEDIA_OBJETIVAS'], 4, labels=['Grupo 1 (25% piores)', 'Grupo 2', 'Grupo 3', 'Grupo 4 (25% melhores)'])

    # `pd.cut`: Divide os alunos em faixas de desempenho com base em intervalos de nota pré-definidos.
    obj_bins = [0, 500, 600, 700, 1000]
    obj_labels = ['<500', '500-600', '600-700', '>700']
    df['FAIXA_OBJETIVAS'] = pd.cut(df['MEDIA_OBJETIVAS'], bins=obj_bins, labels=obj_labels, include_lowest=True)
    red_bins = [0, 400, 600, 800, 1000]
    red_labels = ['<400', '400-600', '600-800', '>800']
    df['FAIXA_REDACAO'] = pd.cut(df['NU_NOTA_REDACAO'], bins=red_bins, labels=red_labels, include_lowest=True)

    # Renomeia as colunas de notas para criar rótulos mais amigáveis nos gráficos.
    df_renamed = df.rename(columns={
        'NU_NOTA_CN': 'Ciências da Natureza', 'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos', 'NU_NOTA_MT': 'Matemática', 'NU_NOTA_REDACAO': 'Redação'
    })

    # --- 8. Geração das Visualizações ---

    # Gráfico 1: HISTOGRAMA - Mostra a distribuição de frequência da média das notas objetivas.
    print("Gerando Histograma...")
    plt.figure(figsize=(9,5)); sns.histplot(df['MEDIA_OBJETIVAS'], bins=50, kde=True) # kde=True adiciona uma linha de densidade.
    plt.title('Distribuição da Média das Provas Objetivas'); plt.xlabel('Média das Notas Objetivas'); plt.ylabel('Contagem de Participantes')
    plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '01_histograma_media_objetivas.png'), dpi=300, bbox_inches='tight'); plt.show(); plt.close()

    # Gráfico 2: BOXPLOT - Compara a distribuição da nota de redação entre os 4 grupos de desempenho.
    print("Gerando Boxplot...")
    plt.figure(figsize=(9,5)); sns.boxplot(x='GRUPO_DESEMPENHO', y='NU_NOTA_REDACAO', data=df)
    plt.title('Distribuição das Notas de Redação por Grupo de Desempenho'); plt.xlabel('Grupo de Desempenho (Média Objetiva)'); plt.ylabel('Nota da Redação')
    plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '02_boxplot_redacao_grupos.png'), dpi=300, bbox_inches='tight'); plt.show(); plt.close()

    
    # Gráfico 4: BARRAS - Compara a nota média (objetivas e redação) de cada grupo de desempenho.
    print("Gerando Gráfico de Barras com Legenda Clara...")
    media_q = df.groupby('GRUPO_DESEMPENHO', observed=True)[['MEDIA_OBJETIVAS', 'NU_NOTA_REDACAO']].mean()
    media_q.rename(columns={'MEDIA_OBJETIVAS': 'Média das Provas Objetivas', 'NU_NOTA_REDACAO': 'Nota da Redação'}, inplace=True)
    media_q.plot(kind='bar', figsize=(10, 6))
    plt.title('Médias por Grupo de Desempenho', fontsize=16)
    plt.xlabel('Grupo de Desempenho', fontsize=12)
    plt.ylabel('Nota Média', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Componente da Nota', fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '04_barras_medias_grupos.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # Gráfico 5: LINHAS
    print("Gerando Gráfico de Linhas (Tendência)...")
    trend = media_q.reset_index()
    plt.figure(figsize=(10,6))
    plt.plot(trend['GRUPO_DESEMPENHO'].astype(str), trend['Média das Provas Objetivas'], marker='o', linestyle='--', label='Média das Provas Objetivas')
    plt.plot(trend['GRUPO_DESEMPENHO'].astype(str), trend['Nota da Redação'], marker='s', label='Nota da Redação')
    plt.title('Tendência das Notas Médias por Grupo de Desempenho', fontsize=16)
    plt.xlabel('Grupo de Desempenho', fontsize=12)
    plt.ylabel('Nota Média', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, '05_linhas_tendencia.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # Gráfico 6: HEATMAP - Exibe a matriz de correlação entre todas as notas (incluindo as 4 objetivas e a redação).
    print("Gerando Heatmap de Correlação...")
    notas_renamed = ['Ciências da Natureza','Ciências Humanas','Linguagens e Códigos','Matemática','Redação']
    corr = df_renamed[notas_renamed].corr()
    plt.figure(figsize=(8,6)); sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5) # annot=True mostra os valores
    plt.title('Matriz de Correlação entre as Notas das Provas'); plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '06_heatmap_correlacao.png'), dpi=300, bbox_inches='tight'); plt.show(); plt.close()

    # Gráfico 7: DENSIDADE (KDE) - Compara a forma da distribuição da média objetiva com a da redação.
    print("Gerando Gráfico de Densidade...")
    plt.figure(figsize=(9,5)); sns.kdeplot(df['MEDIA_OBJETIVAS'], fill=True, label='Média Objetivas'); sns.kdeplot(df['NU_NOTA_REDACAO'], fill=True, label='Redação')
    plt.title('Comparação da Distribuição de Densidade das Notas'); plt.xlabel('Nota'); plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '07_densidade_distribuicao.png'), dpi=300, bbox_inches='tight'); plt.show(); plt.close()

    # Gráfico 8: BARRAS EMPILHADAS - Mostra, para cada faixa de desempenho nas objetivas, a composição percentual das faixas da redação.
    print("Gerando Gráfico de Barras Empilhadas...")
    # 'normalize=True' calcula as proporções. Multiplicamos por 100 para ter percentuais.
    comp = df.groupby('FAIXA_OBJETIVAS', observed=True)['FAIXA_REDACAO'].value_counts(normalize=True).unstack(fill_value=0) * 100
    ax = comp.plot(kind='bar', stacked=True, figsize=(10,7), title='Composição das Notas de Redação por Faixa de Desempenho nas Objetivas (%)')
    ax.set(xlabel='Faixa de Desempenho (Objetivas)', ylabel='Percentual (%)')
    plt.legend(title='Faixa da Redação', bbox_to_anchor=(1.02,1)); plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '08_barras_empilhadas_composicao.png'), dpi=300, bbox_inches='tight'); plt.show(); plt.close()

    
    # Gráfico 3: DISPERSÃO + REGRESSÃO LINEAR - Visualização central para a pergunta de pesquisa.
    print("Gerando Gráfico de Dispersão...")
    plt.figure(figsize=(9,6)); sns.regplot(x='MEDIA_OBJETIVAS', y='NU_NOTA_REDACAO', data=df,
                                           scatter_kws={'alpha':0.2}, line_kws={'color':'red'}) # alpha deixa os pontos semi-transparentes
    plt.title('Relação entre Média Objetiva e Nota da Redação'); plt.xlabel('Média das Notas Objetivas'); plt.ylabel('Nota da Redação')
    # Adiciona uma caixa de texto no gráfico com os resultados estatísticos mais importantes.
    plt.annotate(f"Correlação (Pearson) r = {pearson_r:.3f}\nCoeficiente de Determinação R² = {lr.rvalue**2:.3f}",
                 xy=(0.05, 0.95), xycoords='axes fraction', va='top', bbox=dict(boxstyle='round', fc='wheat', alpha=0.7))
    plt.tight_layout(); plt.savefig(os.path.join(graficos_path, '03_dispersao_correlacao.png'), dpi=300, bbox_inches='tight'); plt.show(); plt.close()


if __name__ == "__main__":
    # Este bloco garante que a função main() só será executada quando o script for rodado diretamente.
    main()
