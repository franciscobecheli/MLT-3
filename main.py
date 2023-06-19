import tkinter as tk
import socket
import matplotlib.pyplot as plt

# Configurações de rede
HOST = '192.168.0.3'  # Endereço IP do outro computador
PORT = 12345       # Porta para a conexão

# Cria um objeto de socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço IP e a porta para o socket
host = '192.168.0.3'  # Substitua pelo IP do servidor
port = 12345  # Escolha uma porta disponível

# Associa o socket ao endereço IP e à porta
server_socket.bind((host, port))

# Coloca o socket em modo de escuta
server_socket.listen(1)

print('Aguardando conexão...')

# Aceita a conexão do cliente
client_socket, addr = server_socket.accept()

print('Conexão estabelecida de:', addr)

# Função para aplicar o algoritmo MLT-3
def mlt3_encode(data):
    encrypted_string = ""
    previous_bit = "1"

    for bit in data:
        if bit == "0":
            encrypted_string += previous_bit
        else:
            encrypted_string += "0" if previous_bit == "1" else "1"

        previous_bit = encrypted_string[-1]

    return encrypted_string

# Função para converter para binário
def to_binary(ascii):
    binary = ""
    for valor in ascii:
        binary += bin(valor)[2:].zfill(8)
    return binary

# Função para aplicar o princípio do algoritmo de codificação de linha
def line_encoding(data):
    encoded_data = []

    for bit in data:
        encoded_data.append(bit)
        encoded_data.append('0')  # Insere um bit zero após cada bit

    return ''.join(encoded_data)

# Função para enviar os dados pelo socket
def send_data(data):
    encoded = data.encode()
    client_socket.sendall(encoded)

# Função para criar o gráfico
def create_graph(data):
    tuple_data = tuple(char for char in data)
    x = list(range(len(tuple_data)))
    plt.step(x, tuple_data, where='post')
    plt.title('Sinal codificado')
    plt.xlabel('Tempo')
    plt.ylabel('Estado')
    plt.show()

# Função chamada ao clicar no botão
def send_text():
    text = entry.get()  # Obtém o texto digitado

    # Transforma em ascii estendido
    ascii_text = ascii_encode(text)

    # Converte para binário
    binary_data = to_binary(ascii_text)

    # Aplica o algoritmo de codificação de linha
    line_encoded_data = line_encoding(binary_data)

    # Aplica a criptografia MLT-3
    mlt3_data = mlt3_encode(line_encoded_data)

    # Cria o gráfico
    create_graph(mlt3_data)

    # Envia os dados para o outro computador
    send_data(mlt3_data)

def ascii_encode(string):
    ascii = []
    for char in string:
        ascii.append(ord(char))
    return ascii

# Configuração da interface gráfica usando tkinter
root = tk.Tk()
root.title('Comunicação de Dados')

label = tk.Label(root, text='Digite o texto:')
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text='Enviar', command=send_text)
button.pack()

root.mainloop()

# Fecha o socket
server_socket.close()
