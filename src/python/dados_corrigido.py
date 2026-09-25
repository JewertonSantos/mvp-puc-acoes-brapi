import requests
import pandas as pd
import time
import os

TICKERS = [
    "PETR4",
    "VALE3",
    "ITUB4",
    "MGLU3"
]

START_DATE = "2020-01-01"
END_DATE = "2026-12-31"

URL = "https://brapi.dev/api/quote/{}"

OUTPUT_FILE = "dividendos_2020_2026.csv"


def buscar_dividendos(ticker):
    url = URL.format(ticker)

    params = {
        "dividends": "true"
    }

    try:
        print()
        print("=" * 60)
        print("Buscando dividendos:", ticker)
        print("=" * 60)

        resposta = requests.get(
            url,
            params=params,
            timeout=60
        )

        print("Status HTTP:", resposta.status_code)

        if resposta.status_code == 401:
            print("A API pediu autenticacao.")
            print(resposta.text[:500])
            return []

        if resposta.status_code == 429:
            print("Limite de requisicoes atingido.")
            print("Aguardando 10 segundos...")
            time.sleep(10)
            return []

        resposta.raise_for_status()

        payload = resposta.json()

        resultados = payload.get("results", [])

        if not resultados:
            print("Nenhum resultado retornado.")
            return []

        ativo = resultados[0]

        dividends_data = ativo.get("dividendsData", {})

        if not isinstance(dividends_data, dict):
            print("dividendsData nao encontrado.")
            return []

        registros = []

        listas = [
            ("cashDividends", "cashDividend"),
            ("stockDividends", "stockDividend"),
            ("subscriptions", "subscription"),
            ("dividends", "dividend")
        ]

        for nome_lista, event_type in listas:
            lista = dividends_data.get(nome_lista, [])

            if not isinstance(lista, list):
                continue

            for evento in lista:
                if not isinstance(evento, dict):
                    continue

                registro = {
                    "symbol": ticker,
                    "eventType": event_type,
                    "label": evento.get("label"),
                    "rate": evento.get("rate"),
                    "approvedOn": evento.get("approvedOn"),
                    "lastDatePrior": evento.get("lastDatePrior"),
                    "exDate": evento.get("exDate"),
                    "paymentDate": evento.get("paymentDate"),
                    "relatedTo": evento.get("relatedTo"),
                    "isinCode": evento.get("isinCode"),
                    "remarks": evento.get("remarks")
                }

                registros.append(registro)

        print("Eventos encontrados:", len(registros))

        return registros

    except requests.exceptions.Timeout:
        print("Tempo limite excedido.")
        return []

    except requests.exceptions.RequestException as erro:
        print("Erro na requisicao:")
        print(erro)
        return []

    except ValueError as erro:
        print("Erro ao interpretar JSON:")
        print(erro)
        return []


def dentro_periodo(registro):
    datas = [
        registro.get("paymentDate"),
        registro.get("exDate"),
        registro.get("lastDatePrior"),
        registro.get("approvedOn")
    ]

    for data in datas:
        if not data:
            continue

        texto = str(data)[:10]

        if START_DATE <= texto <= END_DATE:
            return True

    return False


def main():
    todos_dividendos = []

    print()
    print("=" * 60)
    print("COLETA DE DIVIDENDOS BRAPI")
    print("=" * 60)
    print("Periodo:", START_DATE, "ate", END_DATE)
    print("Ativos:", ", ".join(TICKERS))
    print()

    for ticker in TICKERS:
        registros = buscar_dividendos(ticker)

        registros_periodo = [
            registro
            for registro in registros
            if dentro_periodo(registro)
        ]

        print(
            "Eventos dentro do periodo:",
            len(registros_periodo)
        )

        todos_dividendos.extend(registros_periodo)

        time.sleep(2)

    if not todos_dividendos:
        print()
        print("=" * 60)
        print("NENHUM DIVIDENDO ENCONTRADO")
        print("=" * 60)
        print()
        print("O arquivo CSV nao sera criado.")
        return

    df = pd.DataFrame(todos_dividendos)

    colunas = [
        "symbol",
        "eventType",
        "label",
        "rate",
        "approvedOn",
        "lastDatePrior",
        "exDate",
        "paymentDate",
        "relatedTo",
        "isinCode",
        "remarks"
    ]

    for coluna in colunas:
        if coluna not in df.columns:
            df[coluna] = None

    df = df[colunas]

    df = df.drop_duplicates()

    df = df.sort_values(
        by=[
            "symbol",
            "paymentDate",
            "exDate",
            "approvedOn"
        ],
        na_position="last"
    )

    pasta_script = os.path.dirname(
        os.path.abspath(__file__)
    )

    caminho_saida = os.path.join(
        pasta_script,
        OUTPUT_FILE
    )

    df.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print("=" * 60)
    print("ARQUIVO GERADO COM SUCESSO")
    print("=" * 60)
    print("Arquivo:", caminho_saida)
    print("Quantidade de registros:", len(df))
    print()

    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
