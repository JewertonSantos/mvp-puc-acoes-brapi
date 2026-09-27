# Arquitetura do Projeto

## 1. Visão geral

Este projeto implementa um pipeline de dados para análise fundamentalista de ações brasileiras, utilizando dados obtidos da BRAPI e processados no Databricks.

A arquitetura segue o conceito de medalhão, dividindo o processamento em três camadas principais:

- **Bronze:** dados brutos carregados no Databricks.
- **Silver:** dados tratados, padronizados e reduzidos às colunas necessárias.
- **Gold:** dados consolidados e métricas utilizadas na análise fundamentalista.

O fluxo geral é:

BRAPI → Python → CSV → Volume Databricks → Bronze → Silver → Gold → Análise fundamentalista

---

## 2. Origem dos dados

Os dados financeiros e históricos das ações são obtidos por meio da BRAPI. Os dados que a plataforma disponibiliza gratuitamente via API são limitados, deixando apenas 4 ativos disponíveis.

Os ativos analisados neste projeto são:

- PETR4
- VALE3
- ITUB4
- MGLU3

O período considerado para a coleta é:

**01/01/2020 a 31/12/2026**

No entanto, os dados vão até os dias em que o código foi rodado, já que foi executado antes do dia 31. Como parte da análise se baseia em dados de intervalos até 5 anos, não tem problema de não estar completo o ano de 2026.
A coleta é realizada pelo script Python:

`src/python/dados_corrigido.py`

Os dados coletados são armazenados em arquivos CSV.

---

## 3. Armazenamento dos arquivos

Os arquivos CSV são armazenados em um Volume do Databricks:

`/Volumes/workspace/brapi_csv/brapi_base/`

O Volume funciona como área de armazenamento dos arquivos utilizados na ingestão dos dados.

Os arquivos CSV não fazem parte do repositório GitHub, pois o GitHub é utilizado para versionamento do código, notebooks e documentação do projeto.

---

## 4. Camada Bronze

A camada Bronze representa os dados carregados a partir dos arquivos CSV, mantendo uma estrutura próxima à origem. Foram trazidas todas as tabelas que a API da BRAPI disponibiliza gratuitamente para os quatro ativos, de modo que ainda seria definido quais colunas ou quais tabelas ainda seriam usadas de fato no projeto.

Os arquivos são lidos utilizando Spark e posteriormente gravados como tabelas Delta no schema:

`workspace.bronze`

As tabelas Bronze utilizadas no projeto são:

- `workspace.bronze.cotacoes`
- `workspace.bronze.estatisticas`
- `workspace.bronze.dados_financeiros`
- `workspace.bronze.balanco_patrimonial`
- `workspace.bronze.demonstracao_resultados`
- `workspace.bronze.fluxo_caixa`
- `workspace.bronze.valor_adicionado`
- `workspace.bronze.dividendos`

O notebook responsável pela carga é:

`notebooks/bronze/01_carga_bronze`

---

## 5. Camada Silver

A camada Silver realiza a preparação dos dados para utilização nas análises.

Nesta etapa são selecionadas as colunas necessárias, padronizados os dados e preservada a granularidade adequada para cada conjunto de informações.

As tabelas Silver utilizadas na análise são:

- `workspace.silver.cotacoes`
- `workspace.silver.estatisticas`
- `workspace.silver.dados_financeiros`
- `workspace.silver.demonstracao_resultados`
- `workspace.silver.dividendos`

As tabelas Bronze de balanço patrimonial, fluxo de caixa e valor adicionado não foram transformadas para Silver porque não são necessárias para os critérios definidos no MVP.

O notebook responsável por esta etapa é:

`notebooks/silver/02_carga_silver`

---

## 6. Camada Gold

A camada Gold consolida os dados tratados e aplica as regras de negócio utilizadas na análise fundamentalista.

Entre as informações calculadas estão:

- preço atual;
- P/L;
- P/VP;
- P/VP × P/L;
- EPS;
- valor patrimonial por ação;
- margem líquida;
- ROE;
- EBITDA;
- dívida total;
- caixa;
- dívida líquida;
- dívida líquida/EBITDA;
- dividendos médios dos últimos cinco anos;
- dividend yield médio dos últimos cinco anos;
- CAGR do lucro em cinco anos;
- preço teto pelo método de Bazin;
- valor justo pelo método de Graham;
- valor máximo de compra considerando margem de segurança de 25%.

As principais tabelas Gold são:

- `workspace.gold.analise_acoes`
- `workspace.gold.crescimento_lucros`
- `workspace.gold.criterios_acoes`

O notebook responsável pela construção das análises é:

`notebooks/gold/03_carga_gold`

---

## 7. Data Catalog

O projeto também possui documentação dos dados e das regras utilizadas.

O notebook:

`notebooks/gold/04_DataCatalog`

é utilizado para apoiar a documentação e o catálogo das tabelas.

As tabelas possuem comentários de contexto e descrição das colunas, permitindo identificar o significado dos dados utilizados na análise.

---

## 8. Versionamento

O código e a documentação do projeto são versionados utilizando GitHub por meio de um Git Folder do Databricks.

Repositório:

`mvp-puc-acoes-brapi`

A estrutura principal do repositório é:

```text
mvp-puc-acoes-brapi/
├── README.md
├── documentacao/
├── src/
│   └── python/
├── notebooks/
    ├── bronze/
    ├── silver/
    └── gold/
