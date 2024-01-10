import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

CONFIG_BD = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "gastos"
}

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

def calcular_gastos():
    valor_luz = float(entrada_luz.get())
    valor_passe = float(entrada_passe.get())
    valor_recarga_celular = float(entrada_recarga.get())
    data_vencimento_comum = entrada_data_vencimento.get()
    valor_recebido = float(entrada_valor_recebido.get())

    gastos_extra = []
    for nome_gasto, valor_gasto in gastos_extra_entries:
        valor_gasto = float(valor_gasto.get())
        gastos_extra.append((nome_gasto, valor_gasto))

    try:
        conexao_bd = mysql.connector.connect(**CONFIG_BD)
        cursor_bd = conexao_bd.cursor()

        data_vencimento_comum_bd = formatar_data_para_bd(data_vencimento_comum)

        total_a_pagar = (
            valor_luz + valor_passe + valor_recarga_celular +
            sum(gasto[1] for gasto in gastos_extra)
        )

        # Inserir gastos regulares com a mesma data de vencimento
        gastos_regulares = [("Conta de Luz", valor_luz), ("Passe de Transporte", valor_passe),
                            ("Recarga do Celular", valor_recarga_celular)]
        inserir_gastos(cursor_bd, gastos_regulares, data_vencimento_comum_bd)

        # Inserir gastos extras com datas de vencimento individuais
        for nome_gasto, valor_gasto in gastos_extra:
            data_vencimento = gastos_extra_datas[nome_gasto].get()
            data_vencimento_bd = formatar_data_para_bd(data_vencimento)
            if data_vencimento_bd is not None:
                inserir_gastos(cursor_bd, [(nome_gasto, valor_gasto)], data_vencimento_bd)
            else:
                print(f"O gasto '{nome_gasto}' não foi inserido devido a uma data inválida.")

        conexao_bd.commit()

        saldo_restante = valor_recebido - total_a_pagar

        # Exibir resumo na interface gráfica
        resumo_texto = f"\nResumo dos Gastos:\n"
        for nome_gasto, valor_gasto in gastos_regulares:
            resumo_texto += f"{nome_gasto}: R${valor_gasto:.2f} - Vencimento: {data_vencimento_comum}\n"
        for nome_gasto, valor_gasto in gastos_extra:
            resumo_texto += f"{nome_gasto}: R${valor_gasto:.2f}\n"
        resumo_texto += "------------------------\n"
        resumo_texto += f"Total a pagar: R${total_a_pagar:.2f}\n"
        resumo_texto += f"Saldo restante: R${saldo_restante:.2f}\n"

        resultado_label.config(text=resumo_texto)

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")
    finally:
        if cursor_bd:
            cursor_bd.close()
        if conexao_bd and conexao_bd.is_connected():
            conexao_bd.close()

# Criação da interface gráfica
tela = tk.Tk()
tela.title("Calculadora de Gastos")

# Elementos para entrada de dados
tk.Label(tela, text="Valor da conta de luz:").pack()
entrada_luz = tk.Entry(tela)
entrada_luz.pack()

tk.Label(tela, text="Valor do passe de transporte:").pack()
entrada_passe = tk.Entry(tela)
entrada_passe.pack()

tk.Label(tela, text="Valor da recarga do celular:").pack()
entrada_recarga = tk.Entry(tela)
entrada_recarga.pack()

tk.Label(tela, text="Data de vencimento comum (DD-MM-AAAA):").pack()
entrada_data_vencimento = tk.Entry(tela)
entrada_data_vencimento.pack()

tk.Label(tela, text="Valor que você irá receber este mês:").pack()
entrada_valor_recebido = tk.Entry(tela)
entrada_valor_recebido.pack()

# Adicionando gastos extras
gastos_extra_entries = []
gastos_extra_datas = {}
gasto_extra_label = tk.Label(tela, text="Gastos Extras:")
gasto_extra_label.pack()

while True:
    nome_gasto = tk.simpledialog.askstring("Gasto Extra", "Digite o nome do gasto extra (ou cancel para encerrar):")
    if not nome_gasto:
        break

    gastos_extra_entries.append((nome_gasto, tk.Entry(tela)))
    gastos_extra_entries[-1][1].pack()

    tk.Label(tela, text=f"Data de vencimento para '{nome_gasto}' (DD-MM-AAAA):").pack()
    gastos_extra_datas[nome_gasto] = tk.Entry(tela)
    gastos_extra_datas[nome_gasto].pack()

# Botão para calcular os gastos
tk.Button(tela, text="Calcular Gastos", command=calcular_gastos).pack()

# Rótulo para mostrar o resumo
resultado_label = tk.Label(tela, text="", justify="left")
resultado_label.pack()

# Inicie a interface gráfica
tela.mainloop()
