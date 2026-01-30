import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

# CONFIGURAÇÕES GERAIS
TICKERS = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA", "ABEV3.SA"]
DATA_INICIO = "2023-01-01"
NOME_BANCO = 'dados_investimentos.db'

def obter_conexao():
    return sqlite3.connect(NOME_BANCO)

def extrair_dimensao_empresas(lista_tickers):
    print(f"\n[1/3] Atualizando Metadados das Empresas...")
    dados_cadastrais = []
    
    for ticker in lista_tickers:
        try:
            acao = yf.Ticker(ticker)
            info = acao.info
            site_limpo = info.get('website', '').replace('https://', '').replace('http://', '').split('/')[0]

            dados_cadastrais.append({
                'Ticker': ticker,
                'Empresa': info.get('longName'),
                'Setor': info.get('sector'),
                'Market_Cap': info.get('marketCap'),
                'Cidade': info.get('city'),
                'Estado': info.get('state'),
                'Pais': info.get('country'),
                'Logo_URL': f"https://www.google.com/s2/favicons?domain={site_limpo}&sz=128"
            })
        except Exception as e:
            print(f"-- Erro nos metadados de {ticker}: {e}")

    df_dim = pd.DataFrame(dados_cadastrais)
    with obter_conexao() as conn:
        df_dim.to_sql('d_empresa', conn, if_exists='replace', index=False)
    print("-- Tabela d_empresa atualizada!")

def extrair_contabilidade_trimestral(lista_tickers):
    print(f"\n[2/3] Extraindo Dados Contábeis (Trimestrais)...")
    lista_frames = []

    for t in lista_tickers:
        try:
            acao = yf.Ticker(t)
            dre_trim = acao.quarterly_financials.T
            balanco_trim = acao.quarterly_balance_sheet.T
            
            if dre_trim.empty or balanco_trim.empty:
                print(f"-- Dados trimestrais ausentes para {t}")
                continue

            df_unificado = dre_trim.join(balanco_trim, how='outer', lsuffix='_dre', rsuffix='_bal')
            df_unificado['Ticker'] = t
            df_unificado['Data_Referencia'] = df_unificado.index
            
            colunas_foco = [
                'Ticker', 'Data_Referencia', 'Net Income', 'Total Revenue', 
                'EBITDA', 'Stockholders Equity', 'Total Debt', 'Cash And Cash Equivalents'
            ]
            
            disponiveis = [c for c in colunas_foco if c in df_unificado.columns]
            lista_frames.append(df_unificado[disponiveis])
        except Exception as e:
            print(f"-- Erro contábil em {t}: {e}")

    if lista_frames:
        df_final = pd.concat(lista_frames)
        with obter_conexao() as conn:
            df_final.to_sql('f_contabilidade_trimestral', conn, if_exists='replace', index=False)
        print("-- Tabela f_contabilidade_trimestral atualizada!")

def extrair_historico_precos(lista_tickers):
    print(f"\n[3/3] Extraindo Histórico de Preços...")
    try:
        df_bruto = yf.download(lista_tickers, start=DATA_INICIO)
        df_empilhado = df_bruto.stack(level=1).reset_index()
        df_final = df_empilhado.rename(columns={'Date': 'Data', 'level_1': 'Ticker'})
        
        with obter_conexao() as conn:
            df_final.to_sql('f_historico_ativos', conn, if_exists='replace', index=False)
        print("-- Tabela f_historico_ativos atualizada!")
    except Exception as e:
        print(f"-- Erro ao extrair preços: {e}")

if __name__ == "__main__":
    start_time = datetime.now()
    print(f"-- Iniciando Extração Integrada - {start_time.strftime('%H:%M:%S')}")
    
    extrair_dimensao_empresas(TICKERS)
    extrair_contabilidade_trimestral(TICKERS)
    extrair_historico_precos(TICKERS)
    
    end_time = datetime.now()
    print(f"\n-- Processo concluído em: {end_time - start_time}")
    print(f"- Banco de dados pronto: {NOME_BANCO}")