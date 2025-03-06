# utils.py

import re

def sanitize_column_name(col_name):
    """Função para normalizar os nomes das colunas removendo caracteres inválidos"""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', col_name)
