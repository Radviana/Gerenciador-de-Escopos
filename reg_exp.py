ER_ESPAÇO = r"\s+"

ER_NUMERO1 = r"[+-]?\d+(\.\d+)?"
ER_NUMERO2 = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" + ER_NUMERO1

ER_STRING1 = r'"([^"]*)"'
ER_STRING2 = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" + ER_STRING1

ER_VARIAVEL = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[a-zA-Z_][a-zA-Z0-9_]*"

ER_PRINT = r"PRINT\s+[a-zA-Z_][a-zA-Z0-9_]*"

PRINT_NUM_DECLARADO = f"NUMERO{ER_ESPAÇO}{ER_NUMERO2}"
PRINT_NUM_NÃO_DECLARADO = r"NUMERO\s+[a-zA-Z_][a-zA-Z0-9_]*"

PRINT_STRING_DECLARADA = f"CADEIA{ER_ESPAÇO}{ER_STRING2}"
PRINT_STRING_NÃO_DECLARADA = r"CADEIA\s+[a-zA-Z_][a-zA-Z0-9_]*"
