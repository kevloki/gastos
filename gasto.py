import mysql.connector
from datetime import datetime

CONFIG_BD = {
    "host": "localhost",
    "user": "admin",
    "password": "admin",
    "database": "gastos"
}

def obter_entrada_usuario(mensagem, tipo_dado=float):
    while True:
        try:
            valor = tipo_dado(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, insira um valor válido.")

def obter_gastos_extra():
    gastos = []
    while True:
        nome = input("Digite o nome do gasto extra (ou pressione Enter para encerrar): ")
        if not nome:
            break
        valor = obter_entrada_usuario(f"Digite o valor do gasto '{nome}': ")
        gastos.append((nome, valor))
    return gastos

def formatar_data_para_bd(data):
    try:
        data_objeto = datetime.strptime(data, '%d-%m-%Y')
        return data_objeto.strftime('%Y-%m-%d')
    except ValueError:
        print("Data inválida. Certifique-se de que o dia e o mês sejam válidos.")
        return None

def inserir_gastos(cursor, gastos, data):
    query_insercao = "INSERT INTO gastos_mensais (nome_conta, valor, data_vencimento) VALUES (%s, %s, %s)"
    for nome, valor in gastos:
        cursor.execute(query_insercao, (nome, valor, data))

def main():
    try:
        conexao_bd = mysql.connector.connect(**CONFIG_BD)
        cursor_bd = conexao_bd.cursor()

        # Coletar os valores dos gastos regulares
        valor_luz = obter_entrada_usuario("Digite o valor da conta de luz: ")
        valor_passe = obter_entrada_usuario("Digite o valor do passe de transporte: ")
        valor_recarga_celular = obter_entrada_usuario("Digite o valor da recarga do celular: ")
        
        # Coletar a data de vencimento comum para gastos regulares
        data_vencimento_comum = input("Digite a data de vencimento para os gastos regulares (DD-MM-AAAA): ")
        data_vencimento_comum_bd = formatar_data_para_bd(data_vencimento_comum)

        # Coletar os valores dos gastos extras
        gastos_extra = obter_gastos_extra()

        total_a_pagar = (
            valor_luz + valor_passe + valor_recarga_celular +
            sum(gasto[1] for gasto in gastos_extra)
        )

        valor_recebido = obter_entrada_usuario("Digite o valor que você irá receber este mês: ")

        # Inserir gastos regulares com a mesma data de vencimento
        gastos_regulares = [("Conta de Luz", valor_luz), ("Passe de Transporte", valor_passe),
                            ("Recarga do Celular", valor_recarga_celular)]
        inserir_gastos(cursor_bd, gastos_regulares, data_vencimento_comum_bd)

        # Inserir gastos extras com datas de vencimento individuais
        for nome_gasto, valor_gasto in gastos_extra:
            data_vencimento = input(f"Digite a data de vencimento para o gasto '{nome_gasto}' (DD-MM-AAAA): ")
            data_vencimento_bd = formatar_data_para_bd(data_vencimento)
            if data_vencimento_bd is not None:
                inserir_gastos(cursor_bd, [(nome_gasto, valor_gasto)], data_vencimento_bd)
            else:
                print(f"O gasto '{nome_gasto}' não foi inserido devido a uma data inválida.")

        conexao_bd.commit()

        saldo_restante = valor_recebido - total_a_pagar

        print("\nResumo dos Gastos:")      
        for nome_gasto, valor_gasto in gastos_regulares:
            print(f"{nome_gasto}: R${valor_gasto:.2f} - Vencimento: {data_vencimento_comum}")
        for nome_gasto, valor_gasto in gastos_extra:
            print(f"{nome_gasto}: R${valor_gasto:.2f}")
        print("------------------------")
        print(f"Total a pagar: R${total_a_pagar:.2f}")
        print(f"Saldo restante: R${saldo_restante:.2f}")

    except mysql.connector.Error as erro:
        print("Erro:", erro)
    finally:
        if cursor_bd:
            cursor_bd.close()
        if conexao_bd and conexao_bd.is_connected():
            conexao_bd.close()

if __name__ == "__main__":
    main()






