# Critérios de Análise Fundamentalista

## 1. Objetivo

Esta análise tem como objetivo aplicar critérios fundamentalistas às ações:

- PETR4
- VALE3
- ITUB4
- MGLU3

Os critérios são utilizados como exercício de análise de investimentos dentro do MVP. A comparação entre as empresas possui limitações, pois os ativos pertencem a setores econômicos diferentes.

Os critérios são aplicados individualmente e apresentados na camada Gold, sem a criação de uma pontuação única para as empresas.

---

## 2. Preço atual

O preço atual corresponde ao último preço de fechamento disponível na tabela de cotações.

Campo:

`preco_atual`

Origem:

`workspace.silver.cotacoes`

Regra:

- selecionar o registro mais recente disponível para cada ativo;
- utilizar o campo `close`.

---

## 3. P/L

O P/L (Preço sobre Lucro) representa a relação entre o preço da ação e o lucro por ação.

Neste projeto, é utilizado diretamente o indicador `trailingPE` fornecido pela BRAPI.

Campo:

`pl`

Origem:

`workspace.silver.estatisticas`

Para a análise, valores menores de P/L representam uma relação preço/lucro menor.

---

## 4. P/VP

O P/VP (Preço sobre Valor Patrimonial) representa a relação entre o preço da ação e seu valor patrimonial por ação.

Neste projeto, é utilizado diretamente o indicador `priceToBook` fornecido pela BRAPI.

Campo:

`pvp`

Origem:

`workspace.silver.estatisticas`

O valor patrimonial por ação utilizado na análise corresponde ao campo:

`bookValue`

---

## 5. Relação P/VP × P/L

É calculado o produto entre P/VP e P/L:

`P/VP × P/L`

Regra utilizada:

`P/VP × P/L ≤ 22,5`

O limite de 22,5 é utilizado como referência associada ao critério de Benjamin Graham.

Campo:

`pvp_x_pl`

---

## 6. Dividend Yield

O Dividend Yield utilizado na análise é calculado com base no histórico de dividendos dos últimos cinco anos.

Para cada ano:

`DY anual = dividendos/proventos do ano ÷ preço de fechamento no final do ano`

O Dividend Yield médio é calculado pela média dos DY anuais do período de 2021 a 2025.

Campo:

`dy_medio_5_anos_pct`

Critério:

`DY médio ≥ 6%`

São considerados os proventos registrados na tabela de dividendos, incluindo dividendos e JCP.

---

## 7. Dividendos médios em reais

Também é calculada a média anual dos dividendos/proventos pagos por ação no período de cinco anos.

Campo:

`dividendos_medio_5_anos_reais`

Esse valor é utilizado no cálculo do preço teto pelo método de Bazin.

---

## 8. Crescimento do lucro

O crescimento do lucro é medido pelo CAGR (Compound Annual Growth Rate) do lucro líquido.

São utilizados os resultados anuais de 2021 a 2025.

A fórmula utilizada é:

`CAGR = (Lucro final / Lucro inicial)^(1/4) - 1`

O período possui quatro intervalos entre 2021 e 2025.

Critério:

`CAGR > 12% ao ano`

Campo:

`crescimento_lucro_cagr_5_anos_pct`

Quando não existem dados suficientes ou os valores inicial/final não permitem o cálculo, o indicador é mantido como dado ausente.

---

## 9. Margem líquida

A margem líquida representa a proporção da receita que permanece como lucro líquido.

Neste projeto, é utilizado diretamente o indicador `profitMargins` fornecido pela BRAPI.

Campo:

`margem_liquida`

Critério:

`margem líquida ≥ 10%`

---

## 10. ROE

O ROE (Return on Equity) representa o retorno sobre o patrimônio líquido.

Neste projeto, é utilizado diretamente o indicador `returnOnEquity` fornecido pela BRAPI.

Campo:

`roe`

Critério:

`ROE ≥ 10%`

---

## 11. EBITDA

O EBITDA utilizado na análise é o valor fornecido pela BRAPI.

Campo:

`ebitda`

Origem:

`workspace.silver.dados_financeiros`

O indicador é utilizado principalmente para avaliar a relação entre dívida líquida e capacidade operacional de geração de resultado.

---

## 12. Dívida líquida

A dívida líquida é calculada pela diferença entre dívida total e caixa:

`Dívida líquida = Dívida total - Caixa`

Campos utilizados:

- `totalDebt`
- `totalCash`

Resultado:

`divida_liquida`

---

## 13. Dívida líquida / EBITDA

É calculada a relação entre dívida líquida e EBITDA:

`Dívida líquida / EBITDA`

Campo:

`divida_liquida_ebitda`

Critério:

`Dívida líquida / EBITDA < 5`

Quando dívida ou EBITDA não estão disponíveis, o critério é apresentado como `SEM DADO`.

---

## 14. Preço teto de Bazin

O preço teto pelo método de Bazin é calculado utilizando a média dos dividendos por ação dos últimos cinco anos.

Fórmula:

`Preço teto Bazin = Dividendos médios de 5 anos / 0,06`

O percentual de 6% representa o Dividend Yield mínimo utilizado como referência.

Campo:

`preco_teto_bazin`

---

## 15. Valor justo de Graham

O valor justo de Graham é calculado utilizando:

- EPS (lucro por ação);
- valor patrimonial por ação.

Fórmula:

`Valor justo = √(22,5 × EPS × Valor patrimonial por ação)`

Campos utilizados:

- `trailingEps`
- `bookValue`

Resultados:

- `eps`
- `valor_patrimonial`
- `valor_justo_graham`

---

## 16. Margem de segurança de 25%

Além do valor justo de Graham, é calculado um preço máximo considerando uma margem de segurança de 25%.

Fórmula:

`Preço máximo = Valor justo de Graham × 0,75`

Campo:

`preco_max_graham_25`

Esse valor representa 75% do valor justo calculado.

---

## 17. Classificação dos critérios

Cada critério é avaliado individualmente.

Os possíveis resultados são:

- `ATENDE`
- `NÃO ATENDE`
- `SEM DADO`

`ATENDE` indica que o indicador satisfaz a regra definida.

`NÃO ATENDE` indica que o indicador não satisfaz a regra.

`SEM DADO` indica que não existem informações suficientes para aplicar o critério.

Não é calculada uma pontuação ou classificação geral das empresas.

---

## 18. Limitações

Os critérios possuem caráter educacional dentro do MVP e não representam, isoladamente, uma recomendação de investimento.

Alguns indicadores dependem da disponibilidade e da qualidade dos dados fornecidos pela BRAPI.

A análise também apresenta limitações decorrentes da comparação de empresas pertencentes a setores diferentes.

No cálculo do CAGR, anos com lucro negativo podem tornar a trajetória de crescimento pouco representativa, mesmo quando o cálculo entre o primeiro e o último ano é matematicamente possível.

Por isso, os resultados devem ser interpretados em conjunto com os indicadores individuais e com a disponibilidade dos dados.