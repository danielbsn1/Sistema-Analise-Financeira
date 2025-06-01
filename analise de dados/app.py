import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import yfinance as yf

app = Flask(__name__)

def simplify_key(key):
    if isinstance(key, tuple):
        return key[0]
    return key

def calculate_statistics(df):
    stats = {}
    df['Return'] = df['Close'].pct_change()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    # Volatilidade anualizada (desvio padrão do retorno diário * sqrt(252))
    stats['volatility'] = float(df['Return'].std() * np.sqrt(252))
    # Retorno médio anualizado
    stats['annual_return'] = float(df['Return'].mean() * 252)
    # Correlação entre colunas (geralmente só tem 'Close' e 'MA20', para exemplo)
    corr = df.corr()
    corr_dict = {simplify_key(k): {simplify_key(kk): vv for kk, vv in v.items()} for k, v in corr.to_dict().items()}
    stats['correlation'] = corr_dict
    df.fillna(0, inplace=True)
    return stats, df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    json_data = request.get_json()
    ticker = json_data.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker não fornecido'}), 400
    try:
        data = yf.download(ticker, period='1y')
        if data.empty:
            return jsonify({'error': 'Dados não encontrados para o ticker informado'}), 404
        stats, data_processed = calculate_statistics(data)
        response = {
            'dates': data_processed.index.strftime('%Y-%m-%d').tolist(),
            'close': data_processed['Close'].values.tolist(),
            'ma20': data_processed['MA20'].values.tolist(),
            'return': data_processed['Return'].values.tolist(),
            'stats': stats
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
