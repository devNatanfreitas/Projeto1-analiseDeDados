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
        
        # Primeiro, vamos verificar quantos registros existem na tabela
        count_query = "SELECT COUNT(*) as total FROM participantes"
        count_df = pd.read_sql_query(count_query, engine)
        total_registros = count_df['total'].iloc[0] 
        
        
        query = "SELECT * FROM participantes"
        
        print("Executando consulta... Isso pode levar alguns minutos dependendo do tamanho dos dados.")
        df = pd.read_sql_query(query, engine)
        
        print(f"Dados carregados: {len(df)} registros")
        nome_arquivo = "relatorio_participantes.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"Relatório salvo como {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()