import dash
from dash import dcc, html
from socorro import sanitize_column_name
import pandas as pd

# Carregar dados do Excel
file_path = 'p.xlsx'
df = pd.read_excel(file_path, engine="openpyxl")

def criar_inputs(df):
    inputs = []
    for col in df.columns:
        safe_col = sanitize_column_name(col)

        if col.lower() == "data":
            inputs.append(html.Div([
                html.Label(col),
                dcc.DatePickerSingle(id=f'input-{safe_col}', date=df[col].max())
            ]))

        elif "QTD DE PARCELAS" in col.upper():
            inputs.append(html.Div([
                html.Label(col),
                dcc.Dropdown(
                    id=f'input-{safe_col}',
                    options=[{"label": str(i), "value": str(i)} for i in range(1, 19)],
                    value="1", 
                    clearable=False
                )
            ]))

        else:
            inputs.append(html.Div([
                html.Label(col),
                dcc.Input(id=f'input-{safe_col}', type='text', value='')
            ]))

    return inputs
