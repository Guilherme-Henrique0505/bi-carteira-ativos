import yfinance as yf
import pandas as pd
import sqlite3

tickers = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA", "ABEV3.SA"]
lista_frames = []

for t in tickers:
    print(f"Puxando dados contábeis consolidados de: {t}")
    acao = yf.Ticker(t)
    
    # Puxa os dois demonstrativos (DRE e Balanço)
    dre_trim = acao.quarterly_financials.T
    balanco_trim = acao.quarterly_balance_sheet.T
    
    # Une as duas tabelas pela data 
    # O join garante que as linhas batam exatamente na mesma data
    df_unificado = dre_trim.join(balanco_trim, how='outer', lsuffix='_dre', rsuffix='_bal')
    
    # Adiciona as colunas de controle
    df_unificado['Ticker'] = t
    df_unificado['Data_Referencia'] = df_unificado.index
    
    # Mapeamento das colunas
    colunas_foco = [
        'Ticker', 'Data_Referencia', 
        'Net Income', 'Total Revenue', 'EBITDA', 
        'Stockholders Equity', 'Total Debt', 'Cash And Cash Equivalents'
    ]
    
    # Filtra apenas o que existe para não dar erro
    disponiveis = [c for c in colunas_foco if c in df_unificado.columns]
    
    lista_frames.append(df_unificado[disponiveis])

# Consolida todos os ativos
df_final = pd.concat(lista_frames)

# Salva no banco
conn = sqlite3.connect('dados_investimentos.db')
df_final.to_sql('f_contabilidade_trimestral', conn, if_exists='replace', index=False)
conn.close()

print("\n✅ Sucesso! Tabela f_contabilidade_trimestral criada com indicadores de retorno e saúde financeira.")