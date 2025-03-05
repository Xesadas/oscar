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
    Input("salvar-btn", "n_clicks"),
    [State(f"input-{sanitize_column_name(col)}", "value") for col in df.columns if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]]
)
def salvar_dados(n_clicks, *valores):
    if n_clicks > 0:
        dados = {col: val for col, val in zip([col for col in df.columns if col not in ["MÁQUINA", "COMISSÃO ALESSANDRO", "VALOR DUALCRED", "%TRANS.", "%LIBERAD."]], valores)}
        
        # Calcular os valores das colunas automáticas
        dados["MÁQUINA"] = "PAGSEGURO"  # Substitua com a lógica de cálculo real
        dados["COMISSÃO ALESSANDRO"] = "Valor calculado"  # Substitua com a lógica de cálculo real
        dados["VALOR DUALCRED"] = "Valor calculado"  # Substitua com a lógica de cálculo real
        dados["%TRANS."] = "Valor calculado"  # Substitua com a lógica de cálculo real
        dados["%LIBERAD."] = "Valor calculado"  # Substitua com a lógica de cálculo real
        
        return f"Dados inseridos: {dados}"
    return ""

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)