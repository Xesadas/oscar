import dash
from dash import dcc, Input, Output, State, html, dash_table
import pandas as pd
from layout_config import criar_inputs
from socorro import sanitize_column_name

# Carregar dados do Excel e garantir que a coluna DATA seja datetime
file_path = "p.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# Converter coluna DATA para datetime (caso o parse_dates não tenha funcionado)
df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Transações"),
    html.Div(criar_inputs(df)),

    dcc.DatePickerRange(
        id="date-picker",
        start_date=df["DATA"].min(),
        end_date=df["DATA"].max(),
        display_format="DD/MM/YYYY"
    ),

    dash_table.DataTable(
        id="tabela-dados",
        columns=[{"name": col, "id": sanitize_column_name(col)} for col in df.columns],
        data=df.to_dict("records"),
        page_size=10
    ),

    html.Button("Salvar Dados", id="salvar-btn", n_clicks=0),
    html.Div(id="output-mensagem"),
    dcc.Store(id="stored-data", storage_type='memory')
])

# -------------------------
# Callback para filtrar dados
# -------------------------
@app.callback(
    Output("tabela-dados", "data"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def filtrar_dados(start_date, end_date):
    # Criar uma cópia do DataFrame original para evitar modificações globais
    df_filtrado = df.copy()
    
    # Converter datas do DatePicker para datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filtrar dados entre as datas
    mask = (df_filtrado["DATA"] >= start_date) & (df_filtrado["DATA"] <= end_date)
    df_filtrado = df_filtrado.loc[mask]
    
    # Converter datas para string (formato DD/MM/YYYY) para exibição
    df_filtrado["DATA"] = df_filtrado["DATA"].dt.strftime("%d/%m/%Y")
    
    return df_filtrado.to_dict("records")


# 📌 Preenche automaticamente os dados com base no beneficiário
def preencher_automaticamente(dados, df):
    beneficiario = dados.get("BENEFICIÁRIO", "")
    if beneficiario:
        registros_anteriores = df[df["BENEFICIÁRIO"] == beneficiario]
        if not registros_anteriores.empty:
            dados["MÁQUINA"] = registros_anteriores["MÁQUINA"].iloc[-1]
            valores = pd.to_numeric(registros_anteriores["VALOR"], errors="coerce")  # Garante que VALOR seja float
            dados["PORCENTAGEM"] = f"{(dados.get('VALOR', 0) / valores.mean()) * 100:.2f}%" if not valores.empty else "0%"
        else:
            dados["MÁQUINA"] = "PAGSEGURO"
            dados["PORCENTAGEM"] = "0%"
    return dados

# 📌 Salva os dados no Excel
@app.callback(
    Output("output-mensagem", "children"),
    Output("stored-data", "data"),
    Input("salvar-btn", "n_clicks"),
    State("stored-data", "data"),
    *[State(f"input-{sanitize_column_name(col)}", "value") for col in df.columns]
)
def salvar_dados(n_clicks, stored_data, *valores):
    if n_clicks > 0:
        dados = {col: val for col, val in zip(df.columns, valores)}
        dados = preencher_automaticamente(dados, df)
        novo_registro = pd.DataFrame([dados])
        df_atualizado = pd.concat([df, novo_registro], ignore_index=True).drop_duplicates()
        df_atualizado.to_excel(file_path, index=False, engine="openpyxl")
        return f"Dados inseridos: {dados}", stored_data

    return "", stored_data

if __name__ == "__main__":
    app.run_server(debug=True)