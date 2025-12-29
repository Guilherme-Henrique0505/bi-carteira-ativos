import yfinance as yf
import sqlite3  
import pandas as pd
from datetime import datetime

tickers = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA", "ABEV3.SA"]
data_inicio = "2023-01-01"

def capturar_e_tratar(lista):
    print(f"Extraindo dados para {lista}...")

    df_bruto = yf.download(lista, start=data_inicio) 
    df_empilhado = df_bruto.stack(level=1) #empilhamento: colunas em tickers em linhas
    df_final = df_empilhado.reset_index() #transformar index em colunas, data e tickers
    df_final = df_final.rename(columns={
        'Date': 'Data',
        'level_1': 'Ticker' 
    }) #renomear colunas

    return df_final

def salvar_no_banco(df, nome_tabela="historico_ativos"):
    try:
        conn = sqlite3.connect('dados_investimentos.db') #salva no banco
        df.to_sql(nome_tabela, conn, if_exists='replace', index=False) #salva o df no sql

        conn.close()
        print(f"Sucesso, dados salvos no banco 'dados_investimentos.db na tabela '{nome_tabela}'")
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")


if __name__ == "__main__":
    df_carteira = capturar_e_tratar(tickers)

# Salva no banco
    if not df_carteira.empty:
        salvar_no_banco(df_carteira)
        print(f"\n--- Primeiras linhas do banco de dados ---")
        print(df_carteira.head(10))