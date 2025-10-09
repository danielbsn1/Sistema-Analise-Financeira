#sistema para analise financeira de bolsa de valores com graficos e analise de indicadores
#para analise de acoes, precos, volume, tendencia, suporte e resistencia
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import mplfinance as mpf
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings("ignore")
# Configurações do matplotlib
plt.style.use('seaborn-darkgrid')
plt.rcParams['figure.figsize'] = (14, 7)

# Função para baixar dados de ações
def baixar_dados(ticker, start, end):
    """
    Baixa os dados históricos de ações usando yfinance.
    """
    dados = yf.download(ticker, start=start, end=end)
    return dados

# Função para calcular indicadores técnicos sem TA-Lib
def calcular_indicadores(dados):
    """
    Calcula indicadores técnicos como Médias Móveis, RSI, MACD e Bollinger Bands usando pandas/numpy.
    """
    # Médias móveis
    dados['SMA_20'] = dados['Close'].rolling(window=20).mean()
    dados['SMA_50'] = dados['Close'].rolling(window=50).mean()
    
    # RSI
    delta = dados['Close'].diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    media_ganho = ganho.rolling(window=14).mean()
    media_perda = perda.rolling(window=14).mean()
    rs = media_ganho / media_perda
    dados['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema_12 = dados['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = dados['Close'].ewm(span=26, adjust=False).mean()
    dados['MACD'] = ema_12 - ema_26
    dados['MACD_Signal'] = dados['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    dados['Middle_Band'] = dados['Close'].rolling(window=20).mean()
    std = dados['Close'].rolling(window=20).std()
    dados['Upper_Band'] = dados['Middle_Band'] + (std * 2)
    dados['Lower_Band'] = dados['Middle_Band'] - (std * 2)
    
    return dados

# Função para plotar gráficos de preços e indicadores
def plotar_graficos(dados, ticker):
    """
    Plota gráficos de preços e indicadores técnicos.
    """
    apds = [
        mpf.make_addplot(dados['SMA_20'], color='blue'),
        mpf.make_addplot(dados['SMA_50'], color='red'),
        mpf.make_addplot(dados['Upper_Band'], color='green', linestyle='--'),
        mpf.make_addplot(dados['Lower_Band'], color='green', linestyle='--')
    ]
    mpf.plot(dados, type='candle', style='charles', title=f'{ticker} Preços e Indicadores',
             ylabel='Preço (R$)', volume=True, addplot=apds)
    plt.show()

# Função para prever preços futuros usando regressão polinomial
def prever_precos(dados, grau=2):
    """
    Preve os preços futuros usando regressão polinomial.
    """
    dados['Date'] = pd.to_datetime(dados.index)
    dados['Date'] = (dados['Date'] - dados['Date'].min()).dt.days
    X = dados[['Date']]
    y = dados['Close']
    
    modelo = make_pipeline(PolynomialFeatures(degree=grau), LinearRegression())
    modelo.fit(X, y)
    
    previsoes = modelo.predict(X)
    
    mse = mean_squared_error(y, previsoes)
    r2 = r2_score(y, previsoes)
    
    print(f'MSE: {mse}, R²: {r2}')
    
    plt.plot(dados['Date'], y, label='Preços Reais', color='blue')
    plt.plot(dados['Date'], previsoes, label='Previsões', color='red')
    plt.title('Previsão de Preços Futuros')
    plt.xlabel('Dias desde o início')
    plt.ylabel('Preço (R$)')
    plt.legend()
    plt.show()

# Função principal para executar o sistema de análise financeira
def main():
    ticker = 'AAPL'  # Exemplo: Apple Inc.
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime.now()
    
    # Baixar dados
    dados = baixar_dados(ticker, start, end)
    
    # Calcular indicadores
    dados = calcular_indicadores(dados)
    
    # Plotar gráficos
    plotar_graficos(dados, ticker)
    
    # Prever preços futuros
    prever_precos(dados)

# Executar o sistema
if __name__ == "__main__":
    main()
# --- IGNORE ---
# End of file