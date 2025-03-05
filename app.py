import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import re

# Carregar dados
file_path = "p.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# Função para normalizar os IDs removendo caracteres inválidos
def sanitize_column_name(col_name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', col_name)  # Substitui caracteres inválidos por _

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Criar o layout com inputs para cada coluna
def criar_inputs():
    inputs = []
    for col in df.columns:
        safe_col = sanitize_column_name(col)
        inputs.append(html.Div([
            html.Label(col),
            dcc.Input(id=f'input-{safe_col}', type='text', value='')
        ], style={'marginBottom': '10px'}))
    return inputs

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Transações"),
    html.Div(criar_inputs()),
    html.Button("Salvar", id="salvar-btn", n_clicks=0),
    html.Div(id="output-mensagem")
])

# Callback para capturar inputs e exibir mensagem de confirmação
@app.callback(
    Output("output-mensagem", "children"),
    Input("salvar-btn", "n_clicks"),
    [State(f"input-{sanitize_column_name(col)}", "value") for col in df.columns]
)
def salvar_dados(n_clicks, *valores):
    if n_clicks > 0:
        dados = {col: val for col, val in zip(df.columns, valores)}
        return f"Dados inseridos: {dados}"
    return ""

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
#teste!