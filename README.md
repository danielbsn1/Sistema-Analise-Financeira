# SISTEMA PARA   ANALISE DE DADOS FINANCEIRO
# Sistema de Análise Financeira

Resumo
---
Ferramenta para análise de séries históricas de ações: coleta de dados, cálculo de indicadores técnicos, geração de gráficos e previsões de preço. Back-end em Python; front-end em HTML/CSS/JavaScript.

Funcionalidades
---
- Download de dados históricos via yfinance
- Cálculo de indicadores (SMA, RSI, MACD, Bollinger Bands) com pandas/numpy
- Gráficos interativos de candles e indicadores (mplfinance / matplotlib)
- Previsão de preços por regressão polinomial (scikit-learn)
- Separação clara entre Front-end e Back-end

Stack Tecnológico
---
- Python 3.11/3.12 (recomendado)
- pandas, numpy, matplotlib, yfinance, mplfinance, scikit-learn
- HTML / CSS / JavaScript para o front-end

Estrutura do Projeto
---
```
Sistema-Analise-Financeira/
├── Back-end/
│   ├── sistema_analise_financeira.py
│   └── __init__.py
├── Front-end/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── tests/
│   └── test_indicadores.py
├── requirements.txt
├── README.md
└── .gitignore
```
