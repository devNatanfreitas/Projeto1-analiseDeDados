import psycopg2

def get_db_params():
    """Retorna os parâmetros de conexão com o banco de dados."""
    return {
        'host': 'localhost',
        'database': 'postgres',
        'port': '5432',
        'user': 'postgres',
        'password': '' 
    }

def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL."""
    db_params = get_db_params()
    
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        print("Conexão bem-sucedida ao banco de dados.")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        if conn:
            conn.close()
        return None