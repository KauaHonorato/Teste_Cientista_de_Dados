# Teste_Cientista_de_Dados
Resolução do Teste para Cientista de dados da Pacto Tecnologia.

## Estrutura do Projeto

- **/data**
  - d_date.csv
  - f_transactions.csv
  - products.csv
  - users.csv

- **/src**
  - import requests.py

- **Receitas_de_Produtos.pbix**
  - Arquivo principal do dashboard no Power BI

## Objetivos

Realizar Extração de dados via API pública (Fake Store API), tratamento com Python e modelagem dimensional para análise no Power BI.
Realizar análise de transações e geração de indicadores de receita cumprindo com os requisitos do teste para Cientista de Dados.



## Tecnologias utilizadas:

- Python
- Pandas
- Power BI
- CSV

## Processo:
1-Os dados foram extraídos utilizando um Script em Python, e inseridos em um arquivo CSV;
2-Os arquivos gerados Foram importados como consultas para o Power BI;
3-Com as Consultas geradas, os dados foram manipulados para se adequar ao cenário ideal;
4-As colunas calculadas e Medidas em DAX foram criadas;
5-E as telas foram geradas com gráficos para compor o dashboard com os requisitos.

## Modelagem
Modelo estrela contendo:
- d_users
- d_products
- d_date
- f_transactions

## Indicadores Desenvolvidos
- Receita Total
- ARPU
- Usuários Ativos
- Receita por Categoria
- Top 5 Produtos

