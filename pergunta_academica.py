import pandas as pd
from db import get_db_connection, get_db_params
from sqlalchemy import create_engine



def main():
    conn = get_db_connection()
    conn_string = None
    engine = None



    if conn is None:
        print("Não foi possível conectar ao banco de dados.")
        return
    
    try:
        db_params = get_db_params()
        conn_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(conn_string)

        query_participantes = 'SELECT "NU_INSCRICAO", "Q023", "TP_ENSINO" FROM participantes'
        df_participantes = pd.read_sql_query(query_participantes, engine)

        
        colunas_provas = [
            '"NU_NOTA_CN"', '"NU_NOTA_CH"', '"NU_NOTA_LC"', '"NU_NOTA_MT"', '"NU_NOTA_REDACAO"',
            '"TP_PRESENCA_CN"', '"TP_PRESENCA_CH"', '"TP_PRESENCA_LC"', '"TP_PRESENCA_MT"', '"TP_STATUS_REDACAO"'
        ]
        query_provas = f"SELECT {', '.join(colunas_provas)} FROM resultados"
        df_provas = pd.read_sql_query(query_provas, engine)

        print(f"Dados carregados: {len(df_participantes)} participantes e {len(df_provas)} registros de prova.")

    except Exception as e:
        print(f"Erro ao carregar dados do banco: {e}")
        return

    # --- Parte 2: Unir (Merge), Limpar e Preparar os Dados ---
    print("\nJuntando (merge) os dados...")
    
    # Como as tabelas não têm chave comum, mas têm o mesmo número de registros,
    # vamos assumir que estão na mesma ordem e usar o índice para unir
    df_participantes['index_temp'] = df_participantes.index
    df_provas['index_temp'] = df_provas.index
    df_final = pd.merge(df_participantes, df_provas, on='index_temp', how='inner')
    df_final.drop('index_temp', axis=1, inplace=True)
    
    print("\nIniciando limpeza e preparação dos dados...")


    df_presentes = df_final[
        (df_final['TP_PRESENCA_CN'] == 1) & (df_final['TP_PRESENCA_CH'] == 1) &
        (df_final['TP_PRESENCA_LC'] == 1) & (df_final['TP_PRESENCA_MT'] == 1) &
        (df_final['TP_STATUS_REDACAO'] == 1)
    ].copy()

    notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_presentes.dropna(subset=notas_cols, inplace=True)
    
    print(f"Registros válidos e combinados para análise: {len(df_presentes)}.")

    mapa_tipo_escola = {
        'A': 'Somente Pública', 
        'B': 'Mista (pública e privada sem bolsa)',
        'C': 'Mista (pública e privada com bolsa)', 
        'D': 'Somente Privada (sem bolsa)',
        'E': 'Somente Privada (com bolsa)', 
        'F': 'Não frequentou Ensino Médio'
    }
    df_presentes['TIPO_ESCOLA'] = df_presentes['Q023'].map(mapa_tipo_escola)
    
    mapa_modalidade_ensino = {  1: 'Ensino Regular', 2: 'Educação Especial/EJA' }
    df_presentes['MODALIDADE_ENSINO'] = df_presentes['TP_ENSINO'].map(mapa_modalidade_ensino)
    
    # --- Parte 3: Análise de Desempenho (com os dados já unidos) ---
    pd.set_option('display.float_format', '{:.2f}'.format)

    print("\n" + "="*80)
    print(" ANÁLISE DE DESEMPENHO (NOTAS TRI) NO ENEM 2024")
    print("="*80)


    analise = df_presentes.groupby(['TIPO_ESCOLA', 'MODALIDADE_ENSINO'])[notas_cols].mean()
    print(analise)
    

if __name__ == "__main__":
    main()