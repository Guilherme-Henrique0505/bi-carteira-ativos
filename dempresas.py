import yfinance as yf
import pandas as pd
import sqlite3

def atualizar_dimensao_empresas(lista_tickers):
    dados_cadastrais = []
    
    for ticker in lista_tickers:
        print(f"Buscando metadados de: {ticker}...")
        try:
            acao = yf.Ticker(ticker)
            info = acao.info
            site_limpo = info.get('website', '').replace('https://', '').replace('http://', '').split('/')[0]

            dados_cadastrais.append({
                'Ticker': ticker,
                'Empresa': info.get('longName'),
                'Setor': info.get('sector'),
                'Market_Cap': info.get('marketCap'), # Este é o Valor de Mercado atual
                'Cidade': info.get('city'),
                'Estado': info.get('state'),
                'Pais': info.get('country'),
                'Logo_URL': f"https://www.google.com/s2/favicons?domain={site_limpo}&sz=128"
            })
        except Exception as e:
            print(f"Erro ao puxar {ticker}: {e}")

    df_dim = pd.DataFrame(dados_cadastrais)

    # Conecta no banco
    conn = sqlite3.connect('dados_investimentos.db')
    df_dim.to_sql('d_empresa', conn, if_exists='replace', index=False)
    conn.close()
    print("\n✅ Tabela d_empresa atualizada no banco SQL!")

if __name__ == "__main__":
    meus_tickers = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA", "ABEV3.SA"]
    atualizar_dimensao_empresas(meus_tickers)