import socket
import matplotlib.pyplot as plt
import tkinter as tk

# Cria um objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço IP e a porta para o socket
host = '10.181.4.106'  # Substitua pelo IP do servidor
port = 12346  # A mesma porta usada pelo servidor

# Conecta-se ao servidor
client_socket.connect((host, port))

# Função para converter de binário para ASCII
def to_ascii(binary):
    ascii_data = ''
    string = ''.join(str(bit) for bit in binary)
    for i in range(0, len(string), 8):
        char = chr(int(string[i:i+8], 2))
        ascii_data += char

    return ascii_data

# Função para aplicar o algoritmo de criptografia inverso
def mlt3_decode(data):
    mensagem = []

    if data[0] != '0':
        mensagem.append(1)
    else:
        mensagem.append(0)

    for i in range(len(data)):
        if index_in_list(data, i + 1):
            if data[i] != data[i + 1]:
                mensagem.append(1)

            else:
                mensagem.append(0)

    return mensagem

# Função para criar o gráfico
def create_graph(data):
    tuple_data = tuple(char for char in data)
    x = list(range(len(tuple_data)))

    # Configura posições dos elementos no eixo y
    y_positions = {'-': 0, '0': 1, '+': 2}
    y = [y_positions[str(value)] for value in tuple_data]

    plt.step(x, y, where='post')
    plt.yticks([0, 1, 2], ['-', '0', '+'])
    plt.title('Sinal codificado')
    plt.xlabel('Tempo')
    plt.ylabel('Estado')
    plt.show(block=False)

# Função para receber os dados pelo socket
def receive_data():
    data = client_socket.recv(1024).decode()
    return data

def print_list(lista):
    formatted_list = ', '.join(str(item) for item in lista)  # Convert list to a formatted string with comma separator
    text_box.insert(tk.END, formatted_list)  # Insert the formatted list into the text field

# Função chamada ao receber os dados
def process_data(data):
    # Cria o gráfico

    create_graph(data)

    text_box.insert(tk.END, "Mensagem recebida: " + data + "\n\n")

    # Aplica o princípio do algoritmo de codificação de linha inverso
    decoded_mlt3_data = mlt3_decode(data)
    text_box.insert(tk.END, "Mensagem decodificada em binário: ")
    print_list(decoded_mlt3_data)
    text_box.insert(tk.END, "\n\n")

    # Aplica o algoritmo de criptografia inverso
    ascii_data = to_ascii(decoded_mlt3_data)
    text_box.insert(tk.END, "\n\nMensagem criptografada em ascii: " + ascii_data + "\n\n")

    caser_decrypted_data = caeser_decrypt(ascii_data, -3)
    text_box.insert(tk.END, "\n\nMensagem descriptografada: " + caser_decrypted_data + "\n\n")

    # Exibe a mensagem recebida
    print('Mensagem descriptografada:', ''.join(caser_decrypted_data))

    text_box.pack()

def index_in_list(a_list, index):
    return index < len(a_list)

def caeser_decrypt(string, key):
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

# Recebe os dados

root = tk.Tk()
root.title('Comunicação de Dados')
text_box = tk.Text(root)

data_received = receive_data()

# Processa os dados
process_data(data_received)

input()

# Fecha a conexão e o socket
client_socket.close()
