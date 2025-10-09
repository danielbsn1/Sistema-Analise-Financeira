import pandas as pd
from Back_end.sistema_analise_financeira import calcular_indicadores

def test_calcular_indicadores():
    df = pd.DataFrame({'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]})
    result = calcular_indicadores(df)
    assert 'SMA_20' in result.columns