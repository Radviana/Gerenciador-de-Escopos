def obter_token_por_identificador(identificador, pilha_escopos):
    for escopo in pilha_escopos[::-1]:
        for token_atual in escopo:
            if token_atual[2] == identificador:
                return token_atual
    return None


def verificar_existencia_variavel(identificador, escopo):
    for token_atual in escopo:
        if token_atual[2] == identificador:
            return True
    return False


def atribuir_valor_ao_token(identificador, valor, pilha_escopos):
    for escopo in pilha_escopos[::-1]:
        for token_atual in escopo:
            if token_atual[2] == identificador:
                token_atual[3] = valor
                return None
