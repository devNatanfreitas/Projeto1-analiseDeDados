#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar os temas modificados.
Este script executa um tema específico para verificar se os gráficos estão sendo salvos corretamente.
"""

import subprocess
import sys
import os

def testar_tema(nome_tema):
    """
    Testa um tema específico executando o arquivo Python correspondente.
    
    Args:
        nome_tema (str): Nome do tema a ser testado (ex: 'desempenho', 'academico', etc.)
    """
    arquivo_tema = f"tema_{nome_tema}.py"
    
    if not os.path.exists(arquivo_tema):
        print(f"ERRO: Arquivo {arquivo_tema} não encontrado!")
        return False
    
    print(f"\n{'='*50}")
    print(f"TESTANDO TEMA: {nome_tema.upper()}")
    print(f"{'='*50}")
    
    try:
        # Executa o script do tema
        resultado = subprocess.run([sys.executable, arquivo_tema], 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=300)  # Timeout de 5 minutos
        
        if resultado.returncode == 0:
            print(f"✅ Tema {nome_tema} executado com sucesso!")
            print(f"📁 Verifique a pasta 'graficos_{nome_tema}' para os gráficos gerados.")
            
            # Verifica se a pasta de gráficos foi criada
            pasta_graficos = f"graficos_{nome_tema}"
            if os.path.exists(pasta_graficos):
                arquivos = os.listdir(pasta_graficos)
                print(f"📊 {len(arquivos)} arquivo(s) gerado(s): {', '.join(arquivos)}")
            else:
                print(f"⚠️  Pasta {pasta_graficos} não foi criada!")
            
            return True
        else:
            print(f"❌ Erro ao executar tema {nome_tema}:")
            print(f"STDOUT: {resultado.stdout}")
            print(f"STDERR: {resultado.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal para testar os temas."""
    print("🚀 INICIANDO TESTE DOS TEMAS MODIFICADOS")
    print("=" * 60)
    
    # Verifica se a pasta DADOS existe
    if not os.path.exists("DADOS"):
        print("❌ ERRO: Pasta 'DADOS' não encontrada!")
        print("Por favor, certifique-se de que os arquivos CSV estão na pasta 'DADOS'")
        return
    
    # Lista de temas disponíveis
    temas = ['desempenho', 'academico', 'perfil_estudante', 'instucional', 'socieconomico']
    
    print("Temas disponíveis:")
    for i, tema in enumerate(temas, 1):
        print(f"{i}. {tema}")
    
    print("\nDigite o número do tema que deseja testar (ou 0 para testar todos):")
    
    try:
        escolha = int(input("Sua escolha: "))
        
        if escolha == 0:
            # Testa todos os temas
            sucessos = 0
            for tema in temas:
                if testar_tema(tema):
                    sucessos += 1
                print()  # Linha em branco entre temas
            
            print(f"\n📊 RESUMO: {sucessos}/{len(temas)} temas executados com sucesso!")
            
        elif 1 <= escolha <= len(temas):
            # Testa tema específico
            tema_escolhido = temas[escolha - 1]
            testar_tema(tema_escolhido)
            
        else:
            print("❌ Escolha inválida!")
            
    except ValueError:
        print("❌ Por favor, digite um número válido!")
    except KeyboardInterrupt:
        print("\n⚠️  Teste interrompido pelo usuário!")

if __name__ == "__main__":
    main()