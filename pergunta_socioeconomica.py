import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np

def main():
    """
    Função principal para analisar as diferenças socioeconômicas entre
    estudantes de diferentes grupos raciais/cor no ENEM 2024.
    """



 
    drive_path = '/content/'
    dados_enem_file = os.path.join(drive_path, 'PARTICIPANTES_2024.csv')

    # Define um estilo visual para os gráficos
    sns.set_theme(style="whitegrid")


    # --- Parte 1: Carregar os Dados do CSV ---
    print("\n--- Parte 1: Carregando Dados ---")
    try:
        # Carrega o arquivo de resultados do ENEM 2024
        # Especificando o encoding e o delimitador, se necessário
        df = pd.read_csv(dados_enem_file, encoding='latin1', delimiter=';')
        print(f"Dados carregados com sucesso: {len(df)} registros.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{dados_enem_file}' não encontrado.")
        print("Verifique se o caminho está correto e o Google Drive montado.")
        return
    except Exception as e:
        print(f"ERRO ao carregar o arquivo CSV: {e}")
        return

    if df is None or df.empty:
        print("DataFrame está vazio. Finalizando.")
        return

    # --- DECODIFICAÇÃO E PREPARAÇÃO DOS DADOS ---
    print("\nDecodificando os dados para análise...")

    # Dicionários de mapeamento... (mesmos do código anterior)
    mapa_cor_raca = {0: 'Não declarado', 1: 'Branca', 2: 'Preta', 3: 'Parda', 4: 'Amarela', 5: 'Indígena', 6: 'Não dispõe da informação'}
    mapa_escolaridade = {'A': 'Nunca estudou', 'B': 'Fund. I Incompleto', 'C': 'Fund. II Incompleto', 'D': 'Médio Incompleto', 'E': 'Médio Completo', 'F': 'Superior Completo', 'G': 'Pós-graduação', 'H': 'Não sei'}
    mapa_ocupacao = {'A': 'Grupo 1 (Agricultor)', 'B': 'Grupo 2 (Doméstico)', 'C': 'Grupo 3 (Qualificado)', 'D': 'Grupo 4 (Técnico)', 'E': 'Grupo 5 (Superior)', 'F': 'Não sei'}
    mapa_renda_familiar = {
        'A': 'Nenhuma Renda', 
        'B': 'Até 1 Sálario Min.', 
        'C': '1-1.5 Sálario Min.', 
        'D': '1.5-2 Sálario Min.', 
        'E': '2-2.5 Sálario Min.', 
        'F': '2.5-3 Sálario Min.', 
        'G': '3-4 Sálario Min.', 
        'H': '4-5 Sálario Min.', 
        'I': '5-6 Sálario Min.', 
        'J': '6-7 Sálario Min.', 
        'K': '7-8 Sálario Min.', 
        'L': '8-9 Sálario Min.', 
        'M': '9-10 Sálario Min.', 
        'N': '10-12 Sálario Min.', 
        'O': '12-15 Sálario Min.', 
        'P': '15-20 Sálario Min.', 
        'Q': 'Acima de 20 Sálario Min.'}

    # Aplicando mapeamento para todas as variáveis - Corrigindo nomes das colunas
    df['COR_RACA'] = df['TP_COR_RACA'].map(mapa_cor_raca)
    df['ESCOLARIDADE_PAI'] = df['Q001'].map(mapa_escolaridade)
    df['ESCOLARIDADE_MAE'] = df['Q002'].map(mapa_escolaridade)
    df['OCUPACAO_PAI'] = df['Q003'].map(mapa_ocupacao)
    df['OCUPACAO_MAE'] = df['Q004'].map(mapa_ocupacao)
    df['RENDA_FAMILIAR'] = df['Q007'].map(mapa_renda_familiar)

    # Define a ordem lógica para os gráficos
    ordem_raca = ['Branca', 'Parda', 'Preta', 'Amarela', 'Indígena', 'Não declarado']
    ordem_escolaridade = list(mapa_escolaridade.values())
    ordem_ocupacao = list(mapa_ocupacao.values())
    ordem_renda = list(mapa_renda_familiar.values())

    # Converte para tipo Categórico com ordem
    df['COR_RACA'] = pd.Categorical(df['COR_RACA'], categories=ordem_raca, ordered=True)
    df['ESCOLARIDADE_PAI'] = pd.Categorical(df['ESCOLARIDADE_PAI'], categories=ordem_escolaridade, ordered=True)
    df['ESCOLARIDADE_MAE'] = pd.Categorical(df['ESCOLARIDADE_MAE'], categories=ordem_escolaridade, ordered=True)
    df['OCUPACAO_PAI'] = pd.Categorical(df['OCUPACAO_PAI'], categories=ordem_ocupacao, ordered=True)
    df['OCUPACAO_MAE'] = pd.Categorical(df['OCUPACAO_MAE'], categories=ordem_ocupacao, ordered=True)
    df['RENDA_FAMILIAR'] = pd.Categorical(df['RENDA_FAMILIAR'], categories=ordem_renda, ordered=True)

    # Filtrar valores indesejados
    df_filtrado = df[~df['COR_RACA'].isin(['Não declarado', 'Não dispõe da informação'])].copy()
    for col in ['ESCOLARIDADE_PAI', 'ESCOLARIDADE_MAE', 'OCUPACAO_PAI', 'OCUPACAO_MAE', 'RENDA_FAMILIAR']: # Incluindo Renda Familiar na filtragem
        df_filtrado = df_filtrado[~df_filtrado[col].isin(['Não sei', 'Não declarado', 'Não dispõe da informação', None])] # Adicionando None para garantir

    # Criar códigos numéricos para correlação e alguns gráficos
    df_numeric = df_filtrado.copy()
    for col in df_filtrado.columns:
        if isinstance(df_filtrado[col].dtype, pd.CategoricalDtype):
            df_numeric[f'{col}_COD'] = df_filtrado[col].cat.codes

    # --- GERAÇÃO DOS GRÁFICOS ---

    # 1. Gráficos de Barras (Escolaridade do Pai e da Mãe)
    print("\n[1/8] Gerando: Gráficos de Barras (Escolaridade Mãe e Pai)...")
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
    sns.countplot(ax=axes[0], data=df_filtrado, y='ESCOLARIDADE_MAE', hue='COR_RACA', palette='viridis')
    axes[0].set_title('Escolaridade da Mãe por Cor/Raça do Estudante')
    axes[0].set_xlabel('Número de Estudantes')
    axes[0].legend(title='Cor/Raça')
    sns.countplot(ax=axes[1], data=df_filtrado, y='ESCOLARIDADE_PAI', hue='COR_RACA', palette='viridis')
    axes[1].set_title('Escolaridade do Pai por Cor/Raça do Estudante')
    axes[1].set_xlabel('Número de Estudantes')
    axes[1].get_legend().remove() # Remove a legenda duplicada
    fig.suptitle('Gráfico de Barras: Comparativo da Escolaridade Parental', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    # 2. Gráfico de Barras Empilhadas (Composição da Renda Familiar)
    print("[2/8] Gerando: Gráfico de Barras Empilhadas (Renda)...")
    dados_empilhados_renda = df_filtrado.groupby('COR_RACA')['RENDA_FAMILIAR'].value_counts(normalize=True).unstack().fillna(0) * 100
    dados_empilhados_renda.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='tab20')
    plt.title('Barras Empilhadas: Composição da Renda Familiar por Cor/Raça (%)')
    plt.xlabel('Cor/Raça'), plt.ylabel('Percentual de Estudantes (%)'), plt.xticks(rotation=45)
    plt.legend(title='Renda (SM)', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # 3. Boxplots (Comparando Escolaridade e Ocupação Parental)
    print("[3/8] Gerando: Boxplots Múltiplos...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True)
    parental_vars = {
        'Escolaridade Mãe': ('ESCOLARIDADE_MAE_COD', ordem_escolaridade),
        'Escolaridade Pai': ('ESCOLARIDADE_PAI_COD', ordem_escolaridade),
        'Ocupação Mãe': ('OCUPACAO_MAE_COD', ordem_ocupacao),
        'Ocupação Pai': ('OCUPACAO_PAI_COD', ordem_ocupacao)
    }

    for i, (title, (var_cod, labels)) in enumerate(parental_vars.items()):
        ax = axes.flatten()[i]
        sns.boxplot(ax=ax, data=df_numeric, x='COR_RACA', y=var_cod, palette='plasma')
        ax.set_title(f'Distribuição de: {title}')
        ax.set_xlabel(''), ax.set_ylabel('Nível (Código Numérico)')
        ax.set_yticks(ticks=range(len(labels)), labels=labels)
        ax.tick_params(axis='x', rotation=45)

    fig.suptitle('Boxplots: Comparativo Socioeconômico Parental por Cor/Raça', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    # 4. Gráfico de Densidade (Renda Familiar)
    print("[4/8] Gerando: Gráfico de Densidade (Renda)...")
    plt.figure(figsize=(12, 7))
    sns.kdeplot(data=df_numeric, x='RENDA_FAMILIAR_COD', hue='COR_RACA', fill=True, common_norm=False, palette='crest')
    plt.title('Densidade: Distribuição da Renda Familiar por Cor/Raça'), plt.xlabel('Nível de Renda')
    plt.xticks(ticks=range(0, len(ordem_renda), 2), labels=ordem_renda[::2], rotation=30), plt.ylabel('Densidade')
    plt.tight_layout(), plt.show()

    # 5. Gráfico de Linhas (Comparando Escolaridade Parental)
    print("[5/8] Gerando: Gráficos de Linhas (Escolaridade)...")
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
    # Mãe
    data_mae = df_filtrado.groupby('COR_RACA')['ESCOLARIDADE_MAE'].value_counts(normalize=True).unstack().fillna(0) * 100
    data_mae.T.plot(kind='line', style='-o', ax=axes[0])
    axes[0].set_title('% de Mães por Nível de Escolaridade'), axes[0].set_xlabel('Escolaridade da Mãe')
    axes[0].set_ylabel('Percentual de Estudantes (%)'), axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    # Pai
    data_pai = df_filtrado.groupby('COR_RACA')['ESCOLARIDADE_PAI'].value_counts(normalize=True).unstack().fillna(0) * 100
    data_pai.T.plot(kind='line', style='-s', ax=axes[1])
    axes[1].set_title('% de Pais por Nível de Escolaridade'), axes[1].set_xlabel('Escolaridade do Pai')
    axes[1].get_legend().remove(), axes[1].tick_params(axis='x', rotation=45), axes[1].grid(True, linestyle='--', alpha=0.6)

    fig.suptitle('Gráfico de Linhas: Comparativo da Evolução da Escolaridade Parental', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]), plt.show()

    # 6. Heatmap de Correlação (Incluindo todas as variáveis)
    print("[6/8] Gerando: Heatmap de Correlação...")
    corr_cols = [
        'RENDA_FAMILIAR_COD', 'ESCOLARIDADE_MAE_COD', 'ESCOLARIDADE_PAI_COD',
        'OCUPACAO_MAE_COD', 'OCUPACAO_PAI_COD', 'COR_RACA_COD'
    ]
    correlation_matrix = df_numeric[corr_cols].corr(method='spearman')
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    labels = ['Renda', 'Esc. Mãe', 'Esc. Pai', 'Ocup. Mãe', 'Ocup. Pai', 'Cor/Raça']
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation=45)
    plt.yticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation=0)
    plt.title('Heatmap: Correlação entre Fatores Socioeconômicos', fontsize=16)
    plt.tight_layout(), plt.show()

    # 7. Gráfico de Dispersão (Escolaridade da Mãe vs. Escolaridade do Pai)
    print("[7/8] Gerando: Gráfico de Dispersão...")
    g = sns.relplot(
        data=df_numeric, x='ESCOLARIDADE_PAI_COD', y='ESCOLARIDADE_MAE_COD',
        hue='RENDA_FAMILIAR_COD', palette='rocket_r',
        col='COR_RACA', col_wrap=3, alpha=0.7,
        height=4, aspect=1.2
    )
    g.fig.suptitle('Dispersão: Escolaridade do Pai vs. Mãe, por Cor/Raça e Renda Familiar', fontsize=16)
    g.set_axis_labels('Nível Escolaridade do Pai', 'Nível Escolaridade da Mãe')
    # Customizando os ticks para mostrar labels de texto
    for ax in g.axes.flatten():
        ax.set_xticks(ticks=range(len(ordem_escolaridade)), labels=ordem_escolaridade)
        ax.set_yticks(ticks=range(len(ordem_escolaridade)), labels=ordem_escolaridade)
        ax.tick_params(axis='x', rotation=90, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    # 8. Histograma (Distribuição da Renda)
    print("[8/8] Gerando: Histograma (Renda)...")
    plt.figure(figsize=(12, 7))
    sns.histplot(data=df_numeric, x='RENDA_FAMILIAR_COD', hue='COR_RACA', multiple='stack', palette='cubehelix', discrete=True)
    plt.title('Histograma: Distribuição da Renda Familiar por Cor/Raça'), plt.xlabel('Nível de Renda')
    plt.xticks(ticks=range(len(ordem_renda)), labels=ordem_renda, rotation=60), plt.ylabel('Contagem de Estudantes')
    plt.tight_layout(), plt.show()


if __name__ == "__main__":
    main()