import tkinter as tk
import socket
import matplotlib.pyplot as plt

# Configurações de rede
HOST = '192.168.0.3'  # Endereço IP do computador servidor
PORT = 12345       # Porta para a conexão

# Cria um objeto de socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço IP e à porta
server_socket.bind((HOST, PORT))

# Coloca o socket em modo de escuta
server_socket.listen(1)

print('Aguardando conexão...')

# Aceita a conexão do cliente
client_socket, addr = server_socket.accept()

print('Conexão estabelecida de:', addr)

# Função para aplicar o algoritmo MLT-3
def mlt3_encode(data):
    tuple_data = tuple(char for char in data)
    # Função pra codificar o sinal, de acordo com o algoritmo de código de linha MLT-3
    states = ['+', '0', '-', '0']
    sinal = []

    index = 3
    i = 0

    for i in range(0, len(tuple_data)):
        if tuple_data[i] == '1':
            index = (index + 1) % 4
        # print(states[index])
        sinal.append(states[index])

    sinal = ''.join(sinal)
    return sinal

# Função para converter ascii para binário
def to_binary(ascii):
    binary = ""
    for valor in ascii:
        binary += bin(valor)[2:].zfill(8)
    return binary


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
    plt.show(block=False)

# Função chamada ao clicar no botão
def send_text():
    text = entry.get()  # Obtém o texto digitado

    caeser_text = caesar_encrypt(text, 3)

    # Transforma em ascii estendido
    ascii_text = ascii_encode(caeser_text)

    # Converte para binário
    binary_data = to_binary(ascii_text)

    # Aplica a criptografia MLT-3
    mlt3_data = mlt3_encode(binary_data)

    # Cria o gráfico
    create_graph(mlt3_data)

    # Envia os dados para o outro computador
    send_data(mlt3_data)

def ascii_encode(string):
    ascii = []
    for char in string:
        ascii.append(ord(char))
    return ascii

def caesar_encrypt(string, key):
    result = ""
    for char in string:
        if char.isalpha():
            if char.islower():
                index = (ord(char) - ord('a') + key) % 26
                new_char = chr(ord('a') + index)
            else:
                index = (ord(char) - ord('A') + key) % 26
                new_char = chr(ord('A') + index)
            result += new_char
        else:
            result += char
    return result

# Configuração da interface gráfica usando tkinter
root = tk.Tk()
root.title('Comunicação de Dados')

label = tk.Label(root, text='Digite o texto:')
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text='Enviar', command=send_text)
button.pack()

root.mainloop()

# Fecha o socket
server_socket.close()
