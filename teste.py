import pandas as pd

# # Carrega o arquivo Excel
# file_path = 'p.xlsx'
# df = pd.read_excel(file_path)

# # Obtém os nomes das colunas
# column_names = df.columns

# # Printa os nomes das colunas
# for column in column_names:
    #print(column)

# print(df.dtypes)
# print(df.head())
df = pd.read_excel('p.xlsx', engine="openpyxl", parse_dates=["DATA"])
df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")
print(df["DATA"].head())
print(df[df["DATA"].isna()])  # Mostra linhas com datas inválidas