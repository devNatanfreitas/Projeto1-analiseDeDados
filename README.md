# Projeto de Análise de Dados - ENEM 2024

## 📁 Estrutura do Projeto

```
Projeto1-analiseDeDados/
├── DADOS/                          # Pasta com os arquivos CSV do ENEM
│   ├── ITENS_PROVA_2024.csv
│   ├── PARTICIPANTES_2024.csv
│   └── RESULTADOS_2024.csv
├── graficos_academico/             # Gráficos do tema acadêmico
├── graficos_desempenho/            # Gráficos do tema desempenho
├── graficos_institucional/         # Gráficos do tema institucional
├── graficos_perfil_estudante/      # Gráficos do perfil do estudante
├── graficos_socioeconomico/        # Gráficos do tema socioeconômico
├── tema_academico.py               # Análise acadêmica
├── tema_desempenho.py              # Análise de desempenho
├── tema_instucional.py             # Análise institucional
├── tema_perfil_estudante.py        # Análise do perfil do estudante
├── tema_socieconomico.py           # Análise socioeconômica
├── testar_temas.py                 # Script para testar os temas
└── README.md                       # Este arquivo
```

## 🚀 Modificações Realizadas

### ✅ Padronização dos Dados
- **TODOS** os temas agora leem os dados da pasta `DADOS`
- Caminho padronizado: `dados_path = 'DADOS'`

### 📊 Organização dos Gráficos
- Cada tema salva seus gráficos em uma pasta separada
- Formato: `graficos_{nome_do_tema}/`
- Gráficos salvos em alta resolução (300 DPI)
- Nomenclatura padronizada: `{numero}_{tipo}_{descricao}.png`

### 📁 Pastas de Gráficos Criadas

| Tema | Pasta | Descrição |
|------|-------|-----------|
| Acadêmico | `graficos_academico/` | Análise por dependência administrativa |
| Desempenho | `graficos_desempenho/` | Correlação entre provas objetivas e redação |
| Institucional | `graficos_institucional/` | Análise por UF e região |
| Perfil Estudante | `graficos_perfil_estudante/` | Demografia dos participantes |
| Socioeconômico | `graficos_socioeconomico/` | Fatores socioeconômicos por cor/raça |

## 📊 Tipos de Gráficos por Tema

### 🎓 Tema Acadêmico (8 gráficos)
1. `01_barras_notas_medias.png` - Médias por área e tipo de escola
2. `02_boxplots_distribuicao.png` - Distribuição de notas
3. `03_histograma_nota_media.png` - Distribuição da nota média geral
4. `04_densidade_nota_media.png` - Densidade das distribuições
5. `05_barras_empilhadas_desempenho.png` - Composição por faixas
6. `06_heatmap_correlacao.png` - Correlação entre áreas
7. `07_dispersao_matematica_linguagens.png` - Relação entre áreas
8. `08_linhas_composicao_faixas.png` - Proporção por faixa

### 📈 Tema Desempenho (8 gráficos)
1. `01_histograma_media_objetivas.png` - Distribuição das médias
2. `02_boxplot_redacao_grupos.png` - Redação por grupo
3. `03_dispersao_correlacao.png` - Correlação objetivas vs redação
4. `04_barras_medias_grupos.png` - Médias por grupo
5. `05_linhas_tendencia.png` - Tendências de crescimento
6. `06_heatmap_correlacao.png` - Correlação entre todas as notas
7. `07_densidade_distribuicao.png` - Densidade das distribuições
8. `08_barras_empilhadas_composicao.png` - Composição percentual

### 🏛️ Tema Institucional (8 gráficos)
1. `01_histograma_participantes_uf.png` - Participantes por UF
2. `02_boxplot_desempenho_regiao.png` - Desempenho por região
3. `03_dispersao_media_redacao.png` - Média geral vs redação
4. `04_barras_medias_regiao.png` - Médias por região
5. `05_linhas_desempenho_uf.png` - Desempenho por UF
6. `06_heatmap_medias_regionais.png` - Médias regionais por área
7. `07_densidade_notas_regiao.png` - Densidade por região
8. `08_barras_empilhadas_desempenho.png` - Composição do desempenho

### 👥 Tema Perfil do Estudante (8 gráficos)
1. `01_histograma_faixa_etaria.png` - Distribuição por idade
2. `02_violino_idade_conclusao.png` - Idade vs situação de conclusão
3. `03_stripplot_idade_civil_sexo.png` - Relação idade/civil/sexo
4. `04_barras_perfil_demografico.png` - Perfil geral
5. `05_linhas_proporcao_sexo_idade.png` - Proporção sexo por idade
6. `06_heatmap_civil_conclusao.png` - Estado civil vs conclusão
7. `07_densidade_idade_sexo.png` - Densidade de idade por sexo
8. `08_barras_empilhadas_conclusao_idade.png` - Situação por idade

### 💰 Tema Socioeconômico (8 gráficos)
1. `01_histograma_renda_cor_raca.png` - Renda por cor/raça
2. `02_boxplots_socieconomico_parental.png` - Fatores parentais
3. `03_dispersao_escolaridade_renda.png` - Escolaridade vs renda
4. `04_barras_escolaridade_parental.png` - Escolaridade dos pais
5. `05_linhas_escolaridade_parental.png` - Evolução da escolaridade
6. `06_heatmap_correlacao.png` - Correlação entre fatores
7. `07_densidade_renda_familiar.png` - Densidade da renda
8. `08_barras_empilhadas_renda.png` - Composição da renda

## 🛠️ Como Usar

### 1. Executar um tema específico
```bash
python tema_desempenho.py
python tema_academico.py
python tema_perfil_estudante.py
python tema_instucional.py
python tema_socieconomico.py
```

### 2. Testar todos os temas
```bash
python testar_temas.py
```

O script de teste oferece opções para:
- Testar um tema específico
- Testar todos os temas
- Verificar se os gráficos foram gerados corretamente

## 📋 Pré-requisitos

### Dados
- Certifique-se de que os arquivos CSV estão na pasta `DADOS/`
- Arquivos necessários: `PARTICIPANTES_2024.csv`, `RESULTADOS_2024.csv`, `ITENS_PROVA_2024.csv`

### Bibliotecas Python
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats
```

## 🔧 Melhorias Implementadas

1. **📁 Organização**: Gráficos organizados em pastas por tema
2. **📊 Qualidade**: Gráficos salvos em alta resolução (300 DPI)
3. **🔍 Nomenclatura**: Sistema de numeração e descrição padronizado
4. **🛡️ Robustez**: Criação automática de pastas com `os.makedirs(exist_ok=True)`
5. **📈 Eficiência**: Leitura otimizada dos dados da pasta DADOS
6. **🧪 Testes**: Script para validar o funcionamento de todos os temas

## 📝 Observações

- Todos os gráficos são salvos com `bbox_inches='tight'` para melhor aproveitamento do espaço
- As pastas são criadas automaticamente se não existirem
- Os gráficos são exibidos na tela E salvos no disco simultaneamente
- Cada tema mantém sua lógica de análise original, apenas com melhorias na organização

## 🎯 Resultados

Após executar os temas, você terá:
- **40 gráficos** organizados em 5 pastas temáticas
- **Análises completas** de diferentes aspectos do ENEM 2024
- **Visualizações de alta qualidade** prontas para apresentação ou relatórios