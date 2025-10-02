# -*- coding: utf-8 -*-
#@title Código do Tema Socioeconômico


import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.lines import Line2D

def main():


    # --- Configuração Inicial ---
    # Define o caminho base onde os arquivos de dados estão localizados.
    dados_path = 'DADOS'
    # Constrói o caminho completo para o arquivo CSV dos participantes.
    dados_enem_file = os.path.join(dados_path, 'PARTICIPANTES_2024.csv')
    
    # Cria o diretório para salvar os gráficos
    graficos_path = 'graficos_socieconomico'
    os.makedirs(graficos_path, exist_ok=True)
    # Define um tema visual padrão para todos os gráficos gerados pelo Seaborn.
    sns.set_theme(style="whitegrid")

    # --- Parte 1: Carregar os Dados do CSV ---
    print("\n--- Parte 1: Carregando Dados ---")
    try:
        # Tenta ler o arquivo CSV. 'encoding' lida com caracteres especiais do português. 'delimiter' define o separador.
        df = pd.read_csv(dados_enem_file, encoding='latin1', delimiter=';')
        print(f"Dados carregados com sucesso: {len(df)} registros.")
    except FileNotFoundError:
        # Se o arquivo não for encontrado, exibe uma mensagem de erro clara.
        print(f"ERRO: Arquivo '{dados_enem_file}' não encontrado.")
        print("Verifique se o caminho está correto e o Google Drive montado.")
        return
    except Exception as e:
        # Captura qualquer outro erro que possa ocorrer durante a leitura do arquivo.
        print(f"ERRO ao carregar o arquivo CSV: {e}")
        return

    # Validação para garantir que o DataFrame não está vazio após a carga.
    if df.empty:
        print("DataFrame está vazio. Finalizando.")
        return

    # --- Parte 2: Decodificação e Preparação dos Dados ---
    print("\n--- Parte 2: Decodificando e preparando os dados para análise ---")

    # Dicionários de mapeamento: traduzem os códigos do dataset para valores textuais legíveis.
    mapa_cor_raca = {0: 'Não declarado', 1: 'Branca', 2: 'Preta', 3: 'Parda', 4: 'Amarela', 5: 'Indígena', 6: 'Não dispõe da informação'}
    mapa_escolaridade = {'A': 'Nunca estudou', 'B': 'Fund. I Incompleto', 'C': 'Fund. II Incompleto', 'D': 'Médio Incompleto', 'E': 'Médio Completo', 'F': 'Superior Completo', 'G': 'Pós-graduação', 'H': 'Não sei'}
    mapa_ocupacao = {'A': 'Grupo 1 (Agricultor)', 'B': 'Grupo 2 (Doméstico)', 'C': 'Grupo 3 (Qualificado)', 'D': 'Grupo 4 (Técnico)', 'E': 'Grupo 5 (Superior)', 'F': 'Não sei'}
    mapa_renda_familiar = { 'A': 'Nenhuma Renda', 'B': 'Até 1 Salário Min.', 'C': '1-1.5 Salário Min.', 'D': '1.5-2 Salário Min.', 'E': '2-2.5 Salário Min.', 'F': '2.5-3 Salário Min.', 'G': '3-4 Salário Min.', 'H': '4-5 Salário Min.', 'I': '5-6 Salário Min.', 'J': '6-7 Salário Min.', 'K': '7-8 Salário Min.', 'L': '8-9 Salário Min.', 'M': '9-10 Salário Min.', 'N': '10-12 Salário Min.', 'O': '12-15 Salário Min.', 'P': '15-20 Salário Min.', 'Q': 'Acima de 20 Salário Min.' }

    # Aplica os mapeamentos para criar novas colunas com os valores decodificados.
    df['COR_RACA'] = df['TP_COR_RACA'].map(mapa_cor_raca)
    df['ESCOLARIDADE_PAI'] = df['Q001'].map(mapa_escolaridade)
    df['ESCOLARIDADE_MAE'] = df['Q002'].map(mapa_escolaridade)
    df['OCUPACAO_PAI'] = df['Q003'].map(mapa_ocupacao)
    df['OCUPACAO_MAE'] = df['Q004'].map(mapa_ocupacao)
    df['RENDA_FAMILIAR'] = df['Q007'].map(mapa_renda_familiar) # A coluna Q007 não estava no seu código, adicionei como exemplo

    # Define uma ordem lógica para as categorias. Isso garante que os gráficos (ex: eixos, legendas) sejam exibidos na ordem correta.
    ordem_raca = ['Branca', 'Parda', 'Preta', 'Amarela', 'Indígena']
    ordem_escolaridade = list(mapa_escolaridade.values())
    ordem_ocupacao = list(mapa_ocupacao.values())
    ordem_renda = list(mapa_renda_familiar.values())

    # Converte as colunas para o tipo 'Categorical' com a ordem definida, o que melhora a performance e a visualização.
    df['COR_RACA'] = pd.Categorical(df['COR_RACA'], categories=ordem_raca, ordered=True)
    df['ESCOLARIDADE_PAI'] = pd.Categorical(df['ESCOLARIDADE_PAI'], categories=ordem_escolaridade, ordered=True)
    df['ESCOLARIDADE_MAE'] = pd.Categorical(df['ESCOLARIDADE_MAE'], categories=ordem_escolaridade, ordered=True)
    df['OCUPACAO_PAI'] = pd.Categorical(df['OCUPACAO_PAI'], categories=ordem_ocupacao, ordered=True)
    df['OCUPACAO_MAE'] = pd.Categorical(df['OCUPACAO_MAE'], categories=ordem_ocupacao, ordered=True)
    df['RENDA_FAMILIAR'] = pd.Categorical(df['RENDA_FAMILIAR'], categories=ordem_renda, ordered=True)

    # Inicia a limpeza dos dados para análise.
    # Remove registros com 'COR_RACA' nula ou não declarada/informada.
    df_filtrado = df.dropna(subset=['COR_RACA'])
    df_filtrado = df_filtrado[~df_filtrado['COR_RACA'].isin(['Não declarado', 'Não dispõe da informação'])]

    # Itera sobre as colunas socioeconômicas para remover valores nulos e respostas "Não sei".
    for col in ['ESCOLARIDADE_PAI', 'ESCOLARIDADE_MAE', 'OCUPACAO_PAI', 'OCUPACAO_MAE', 'RENDA_FAMILIAR']:
        df_filtrado = df_filtrado.dropna(subset=[col])
        df_filtrado = df_filtrado[~df_filtrado[col].isin(['Não sei'])]

    # Renomeia a coluna para uma legenda mais amigável nos gráficos.
    df_filtrado = df_filtrado.rename(columns={'COR_RACA': 'Cor/Raça'})

    # Cria uma cópia numérica do DataFrame. Gráficos como heatmap, boxplot e scatterplot necessitam de valores numéricos.
    df_numeric = df_filtrado.copy()
    for col in df_filtrado.select_dtypes(include=['category']).columns:
        # A propriedade .cat.codes converte as categorias ordenadas em códigos inteiros (0, 1, 2...).
        df_numeric[f'{col}_COD'] = df_filtrado[col].cat.codes

    print(f"Total de registros válidos para análise: {len(df_filtrado)}")

    # --- Parte 3: Geração dos 8 Tipos de Gráficos ---

    # 1. HISTOGRAMA: Ideal para ver a frequência e distribuição dos dados.
    print("\n[1/8] Gerando: Histograma (Distribuição da Renda)...")
    plt.figure(figsize=(15, 8)) 
    sns.histplot(
        data=df_numeric,          
        x='RENDA_FAMILIAR_COD',   
        hue='Cor/Raça',           
        multiple='stack',         
        palette='cubehelix',      
        discrete=True,            
        edgecolor='white',        
        linewidth=0.5             
    )
    plt.title('Distribuição da renda familiar por cor/raça', fontsize=16)
    plt.xlabel('Nível de renda familiar', fontsize=12)
    plt.ylabel('Número de estudantes', fontsize=12)
    plt.xticks(ticks=range(len(ordem_renda)), labels=ordem_renda, rotation=70, ha='right', fontsize=11)
    plt.yticks(fontsize=11)
    plt.tight_layout() 
    plt.savefig(os.path.join(graficos_path, '01_histograma_renda_familiar.png'), dpi=300, bbox_inches='tight')
    plt.show()         
    plt.close()

    # 2. BOXPLOT: Excelente para comparar a distribuição de uma variável numérica entre diferentes categorias.
    print("[2/8] Gerando: Boxplots (Comparativo Socioeconômico Parental)...")
    # Cria uma figura com 4 subplots (2 linhas, 2 colunas).
    fig, axes = plt.subplots(2, 2, figsize=(18, 14), sharex=True) # sharex=True compartilha o eixo x entre os subplots.
    parental_vars = { # Dicionário para facilitar a iteração e criação dos 4 boxplots.
        'Escolaridade da mãe': ('ESCOLARIDADE_MAE_COD', ordem_escolaridade),
        'Escolaridade do pai': ('ESCOLARIDADE_PAI_COD', ordem_escolaridade),
        'Ocupação da mãe': ('OCUPACAO_MAE_COD', ordem_ocupacao),
        'Ocupação do pai': ('OCUPACAO_PAI_COD', ordem_ocupacao)
    }
    # Itera sobre as variáveis e gera um boxplot para cada uma.
    for i, (title, (var_cod, labels)) in enumerate(parental_vars.items()):
        ax = axes.flatten()[i] # Seleciona o subplot atual. flatten() transforma a matriz de eixos em um array 1D.
        sns.boxplot(ax=ax, data=df_numeric, x='Cor/Raça', y=var_cod, palette='plasma') # Cria o boxplot.
        ax.set_title(f'Distribuição de {title} por cor/raça') # Define o título do subplot.
        ax.set_xlabel('Cor/Raça') # Define o rótulo do eixo x.
        ax.set_ylabel('Nível (código numérico)') # O eixo Y usa o código numérico.
        ax.set_yticks(ticks=range(len(labels)), labels=labels) # Mas os rótulos são os textos correspondentes.
        ax.tick_params(axis='x', rotation=45) # Rotaciona os ticks do eixo x para melhor legibilidade.
    fig.suptitle('Comparativo socioeconômico parental por cor/raça', fontsize=16, y=0.95) # Título principal da figura.
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta layout com espaço para o título principal.
    plt.savefig(os.path.join(graficos_path, '02_boxplots_socieconomico_parental.png'), dpi=300, bbox_inches='tight')
    plt.show() # Exibe a figura.
    plt.close() # Fecha a figura.


    # 4. GRÁFICO DE BARRAS: Ótimo para comparar contagens de categorias.
    print("[4/8] Gerando: Gráficos de Barras (Escolaridade Parental)...")
    fig, axes = plt.subplots(1, 2, figsize=(22, 10), sharey=False) # 1 linha, 2 colunas. sharey=False permite diferentes escalas no eixo y.

    # Gráfico da Esquerda (Mãe)
    sns.countplot( # sns.countplot conta as ocorrências de cada categoria.
        ax=axes[0],
        data=df_filtrado,
        y='ESCOLARIDADE_MAE', # Variável no eixo y (categórica).
        hue='Cor/Raça',       # Variável para segmentar as barras.
        palette='viridis'     # Paleta de cores.
    )
    axes[0].set_title('Escolaridade da mãe por cor/raça', fontsize=14)
    axes[0].set_xlabel('Número de estudantes', fontsize=12)
    axes[0].set_ylabel('Nível de escolaridade da mãe', fontsize=12)
    axes[0].legend(title='Cor/Raça') # Adiciona a legenda.
    axes[0].tick_params(axis='y', labelsize=11) # Define o tamanho da fonte dos ticks do eixo y.

    # Gráfico da Direita (Pai)
    sns.countplot( # Mesma lógica para o pai.
        ax=axes[1],
        data=df_filtrado,
        y='ESCOLARIDADE_PAI',
        hue='Cor/Raça',
        palette='viridis'
    )
    axes[1].set_title('Escolaridade do pai por cor/raça', fontsize=14)
    axes[1].set_xlabel('Número de estudantes', fontsize=12)
    axes[1].set_ylabel('Nível de escolaridade do pai', fontsize=12)
    axes[1].tick_params(axis='y', labelsize=11)
    axes[1].get_legend().remove() # Remove a legenda duplicada no segundo subplot.

    fig.suptitle('Comparativo da escolaridade parental por cor/raça', fontsize=16, y=0.95) # Título principal da figura.
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta layout com espaço para o título principal.
    plt.savefig(os.path.join(graficos_path, '04_graficos_barras_escolaridade.png'), dpi=300, bbox_inches='tight')
    plt.show() # Exibe a figura.
    plt.close() # Fecha a figura.

    # 5. GRÁFICO DE LINHAS: Mostra tendências ou comparações entre categorias ordenadas.
    print("[5/8] Gerando: Gráficos de Linhas (Evolução da Escolaridade Parental)...")

    fig, axes = plt.subplots(1, 2, figsize=(22, 8), sharey=True) # 1 linha, 2 colunas. sharey=True compartilha o eixo y.

    # Gráfico da Esquerda (Mãe)
    # Agrupa os dados para calcular a proporção (%) de cada nível de escolaridade por raça.
    data_mae = df_filtrado.groupby('Cor/Raça', observed=True)['ESCOLARIDADE_MAE'].value_counts(normalize=True).unstack().fillna(0) * 100
    # .T transpõe a matriz para que os níveis de escolaridade fiquem no eixo x e as raças sejam as linhas.
    data_mae.T.plot(kind='line', style='-o', ax=axes[0], colormap='viridis') # kind='line' especifica o tipo de gráfico. style define o marcador e linha.

    axes[0].set_title('% de mães por nível de escolaridade', fontsize=14)
    axes[0].set_xlabel('Nível de escolaridade da mãe', fontsize=12)
    axes[0].set_ylabel('Percentual de estudantes (%)', fontsize=12)
    axes[0].grid(True, linestyle='--', alpha=0.6) # Adiciona um grid leve.
    plt.setp(axes[0].get_xticklabels(), rotation=70, ha="right") # Rota os rótulos do eixo x.

    # Gráfico da Direita (Pai)
    # Repete o processo para o pai.
    data_pai = df_filtrado.groupby('Cor/Raça', observed=True)['ESCOLARIDADE_PAI'].value_counts(normalize=True).unstack().fillna(0) * 100
    data_pai.T.plot(kind='line', style='-s', ax=axes[1], colormap='viridis')

    axes[1].set_title('% de pais por nível de escolaridade', fontsize=14)
    axes[1].set_xlabel('Nível de escolaridade do pai', fontsize=12)
    axes[1].get_legend().remove() # Remove a legenda duplicada.
    axes[1].grid(True, linestyle='--', alpha=0.6)
    plt.setp(axes[1].get_xticklabels(), rotation=70, ha="right")

    fig.suptitle('Comparativo da evolução da escolaridade parental por cor/raça', fontsize=16, y=0.95) # Título principal.
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(graficos_path, '05_graficos_linhas_evolucao_escolaridade.png'), dpi=300, bbox_inches='tight')
    plt.show() # Exibe a figura.
    plt.close() # Fecha a figura.

    # 6. HEATMAP DE CORRELAÇÃO: Visualiza a força da relação entre variáveis numéricas.
    print("[6/8] Gerando: Heatmap de Correlação...")
    # Lista das colunas numéricas (códigos) para calcular a correlação.
    corr_cols = ['RENDA_FAMILIAR_COD', 'ESCOLARIDADE_MAE_COD', 'ESCOLARIDADE_PAI_COD', 'OCUPACAO_MAE_COD', 'OCUPACAO_PAI_COD', 'Cor/Raça_COD']
    # Calcula a matriz de correlação. 'spearman' é adequado para variáveis ordinais (como as nossas).
    correlation_matrix = df_numeric[corr_cols].corr(method='spearman')
    plt.figure(figsize=(12, 9))
    # sns.heatmap gera o mapa de calor. annot=True exibe os valores de correlação no mapa. cmap define o esquema de cores.
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 12}) # fmt formata os valores. annot_kws ajusta o tamanho da fonte dos valores.
    labels = ['Renda familiar', 'Escolaridade mãe', 'Escolaridade pai', 'Ocupação mãe', 'Ocupação pai', 'Cor/raça'] # Rótulos para os eixos.
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation=45, ha='right', fontsize=12) # Define e rotaciona os ticks do eixo x.
    plt.yticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation=0, fontsize=12) # Define os ticks do eixo y.
    plt.title('Correlação entre fatores socioeconômicos', fontsize=16)
    plt.tight_layout() # Ajusta layout.
    plt.savefig(os.path.join(graficos_path, '06_heatmap_correlacao.png'), dpi=300, bbox_inches='tight')
    plt.show() # Exibe.
    plt.close() # Fecha.

    
    # 7. GRÁFICO DE DENSIDADE (KDE) - VERSÃO CORRIGIDA E ROBUSTA
    print("[7/8] Gerando: Gráfico de Densidade (Distribuição da Renda)...")

    # Define o tamanho da figura
    plt.figure(figsize=(16, 8))



    # Pega as categorias únicas de 'Cor/Raça' que realmente existem nos dados
    categorias_presentes = df_numeric['Cor/Raça'].cat.categories

    # Pega a paleta de cores que o Seaborn usaria. 'crest' com o número exato de categorias.
    cores = sns.color_palette('crest', n_colors=len(categorias_presentes))

    # Desenha o gráfico de densidade sem a legenda automática do Seaborn
    ax = sns.kdeplot(
        data=df_numeric,
        x='RENDA_FAMILIAR_COD',
        hue='Cor/Raça',
        fill=True,
        common_norm=False,
        palette=cores,      # Usa a paleta que definimos
        legend=False        # Desabilita explicitamente a legenda do Seaborn
    )

    # Cria os "handles" (as alças visuais da legenda) manualmente.
    # Usamos `Patch` do `matplotlib.patches` para criar pequenos retângulos coloridos.
    from matplotlib.patches import Patch
    handles_da_legenda = [
        Patch(facecolor=cor, label=rotulo) for rotulo, cor in zip(categorias_presentes, cores)
    ]

    # Agora, cria a legenda usando os handles manuais
    plt.legend(
        title='Cor/Raça',
        handles=handles_da_legenda,
        bbox_to_anchor=(1.02, 1),
        loc='upper left'
    )
   

    # Configura o resto do gráfico
    plt.title('Distribuição de densidade da renda familiar por cor/raça', fontsize=16)
    plt.xlabel('Nível de renda familiar', fontsize=12)
    plt.ylabel('Densidade', fontsize=12)
    plt.xticks(ticks=range(len(ordem_renda)), labels=ordem_renda, rotation=70, ha='right')
    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Ajusta o 'rect' para dar mais espaço à legenda
    plt.savefig(os.path.join(graficos_path, '07_grafico_densidade_renda.png'), dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    # 8. GRÁFICO DE BARRAS EMPILHADAS: Mostra a composição proporcional de uma variável dentro de cada categoria de outra.
    print("[8/8] Gerando: Gráfico de Barras Empilhadas (Composição da Renda)...")
    # Calcula a proporção de cada faixa de renda dentro de cada grupo racial.
    # .unstack() transforma as linhas de contagem em colunas para cada faixa de renda.
    dados_empilhados_renda = df_filtrado.groupby('Cor/Raça')['RENDA_FAMILIAR'].value_counts(normalize=True).unstack().fillna(0) * 100
    # Gera o gráfico de barras empilhadas, onde cada barra (cor/raça) soma 100%.
    dados_empilhados_renda.plot(kind='bar', stacked=True, figsize=(15, 9), colormap='tab20')
    plt.title('Composição da renda familiar por cor/raça (%)', fontsize=16)
    plt.xlabel('Cor/raça', fontsize=12)
    plt.ylabel('Percentual de estudantes (%)', fontsize=12)
    plt.xticks(rotation=45) # Rota os ticks do eixo x.
    # Move a legenda para fora do gráfico para não obstruir os dados.
    plt.legend(title='Renda familiar (salário mínimo)', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout() # Ajusta layout.
    plt.savefig(os.path.join(graficos_path, '08_barras_empilhadas_composicao_renda.png'), dpi=300, bbox_inches='tight')
    plt.show() # Exibe.
    plt.close() # Fecha.


     # 3. GRÁFICO DE DISPERSÃO (ADAPTADO): Explora a relação entre três ou mais variáveis.
    print("[3/8] Gerando: Gráfico de Dispersão (Escolaridade vs Renda)...")
    # Agrega os dados para evitar sobreposição excessiva de pontos (overplotting).
    # Agrupa por Cor/Raça, Escolaridade do Pai e Mãe, calculando a renda média e a contagem de alunos para cada combinação.
    df_agregado = df_numeric.groupby(
        ['Cor/Raça', 'ESCOLARIDADE_PAI', 'ESCOLARIDADE_MAE'], observed=True
    ).agg(
        RENDA_MEDIA_COD=('RENDA_FAMILIAR_COD', 'mean'), # Renda média para a cor.
        CONTAGEM=('RENDA_FAMILIAR_COD', 'size')       # Número de alunos para o tamanho.
    ).reset_index() # reset_index transforma o agrupamento de volta em colunas.

    # Define os limites para a escala de cores e tamanhos no scatter plot.
    hue_norm = (df_agregado['RENDA_MEDIA_COD'].min(), df_agregado['RENDA_MEDIA_COD'].max())
    size_norm = (df_agregado['CONTAGEM'].min(), df_agregado['CONTAGEM'].max())

    # Cria os subplots, um para cada raça.
    fig, axes = plt.subplots(2, 3, figsize=(25, 14), sharex=True, sharey=True) # sharex e sharey compartilham os eixos.
    axes_flat = axes.flatten() # Transforma a matriz de eixos em um array 1D para fácil iteração.
    cmap = plt.get_cmap('viridis') # Obtém o colormap a ser usado.

    # Itera sobre cada raça para criar um subplot.
    for i, raca in enumerate(ordem_raca):
        ax = axes_flat[i] # Seleciona o subplot atual.
        data_subset = df_agregado[df_agregado['Cor/Raça'] == raca] # Filtra os dados para a raça atual.

        # Cria o scatter plot onde x e y são a escolaridade dos pais, a cor representa a renda média e o tamanho o n° de alunos.
        sns.scatterplot(
            data=data_subset, x='ESCOLARIDADE_PAI', y='ESCOLARIDADE_MAE',
            hue='RENDA_MEDIA_COD', size='CONTAGEM', sizes=(50, 2000), # Define a variação do tamanho dos pontos.
            palette='viridis', hue_norm=hue_norm, size_norm=size_norm, # Aplica as normas de cor e tamanho.
            ax=ax, legend=False, alpha=0.8 # legend=False desabilita a legenda automática do subplot.
        )
        ax.set_title(f'Cor/raça: {raca}', fontsize=14) # Define o título do subplot.
        ax.set_xlabel('') # Remove o rótulo do eixo x nos subplots individuais (será adicionado um rótulo geral).
        ax.set_ylabel('') # Remove o rótulo do eixo y nos subplots individuais (será adicionado um rótulo geral).

    # Configura os ticks dos eixos x e y para todos os subplots.
    for ax in axes_flat:
        ax.tick_params(axis='x', rotation=90, labelsize=11) # Rota e define o tamanho da fonte dos ticks do eixo x.
        ax.tick_params(axis='y', labelsize=11) # Define o tamanho da fonte dos ticks do eixo y.

    ax_legend = axes_flat[5] # Seleciona o último subplot.
    ax_legend.set_visible(False) # Oculta o último subplot, que não é usado para um gráfico.

    # Criação de legendas personalizadas para cor e tamanho, já que a legenda automática do Seaborn não é ideal para subplots.
    # Esta seção de código é mais complexa e demonstra um control

    # Define legend_income_codes and legend_labels based on the data
    # Obtém os códigos únicos de renda média e seleciona alguns para a legenda.
    unique_income_codes = sorted(df_agregado['RENDA_MEDIA_COD'].unique())
    # Amostra códigos para a legenda. Garante que não tente indexar com float.
    legend_income_codes = [int(code) for code in unique_income_codes[::max(1, len(unique_income_codes) // 5)]]

    # Mapeia os códigos selecionados de volta para os rótulos de renda correspondentes.
    legend_labels = [mapa_renda_familiar[list(mapa_renda_familiar.keys())[code]] for code in legend_income_codes]

    # Cria elementos de legenda personalizados para a cor (renda média).
    legend_elements_color = [Line2D([0], [0], marker='o', color='w', # Line2D cria um objeto gráfico simples (aqui, um marcador).
                                    markerfacecolor=cmap( (c-hue_norm[0])/(hue_norm[1]-hue_norm[0]) ), # Define a cor do marcador com base na escala.
                                    markersize=15, label=label) # Define o tamanho e o rótulo do marcador.
                            for c, label in zip(legend_income_codes, legend_labels)]
    # Adiciona a legenda de cores à figura.
    fig.legend(handles=legend_elements_color, title='Renda familiar média',
              loc='center left', bbox_to_anchor=(0.73, 0.28), # Posição da legenda.
              fontsize=12, title_fontsize=14, frameon=True) # Configurações de fonte e moldura.

    # Cria elementos de legenda personalizados para o tamanho (contagem de alunos).
    legend_size_values = np.array([10000, 50000, 100000, 200000]) # Valores de contagem para representar na legenda.
    s_scale = 2000 / size_norm[1] # Calcula a escala para o tamanho dos marcadores na legenda.
    legend_elements_size = [plt.scatter([],[], s=(v*s_scale), # plt.scatter cria um marcador de dispersão. s define o tamanho.
                                        color='gray', alpha=0.6, label=f'{int(v/1000)} mil') # Define cor, transparência e rótulo.
                            for v in legend_size_values]
    # Adiciona a legenda de tamanho à figura.
    fig.legend(handles=[h for h in legend_elements_size], title='Número de estudantes',
              loc='center left', bbox_to_anchor=(0.86, 0.28), # Posição da legenda.
              fontsize=12, title_fontsize=14, frameon=True) # Configurações de fonte e moldura.

    # Adiciona rótulos gerais para os eixos x e y da figura.
    fig.text(0.5, 0.04, 'Nível de escolaridade do pai', ha='center', va='center', fontsize=16)
    fig.text(0.08, 0.5, 'Nível de escolaridade da mãe', ha='center', va='center', rotation='vertical', fontsize=16)
    fig.suptitle('Escolaridade parental vs. renda média e contagem de alunos por cor/raça', fontsize=20, y=0.98) # Título principal da figura.
    plt.tight_layout(rect=[0.1, 0.05, 1, 0.95]) # Ajusta layout com espaço para títulos e legendas.
    plt.savefig(os.path.join(graficos_path, '03_grafico_dispersao_escolaridade_renda.png'), dpi=300, bbox_inches='tight')
    plt.show() # Exibe a figura.
    plt.close() # Fecha a figura.




if __name__ == "__main__":
    # Esta linha garante que a função main() só seja executada quando o script for rodado diretamente.
    main()