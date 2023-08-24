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

        valor_luz = obter_entrada_usuario("Digite o valor da conta de luz: ")
        data_vencimento_luz = input("Digite a data de vencimento para a conta de luz (DD-MM-AAAA): ")
        data_vencimento_luz_bd = formatar_data_para_bd(data_vencimento_luz)

        valor_wifi = obter_entrada_usuario("Digite o valor da conta de WiFi: ")
        data_vencimento_wifi = input("Digite a data de vencimento para a conta de WiFi (DD-MM-AAAA): ")
        data_vencimento_wifi_bd = formatar_data_para_bd(data_vencimento_wifi)

        valor_passe = obter_entrada_usuario("Digite o valor do passe de transporte: ")
        data_vencimento_passe = input("Digite a data de vencimento para o passe de transporte (DD-MM-AAAA): ")
        data_vencimento_passe_bd = formatar_data_para_bd(data_vencimento_passe)

        valor_recarga_celular = obter_entrada_usuario("Digite o valor da recarga do celular: ")
        data_vencimento_celular = input("Digite a data de vencimento para a recarga do celular (DD-MM-AAAA): ")
        data_vencimento_celular_bd = formatar_data_para_bd(data_vencimento_celular)

        gastos_extra = obter_gastos_extra()

        total_a_pagar = (
            valor_luz + valor_wifi + valor_passe + valor_recarga_celular +
            sum(gasto[1] for gasto in gastos_extra)
        )

        valor_recebido = obter_entrada_usuario("Digite o valor que você irá receber este mês: ")

        inserir_gastos(cursor_bd, [("Conta de Luz", valor_luz)], data_vencimento_luz_bd)
        inserir_gastos(cursor_bd, [("Conta de WiFi", valor_wifi)], data_vencimento_wifi_bd)
        inserir_gastos(cursor_bd, [("Passe de Transporte", valor_passe)], data_vencimento_passe_bd)
        inserir_gastos(cursor_bd, [("Recarga do Celular", valor_recarga_celular)], data_vencimento_celular_bd)

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
        print(f"Conta de Luz: R${valor_luz:.2f} - Vencimento: {data_vencimento_luz}")
        print(f"Conta de Wifi: R${valor_wifi:.2f} - Vencimento: {data_vencimento_wifi}")
        print(f"Passe de Transporte: R${valor_passe:.2f} - Vencimento: {data_vencimento_passe}")
        print(f"Recarga do Celular: R${valor_recarga_celular:.2f} - Vencimento: {data_vencimento_celular}")
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





