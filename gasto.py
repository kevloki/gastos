def main():
    # Solicitar os dados de entrada
    valor_luz = float(input("Digite o valor da conta de luz: "))
    valor_wifi = float(input("Digite o valor da conta de wifi: "))
    valor_passe = float(input("Digite o valor do passe de transporte: "))
    valor_recarga_celular = float(input("Digite o valor da recarga do celular: "))

    # Inicializar as variáveis para o gasto extra
    valor_extra_total = 0
    valor_extra = 1

    # Continuar adicionando valores ao gasto extra até digitar 0
    while valor_extra != 0:
        valor_extra = float(input("Digite o valor adicional do gasto extra (digite 0 para encerrar): "))
        valor_extra_total += valor_extra

    # Calcular o total a ser pago
    total_a_pagar = valor_luz + valor_wifi + valor_passe + valor_recarga_celular + valor_extra_total

    # Solicitar o valor a ser recebido neste mês
    valor_recebido = float(input("Digite o valor que você irá receber este mês: "))

    # Calcular o saldo restante
    saldo_restante = valor_recebido - total_a_pagar

    # Exibir os resultados
    print("\nResumo dos gastos:")
    print(f"Conta de Luz: R${valor_luz:.2f}")
    print(f"Conta de Wifi: R${valor_wifi:.2f}")
    print(f"Passe de Transporte: R${valor_passe:.2f}")
    print(f"Recarga do Celular: R${valor_recarga_celular:.2f}")
    print(f"Gasto Extra Total: R${valor_extra_total:.2f}")
    print("------------------------")
    print(f"Total a pagar: R${total_a_pagar:.2f}")
    print(f"Saldo restante: R${saldo_restante:.2f}")


if __name__ == "__main__":
    main()
