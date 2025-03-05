import dash
from dash import Input, Output, State
import pandas as pd
from layout import layout, sanitize_column_name

# Carregar dados
file_path = "p.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)
app.layout = layout

# Callback para capturar inputs e exibir mensagem de confirmação
@app.callback(
    Output("output-mensagem", "children"),
    Output("stored-data", "data"),
    Output("tabela-dados", "data"),
    Input("salvar-btn", "n_clicks"),
    [State(f"input-{sanitize_column_name(col)}", "value") for col in df.columns if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]],
    State("stored-data", "data")
)
def salvar_dados(n_clicks, *valores, stored_data):
    if n_clicks > 0:
        # Se stored_data for None (primeira vez que a função é chamada), inicialize como uma lista vazia
        if stored_data is None:
            stored_data = []

        # Organizar os dados
        dados = {col: val for col, val in zip([col for col in df.columns if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]], valores)}

        # Calcular os valores das colunas automáticas
        dados["MÁQUINA"] = "PAGSEGURO"  # Substitua com a lógica de cálculo real
        dados["COMISSÃO ALESSANDRO"] = "Valor calculado"  # Substitua com a lógica de cálculo real
        dados["VALOR DUALCRED"] = "Valor calculado"  # Substitua com a lógica de cálculo real
        dados["%TRANS."] = "Valor calculado"  # Substitua com a lógica de cálculo real
        dados["%LIBERAD."] = "Valor calculado"  # Substitua com a lógica de cálculo real

        # Atualizar os dados armazenados
        stored_data.append(dados)
        
        # Retornar a mensagem de confirmação, os dados armazenados atualizados e os dados da tabela
        return f"Dados inseridos: {dados}", stored_data, stored_data
    return "", stored_data, stored_data

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
