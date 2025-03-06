import pandas as pd

# Carrega o arquivo Excel
file_path = 'p.xlsx'
df = pd.read_excel(file_path)

# Obtém os nomes das colunas
column_names = df.columns

# Printa os nomes das colunas
for column in column_names:
    print(column)