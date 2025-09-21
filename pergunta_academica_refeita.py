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

       
        
        
        colunas_resultados = [
            '"TP_DEPENDENCIA_ADM_ESC"',
            '"NU_NOTA_CN"', '"NU_NOTA_CH"', '"NU_NOTA_LC"', '"NU_NOTA_MT"', '"NU_NOTA_REDACAO"',
            '"TP_PRESENCA_CN"', '"TP_PRESENCA_CH"', '"TP_PRESENCA_LC"', '"TP_PRESENCA_MT"', '"TP_STATUS_REDACAO"'
        ]
        query_resultados = f"SELECT {', '.join(colunas_resultados)} FROM resultados"
        df_resultados = pd.read_sql_query(query_resultados, engine)
        print(f"Dados carregados: {len(df_resultados)} registros.")

    except Exception as e:
        print(f"Erro ao carregar dados do banco: {e}")
        return
    finally:
        if conn:
            conn.close()

    # --- Parte 2: Limpar e Preparar os Dados ---
    print("\nLimpando e preparando dados para análise...")

    # Filtra participantes que informaram a escola (código 0 ou nulo geralmente significa não informado)
    # E que estiveram presentes nas provas.
    df_presentes = df_resultados[
        (df_resultados['TP_DEPENDENCIA_ADM_ESC'].isin([1, 2, 3, 4])) &
        (df_resultados['TP_PRESENCA_CN'] == 1) &
        (df_resultados['TP_PRESENCA_CH'] == 1) &
        (df_resultados['TP_PRESENCA_LC'] == 1) &
        (df_resultados['TP_PRESENCA_MT'] == 1) &
        (df_resultados['TP_STATUS_REDACAO'] == 1)
    ].copy()

    notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_presentes.dropna(subset=notas_cols, inplace=True)
    
    # Criar a variável descritiva para a dependência da escola
    mapa_dependencia = {
        1: 'Federal',
        2: 'Estadual',
        3: 'Municipal',
        4: 'Privada'
    }
    df_presentes['DEPENDENCIA_ADM'] = df_presentes['TP_DEPENDENCIA_ADM_ESC'].map(mapa_dependencia)
    
    # --- Parte 3: Análise de Desempenho ---
    pd.set_option('display.float_format', '{:.2f}'.format)
    

    analise_final = df_presentes.groupby('DEPENDENCIA_ADM')[notas_cols].mean()
    print(analise_final)

if __name__ == "__main__":
    main()