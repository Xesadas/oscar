import dash
from dash import dcc, html
from socorro import sanitize_column_name
import pandas as pd  # Corrigindo a importação da função

# Função que cria os inputs do layout
def criar_inputs(df):
    inputs = []
    for col in df.columns:
        if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]:
            safe_col = sanitize_column_name(col)  # Corrigindo a chamada da função para usar apenas um argumento
            if col.lower() == "data":
                df[col] = pd.to_datetime(df[col], errors='coerce')  # Converte para datetime, valores inválidos viram NaT
                inputs.append(html.Div([
                    html.Label(col),
                    dcc.DatePickerSingle(id=f'input-{safe_col}', date=df[col].max())
                ], style={'marginBottom': '10px'}))
            else:
                inputs.append(html.Div([  
                    html.Label(col),
                    dcc.Input(id=f'input-{safe_col}', type='text', value='')  # Corrigido para aceitar o valor padrão
                ], style={'marginBottom': '10px'}))
    return inputs
