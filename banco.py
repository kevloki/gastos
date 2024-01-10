import mysql.connector

# Configuração da conexão com o banco de dados
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="gastos"
)

db_cursor = db_connection.cursor()

# Comando SQL para criar a tabela
create_table_query = """
CREATE TABLE IF NOT EXISTS gastos_mensais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_conta VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data_vencimento DATE
)
"""

db_cursor.execute(create_table_query)

# Certifique-se de fechar a conexão e o cursor após o uso
db_cursor.close()
db_connection.close()
