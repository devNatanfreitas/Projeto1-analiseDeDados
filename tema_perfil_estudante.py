"""## Tema Perfil do Estudante

**Pergunta de Pesquisa:** Qual é o perfil demográfico dos estudantes inscritos no ENEM 2024, considerando a relação entre idade, sexo, estado civil e situação de conclusão do ensino médio?
"""

#@title Código do Tema Perfil do Estudante
# --- Importação de Bibliotecas ---
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():

    # --- Configuração Inicial ---
    dados_path = 'DADOS'
    participantes_file = os.path.join(dados_path, 'PARTICIPANTES_2024.csv')
    sns.set_theme(style="whitegrid", palette="viridis") # Estilo visual dos gráficos
    
    # Cria a pasta para salvar os gráficos
    graficos_path = 'graficos_perfil_estudante'
    os.makedirs(graficos_path, exist_ok=True)

    # --- Carregamento dos Dados ---
    # Carrega apenas as colunas de perfil demográfico necessárias para otimizar.
    cols_perfil = ['TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL', 'TP_ST_CONCLUSAO']
    try:
        df = pd.read_csv(participantes_file, encoding='latin1', delimiter=';', usecols=cols_perfil)
        print(f"Dados de perfil carregados com sucesso: {len(df)} registros.")
    except Exception as e:
        print(f"ERRO ao carregar o arquivo de participantes: {e}")
        return

    # --- Parte 2: Decodificação e Preparação dos Dados ---
    # Dicionários para traduzir os códigos em textos legíveis.
    mapa_sexo = {'F': 'Feminino', 'M': 'Masculino'}
    mapa_idade = {1: '<17', 2: '17', 3: '18', 4: '19', 5: '20', 6: '21', 7: '22', 8: '23', 9: '24', 10: '25', 11: '26-30', 12: '31-35', 13: '36-40', 14: '>40'}
    mapa_conclusao = {1: 'Já concluí', 2: 'Estou cursando', 3: 'Cursando após concluir', 4: 'Não concluí'}
    mapa_estado_civil = {0: 'Não inf.', 1: 'Solteiro(a)', 2: 'Casado(a)', 3: 'Divorciado(a)', 4: 'Viúvo(a)'}

    # Aplica os mapas para criar as novas colunas descritivas.
    df['Sexo'] = df['TP_SEXO'].map(mapa_sexo)
    df['Faixa Etária'] = pd.Categorical(df['TP_FAIXA_ETARIA'].map(mapa_idade), categories=mapa_idade.values(), ordered=True)
    df['Situação Conclusão'] = df['TP_ST_CONCLUSAO'].map(mapa_conclusao)
    df['Estado Civil'] = df['TP_ESTADO_CIVIL'].map(mapa_estado_civil)
    # Remove qualquer linha que tenha valores nulos após o mapeamento (ex: códigos inválidos).
    df.dropna(inplace=True)

    print(f"Total de registros válidos para a análise de perfil: {len(df)}")
    if df.empty: return

    # --- Parte 3: Geração dos 8 Gráficos de Perfil ---

     # 1. HISTOGRAMA (sem alterações)
    print("[1/8] Gerando: Histograma da Faixa Etária...")
    plt.figure(figsize=(12, 7)); sns.histplot(data=df, x='TP_FAIXA_ETARIA', bins=len(mapa_idade), discrete=True, hue='Sexo'); plt.title('Histograma: Distribuição de Inscritos por Faixa Etária', fontsize=16); plt.xlabel('Faixa Etária'); plt.ylabel('Contagem de Inscritos'); plt.xticks(ticks=list(mapa_idade.keys()), labels=mapa_idade.values(), rotation=45, ha='right'); plt.savefig(os.path.join(graficos_path, '01_histograma_faixa_etaria.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 2. GRÁFICO DE VIOLINO (sem alterações)
    print("[2/8] Gerando: Gráfico de Violino...")
    plt.figure(figsize=(12, 8)); sns.violinplot(data=df, x='Situação Conclusão', y='TP_FAIXA_ETARIA'); plt.title('Violino: Distribuição de Idade por Situação de Conclusão do EM', fontsize=16); plt.xlabel('Situação de Conclusão'); plt.ylabel('Faixa Etária'); plt.yticks(ticks=list(mapa_idade.keys()), labels=mapa_idade.values()); plt.savefig(os.path.join(graficos_path, '02_violino_idade_conclusao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 3. GRÁFICO DE DISPERSÃO (STRIPPLOT) (COM A LEGENDA CORRIGIDA)
    
    # 4. GRÁFICO DE BARRAS (sem alterações)
    print("[4/8] Gerando: Gráfico de Barras do Perfil Demográfico...")
    fig, ax = plt.subplots(1, 2, figsize=(18, 7)); sns.countplot(ax=ax[0], data=df, x='Sexo').set_title('Contagem por Sexo'); sns.countplot(ax=ax[1], data=df, x='Situação Conclusão').set_title('Contagem por Situação de Conclusão do EM'); fig.suptitle('Gráfico de Barras: Perfil Geral dos Inscritos', fontsize=16); plt.savefig(os.path.join(graficos_path, '04_barras_perfil_demografico.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 5. GRÁFICO DE LINHAS (sem alterações)
    print("[5/8] Gerando: Gráfico de Linhas (Proporção de Sexo por Idade)...")
    comp_sexo_idade = df.groupby('Faixa Etária', observed=True)['Sexo'].value_counts(normalize=True).unstack().fillna(0) * 100; comp_sexo_idade.plot(kind='line', style='-o', figsize=(12, 7)); plt.title('Linhas: Proporção de Sexo por Faixa Etária (%)', fontsize=16); plt.xlabel('Faixa Etária'); plt.ylabel('Percentual de Inscritos (%)'); plt.grid(True, linestyle='--'); plt.savefig(os.path.join(graficos_path, '05_linhas_proporcao_sexo_idade.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 6. HEATMAP (sem alterações)
    print("[6/8] Gerando: Heatmap (Estado Civil vs Situação de Conclusão)...")
    heatmap_data = pd.crosstab(df['Estado Civil'], df['Situação Conclusão']); plt.figure(figsize=(10, 7)); sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='cividis'); plt.title('Heatmap: Contagem por Estado Civil e Situação de Conclusão', fontsize=16); plt.savefig(os.path.join(graficos_path, '06_heatmap_civil_conclusao.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 7. GRÁFICO DE DENSIDADE (KDE) (sem alterações)
    print("[7/8] Gerando: Gráfico de Densidade da Faixa Etária...")
    plt.figure(figsize=(12, 7)); sns.kdeplot(data=df, x='TP_FAIXA_ETARIA', hue='Sexo', fill=True, bw_adjust=0.5); plt.title('Densidade: Distribuição de Idade dos Inscritos por Sexo', fontsize=16); plt.xlabel('Faixa Etária'); plt.ylabel('Densidade'); plt.xticks(ticks=list(mapa_idade.keys()), labels=mapa_idade.values(), rotation=45, ha='right'); plt.savefig(os.path.join(graficos_path, '07_densidade_idade_sexo.png'), dpi=300, bbox_inches='tight'); plt.show()

    # 8. GRÁFICO DE BARRAS EMPILHADAS (sem alterações)
    print("[8/8] Gerando: Gráfico de Barras Empilhadas...")
    comp_conclusao_idade = df.groupby('Faixa Etária', observed=True)['Situação Conclusão'].value_counts(normalize=True).unstack().fillna(0) * 100; comp_conclusao_idade.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='YlGnBu'); plt.title('Barras Empilhadas: Composição da Situação de Conclusão por Faixa Etária (%)', fontsize=16); plt.xlabel('Faixa Etária'); plt.ylabel('Percentual de Inscritos (%)'); plt.legend(title='Situação de Conclusão', bbox_to_anchor=(1.02, 1)); plt.savefig(os.path.join(graficos_path, '08_barras_empilhadas_conclusao_idade.png'), dpi=300, bbox_inches='tight'); plt.show()

    print("[3/8] Gerando: Gráfico de Dispersão (Stripplot)...")
    plt.figure(figsize=(16, 9)) # Aumentei um pouco o tamanho para acomodar a legenda
    sns.stripplot(data=df, x='Faixa Etária', y='Estado Civil', hue='Sexo', jitter=0.3, alpha=0.5, dodge=True)
    plt.title('Dispersão: Relação entre Idade, Estado Civil e Sexo', fontsize=16)
    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Estado Civil', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Sexo', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig(os.path.join(graficos_path, '03_stripplot_idade_civil_sexo.png'), dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()