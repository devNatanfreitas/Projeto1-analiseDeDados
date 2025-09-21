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


        colunas = ['"TP_COR_RACA"', '"Q001"', '"Q002"', '"Q003"', '"Q004"', '"Q007"']
        query = f"SELECT {','.join(colunas)} from participantes"

        df = pd.read_sql_query(query, engine)
        
        # Define mappings
        print("\nDecodificando os dados para análise...")
        
        # Dicionários de mapeamento atualizados
        mapa_cor_raca = {
            0: 'Não declarado', 1: 'Branca', 2: 'Preta',
            3: 'Parda', 4: 'Amarela', 5: 'Indígena',
            6: 'Não dispõe da informação'
        }
        
        mapa_escolaridade = {
            'A': 'Nunca estudou',
            'B': 'Fundamental I Incompleto',
            'C': 'Fundamental II Incompleto',
            'D': 'Ensino Médio Incompleto',
            'E': 'Ensino Médio Completo',
            'F': 'Superior Completo',
            'G': 'Pós-graduação Completa',
            'H': 'Não sei'
        }

        # Novo dicionário para Ocupação (Q003 e Q004)
        # Resumido para melhor visualização em tabelas
        mapa_ocupacao = {
            'A': 'Grupo 1 (Agricultor, etc)',
            'B': 'Grupo 2 (Doméstico, Vendedor, etc)',
            'C': 'Grupo 3 (Operário Qualificado, etc)',
            'D': 'Grupo 4 (Técnico, Professor, etc)',
            'E': 'Grupo 5 (Nível Superior, Diretor, etc)',
            'F': 'Não sei'
        }

        # Mapa para RENDA FAMILIAR (Q007)
        mapa_renda_familiar = {
            'A': 'Nenhuma Renda', 'B': 'Até 1 SM', 'C': '1 a 1.5 SM', 'D': '1.5 a 2 SM',
            'E': '2 a 2.5 SM', 'F': '2.5 a 3 SM', 'G': '3 a 4 SM', 'H': '4 a 5 SM',
            'I': '5 a 6 SM', 'J': '6 a 7 SM', 'K': '7 a 8 SM', 'L': '8 a 9 SM',
            'M': '9 a 10 SM', 'N': '10 a 12 SM', 'O': '12 a 15 SM', 'P': '15 a 20 SM',
            'Q': 'Acima de 20 SM'
        }
            
        # Apply mappings to create new columns
        df['COR_RACA'] = df['TP_COR_RACA'].map(mapa_cor_raca)
        df['ESCOLARIDADE_PAI'] = df['Q001'].map(mapa_escolaridade)
        df['ESCOLARIDADE_MAE'] = df['Q002'].map(mapa_escolaridade)
        df['OCUPACAO_PAI'] = df['Q003'].map(mapa_ocupacao)
        df['OCUPACAO_MAE'] = df['Q004'].map(mapa_ocupacao)
        df['RENDA_FAMILIAR'] = df['Q007'].map(mapa_renda_familiar)
        
        # Perform analysis
        print("\n>> Distribuição da RENDA FAMILIAR por Cor/Raça (%):")
        analise_renda = df.groupby(['RENDA_FAMILIAR'])['COR_RACA'].value_counts(normalize=True).mul(100).round(2).unstack(fill_value=0)
        print(analise_renda)

    # 2. Escolaridade da Mãe por Cor/Raça
        print("\n>> Distribuição da ESCOLARIDADE DA MÃE e do PAI por Cor/Raça (%):")
        analise_escolaridade = df.groupby(['ESCOLARIDADE_MAE', 'ESCOLARIDADE_PAI'])['COR_RACA'].value_counts(normalize=True).mul(100).round(2).unstack(fill_value=0)
        print(analise_escolaridade)

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return

if __name__ == "__main__":
    main()