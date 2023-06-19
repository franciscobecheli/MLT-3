import socket
import matplotlib.pyplot as plt

# Cria um objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço IP e a porta para o socket
host = '192.168.0.3'  # Substitua pelo IP do servidor
port = 12345  # A mesma porta usada pelo servidor

# Conecta-se ao servidor
client_socket.connect((host, port))

# Função para aplicar o princípio do algoritmo de codificação de linha inverso
def line_decoding(data):
    decoded_data = ''

    i = 0
    while i < len(data):
        decoded_data += data[i]
        i += 2  # Pula o bit zero

    return decoded_data

# Função para converter de binário para ASCII
def to_ascii(binary):
    ascii_data = ''

    for i in range(0, len(binary), 8):
        char = chr(int(binary[i:i+8], 2))
        ascii_data += char

    return ascii_data

# Função para aplicar o algoritmo de criptografia inverso
def mlt3_decode(data):
    decrypted_string = ""
    previous_bit = "1"

    for bit in data:
        if bit == previous_bit:
            decrypted_string += "0"
        else:
            decrypted_string += "1"
            previous_bit = bit

    return decrypted_string

# Função para criar o gráfico
def create_graph(data):
    tuple_data = tuple(char for char in data)
    x = list(range(len(tuple_data)))
    plt.step(x, tuple_data, where='post')
    plt.title('Sinal recebido')
    plt.xlabel('Tempo')
    plt.ylabel('Estado')
    plt.show()

# Função para receber os dados pelo socket
def receive_data():
    data = client_socket.recv(1024).decode()
    return data

# Função chamada ao receber os dados
def process_data(data):
    # Cria o gráfico

    create_graph(data)

    # Aplica o princípio do algoritmo de codificação de linha inverso
    decoded_mlt3_data = mlt3_decode(data)

    # Aplica o algoritmo de criptografia inverso
    ascii_data = to_ascii(decoded_mlt3_data)

    caser_decrypted_data = caeser_decrypt(ascii_data, -3)

    # Exibe a mensagem recebida
    print('Mensagem recebida:', ''.join(caser_decrypted_data))

def index_in_list(a_list, index):
    return index < len(a_list)

def caeser_decrypt(string, key):
    decrypted = []

    if string[0] != '0':
        decrypted.append(1)
    else:
        decrypted.append(0)

    for i in range(len(string)):
        if index_in_list(string, i + 1):
            if string[i] != string[i + 1]:
                decrypted.append(1)

            else:
                decrypted.append(0)

    return decrypted

# Recebe os dados
data_received = receive_data()

# Processa os dados
process_data(data_received)

# Fecha a conexão e o socket
client_socket.close()
