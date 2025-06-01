# Sistema de Análise Financeira

Este projeto é um sistema web para análise financeira de ações, desenvolvido em Python com Flask. Ele permite consultar dados históricos de ativos financeiros, calcular estatísticas como volatilidade e retorno anualizado, e visualizar gráficos interativos.

## Funcionalidades

- Consulta de dados históricos de ações (Yahoo Finance)
- Cálculo de volatilidade anualizada e retorno anualizado médio
- Exibição de matriz de correlação entre variáveis
- Gráficos interativos de preços e retornos com Plotly

## Como rodar

1. Instale as dependências:
   ```
   pip install flask pandas numpy yfinance certifi
   ```

2. Execute o app:
   ```
   python app.py
   ```

3. Acesse no navegador:
   ```
   http://127.0.0.1:5000
   ```

## Estrutura

```
analise de dados/
│   app.py
│
└───templates/
    │   index.html
```

## Observações

- Para ações brasileiras, use o sufixo `.SA` (ex: PETR4.SA).
- Se tiver problemas de certificado SSL no Windows, veja as instruções no código.

---

Desenvolvido por [danielbsn1](https://github.com/danielbsn1)
