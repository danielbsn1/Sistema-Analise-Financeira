
Este arquivo implementa uma API web simples usando Flask para análise de dados financeiros de ações, com integração ao Yahoo Finance via yfinance. Ele calcula estatísticas como volatilidade, retorno anualizado e correlação, além de fornecer médias móveis.

---

## Sumário

- Descrição Geral
- Requisitos
- Endpoints
- Funções Principais
- Execução
- Exemplo de Uso

---

## Descrição Geral

O sistema permite consultar dados históricos de um ticker (ação) e retorna:
- Fechamento diário
- Média móvel de 20 dias (MA20)
- Retorno diário
- Estatísticas: volatilidade anualizada, retorno anualizado e correlação

---

## Requisitos

- Python 3.x
- Flask
- pandas
- numpy
- yfinance
- certifi

Instale as dependências com:
```
pip install flask pandas numpy yfinance certifi
```

---

## Endpoints

### `GET /`

Retorna a página inicial (`index.html`).  
**Uso:** Navegador ou cliente HTTP.

### `POST /get_data`

Recebe um JSON com o ticker da ação e retorna os dados processados.

**Request JSON:**
```json
{
  "ticker": "PETR4.SA"
}
```

**Response JSON:**
```json
{
  "dates": [...],
  "close": [...],
  "ma20": [...],
  "return": [...],
  "stats": {
    "volatility": ...,
    "annual_return": ...,
    "correlation": {...}
  }
}
```

**Códigos de resposta:**
- 200: Sucesso
- 400: Ticker não fornecido
- 404: Dados não encontrados
- 500: Erro interno

---

## Funções Principais

- **simplify_key(key):**  
  Simplifica chaves de tupla para string (usado na correlação).

- **calculate_statistics(df):**  
  Calcula retorno diário, média móvel de 20 dias, volatilidade anualizada, retorno anualizado e correlação entre colunas.

---

## Execução

Execute o arquivo com:
```
python Untitled-1.py
```
O servidor Flask estará disponível em `http://0.0.0.0:5000`.

---

## Exemplo de Uso

Faça uma requisição POST para `/get_data` com o ticker desejado:

```bash
curl -X POST http://localhost:5000/get_data -H "Content-Type: application/json" -d "{\"ticker\": \"PETR4.SA\"}"
```

---

## Observações

- O arquivo espera que exista um template `index.html` na pasta `templates`.
- O endpoint `/get_data` retorna dados para o último ano do ticker informado.
- O código já configura corretamente o certificado SSL para evitar erros de conexão com o Yahoo Finance.

