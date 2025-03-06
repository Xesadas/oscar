import dash
from dash import dcc, Input, Output, State, html, dash_table
import pandas as pd
from layout_config import criar_inputs  # Importando a função de layout
from socorro import sanitize_column_name  # Corrigindo a importação da função

# Carregar dados do Excel
file_path = "p.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")
df["DATA"] = pd.to_datetime(df["DATA"], errors='coerce')  # Converter a coluna DATA para datetime

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dashboard de Transações"),
    
    # Adiciona apenas os inputs gerados pela função
    html.Div(criar_inputs(df)),
    
    dcc.DatePickerRange(
        id="date-picker",
        start_date=df["DATA"].min(),
        end_date=df["DATA"].max(),
        display_format="DD/MM/YYYY"
    ),
    
    dash_table.DataTable(
        id="tabela-dados",
        columns=[{"name": col, "id": sanitize_column_name(col)} for col in df.columns],  # Corrigido
        data=df.to_dict("records"),  # Carregar os dados iniciais
        page_size=10,
        style_table={'overflowX': 'auto'}
    ),
    
    # Adicionando o botão de salvar
    html.Div([
        html.Button("Salvar Dados", id="salvar-btn", n_clicks=0)
    ], style={'marginTop': '20px'}),
    
    # Componente de saída para exibir a mensagem
    html.Div(id="output-mensagem", style={'marginTop': '10px'}),
    
    # Componente dcc.Store para armazenar os dados temporários
    dcc.Store(id="stored-data", storage_type='memory')
])

# Callback para filtrar os dados com base nas datas
@app.callback(
    Output("tabela-dados", "data"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def filtrar_dados(start_date, end_date):
    global df
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Filtra os dados entre as datas fornecidas, garantindo que a comparação de datas seja feita corretamente
        df_filtrado = df[(df["DATA"] >= start_date) & (df["DATA"] <= end_date)]
        # Verifica se o filtro não resultou em um DataFrame vazio
        if not df_filtrado.empty:
            return df_filtrado.drop_duplicates().to_dict("records")  # Remove valores duplicados
    # Caso contrário, retorna todos os dados
    return df.to_dict("records")

# Callback para salvar os dados
@app.callback(
    Output("output-mensagem", "children"),
    Output("stored-data", "data"),
    Input("salvar-btn", "n_clicks"),
    [State(f"input-{sanitize_column_name(col)}", "date" if col.lower() == "data" else "value") for col in df.columns if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]],
    State("stored-data", "data")
)
def salvar_dados(n_clicks, *valores, stored_data):
    global df
    if n_clicks > 0:
        if stored_data is None:
            stored_data = []

        # Coletar os valores dos inputs
        dados = {col: val for col, val in zip([col for col in df.columns if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]], valores)}
        
        # Adicionar valores fixos
        dados["MÁQUINA"] = "PAGSEGURO"
        dados["COMISSÃO ALESSANDRO"] = "Valor calculado"
        dados["VALOR DUALCRED"] = "Valor calculado"
        dados["%TRANS."] = "Valor calculado"
        dados["%LIBERAD."] = "Valor calculado"
        
        # Adicionar os novos dados ao stored_data
        stored_data.append(dados)

        # Atualizar o DataFrame e salvar no Excel sem duplicatas
        novo_registro = pd.DataFrame([dados])
        df = pd.concat([df, novo_registro], ignore_index=True).drop_duplicates()
        df.to_excel(file_path, index=False, engine="openpyxl")

        return f"Dados inseridos: {dados}", stored_data
    return "", stored_data

if __name__ == "__main__":
    app.run_server(debug=True)
