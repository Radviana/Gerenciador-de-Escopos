import re

class ScopeManager:
    def __init__(self):
        self.ER_ESPAÇO = r"\s+"
        self.ER_NUMERO1 = r"[+-]?\d+(\.\d+)?"
        self.ER_NUMERO2 = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" + self.ER_NUMERO1
        self.ER_STRING1 = r'"([^"]*)"'
        self.ER_STRING2 = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" + self.ER_STRING1
        self.ER_VARIAVEL = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[a-zA-Z_][a-zA-Z0-9_]*"
        self.ER_PRINT = r"PRINT\s+[a-zA-Z_][a-zA-Z0-9_]*"
        self.PRINT_NUM_DECLARADO = f"NUMERO{self.ER_ESPAÇO}{self.ER_NUMERO2}"
        self.PRINT_NUM_NÃO_DECLARADO = r"NUMERO\s+[a-zA-Z_][a-zA-Z0-9_]*"
        self.PRINT_STRING_DECLARADA = f"CADEIA{self.ER_ESPAÇO}{self.ER_STRING2}"
        self.PRINT_STRING_NÃO_DECLARADA = r"CADEIA\s+[a-zA-Z_][a-zA-Z0-9_]*"

        self.escopes = []
        self.list_tk_id_block = []

    def obter_token_por_identificador(self, identificador):
        for escopo in reversed(self.escopes):
            for token_atual in escopo:
                if token_atual[2] == identificador:
                    return token_atual
        return None

    def verificar_existencia_variavel(self, identificador, escopo):
        return any(token_atual[2] == identificador for token_atual in escopo)

    def atribuir_valor_ao_token(self, identificador, valor):
        for escopo in reversed(self.escopes):
            for token_atual in escopo:
                if token_atual[2] == identificador:
                    token_atual[3] = valor
                    return None

    def processar_linha(self, linha):
        linha = linha.strip().replace("\n", "")

        if "BLOCO" in linha:
            self.list_tk_id_block.append(linha.split(" ")[-1])
            self.escopes.append([])
            print(f'\n{"*INICIO " + self.list_tk_id_block[-1] + "*"}')
        elif self.list_tk_id_block and re.match(f"FIM{self.ER_ESPAÇO}{self.list_tk_id_block[-1]}", linha):
            if self.escopes:
                self.escopes.pop()
                print(f'\n{"*FIM " + self.list_tk_id_block[-1] + "*"}')
                self.list_tk_id_block.pop()
        elif re.match(self.PRINT_STRING_DECLARADA, linha) or re.match(self.PRINT_NUM_DECLARADO, linha):
            if "," in linha:
                tipo_var, *rest = linha.split(" ", 1)
                recebe_a, recebe_b = map(str.strip, rest[0].split(","))
                for recebe in [recebe_a, recebe_b]:
                    id_current, *value = map(str.strip, recebe.split("="))
                    if not self.verificar_existencia_variavel(id_current, self.escopes[-1]):
                        self.escopes[-1].append(["tk_identificador", tipo_var, id_current, value[0]])
            else:
                tipo_var, *rest = linha.split(" ", 1)
                id_unique, *value = map(str.strip, rest[0].split("="))
                if not self.verificar_existencia_variavel(id_unique, self.escopes[-1]):
                    self.escopes[-1].append(["tk_identificador", tipo_var, id_unique, value[0]])
        elif re.match(self.PRINT_STRING_NÃO_DECLARADA, linha) or re.match(self.PRINT_NUM_NÃO_DECLARADO, linha):
            tipo_var, id_unique = map(str.strip, linha.split(" "))
            if not self.verificar_existencia_variavel(id_unique, self.escopes[-1]):
                self.escopes[-1].append(["tk_identificador", tipo_var, id_unique, None])
        elif re.match(self.ER_VARIAVEL, linha):
            id_a, *id_b = map(str.strip, linha.split("="))
            token_b = self.obter_token_por_identificador(id_b[0])
            if token_b is None:
                print(f"{id_b[0]} não declarado")
                return
            token_a = self.obter_token_por_identificador(id_a)
            if token_a is None:
                self.escopes[-1].append(["tk_identificador", token_b[1], id_a, token_b[3]])
            else:
                if token_a[1] == token_b[1]:
                    self.atribuir_valor_ao_token(id_a, token_b[3])
                else:
                    print(f"{id_a} : Atribuição inválida")
        elif re.match(self.ER_NUMERO2, linha) or re.match(self.ER_STRING2, linha):
            id_a, value_a = map(str.strip, linha.split("="))
            token = self.obter_token_por_identificador(id_a)
            if token is None:
                if re.match(self.ER_NUMERO1, value_a):
                    self.escopes[-1].append(["tk_identificador", "NUMERO", id_a, value_a])
                elif re.match(self.ER_STRING1, value_a):
                    self.escopes[-1].append(["tk_identificador", "CADEIA", id_a, value_a])
                else:
                    print(f"Error: Valor ou cadeia inválida.")
            else:
                if token[1] == "NUMERO" and re.match(self.ER_NUMERO1, value_a):
                    self.atribuir_valor_ao_token(id_a, value_a)
                elif token[1] == "CADEIA" and re.match(self.ER_STRING1, value_a):
                    self.atribuir_valor_ao_token(id_a, value_a)
                else:
                    print(f"{id_a} : Atribuição inválida")
        elif re.match(self.ER_PRINT, linha):
            id_a = linha.split(" ")[-1]
            token = self.obter_token_por_identificador(id_a)
            if token is None:
                print(f"{id_a} não declarado")
            else:
                print(f"{id_a} = {token[3]} em {self.list_tk_id_block[-1]}")

    def processar_escopo(self, caminho_arquivo):
        with open(caminho_arquivo, "r") as txt:
            linhas = txt.readlines()

        for linha in linhas:
            self.processar_linha(linha)

if __name__ == "__main__":
    manager = ScopeManager()
    manager.processar_escopo("escopo.txt")
