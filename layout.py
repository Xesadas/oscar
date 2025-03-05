from dash import dcc, html
import pandas as pd
import re

# Carregar dados
file_path = "p.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# Função para normalizar os IDs removendo caracteres inválidos
def sanitize_column_name(col_name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', col_name)  # Substitui caracteres inválidos por _

# Criar o layout com inputs para cada coluna
def criar_inputs():
    inputs = []
    for col in df.columns:
        if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]:
            safe_col = sanitize_column_name(col)
            if col.lower() == "data":
                df[col] = pd.to_datetime(df[col], errors='coerce')  # Converte para datetime, valores inválidos viram NaT
                inputs.append(html.Div([
                    html.Label(col),
                    dcc.DatePickerSingle(id=f'input-{safe_col}', date=df[col].max())
                ], style={'marginBottom': '10px'}))
            else:
                inputs.append(html.Div([
                    html.Label(col),
                    dcc.Input(id=f'input-{safe_col}', type='text', value='')
                ], style={'marginBottom': '10px'}))
    return inputs

# Layout do dashboard
layout = html.Div([
    html.H1("Dashboard de Transações"),
    html.Div(criar_inputs()),
    html.Button("Salvar", id="salvar-btn", n_clicks=0),
    html.Div(id="output-mensagem")
])