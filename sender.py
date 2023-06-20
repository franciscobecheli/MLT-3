import tkinter as tk
import socket
import matplotlib.pyplot as plt

# Configurações de rede
HOST = '10.181.4.108'  # Endereço IP do computador servidor
PORT = 12346       # Porta para a conexão

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

    # Configura posições dos elementos no eixo y
    y_positions = {'-': 0, '0': 1, '+': 2}
    y = [y_positions[str(value)] for value in tuple_data]

    plt.step(x, y, where='post')
    plt.yticks([0, 1, 2], ['-', '0', '+'])
    plt.title('Sinal codificado')
    plt.xlabel('Tempo')
    plt.ylabel('Estado')
    plt.show(block=False)

# Função chamada ao clicar no botão
def send_text():
    text = entry.get()  # Obtém o texto digitado
    text_box.insert(tk.END, "Mensagem original:" + text + "\n\n")

    caesar_text = caesar_encrypt(text, 3, 1)
    text_box.insert(tk.END, "Mensagem criptografada:" + caesar_text + "\n\n")

    # Transforma em ascii estendido
    ascii_text = ascii_encode(caesar_text)
    text_box.insert(tk.END, "Mensagem criptografa em ascii:")
    print_list(ascii_text)

    # Converte para binário
    binary_data = to_binary(ascii_text)
    text_box.insert(tk.END, "\n\nAscii em binário:" + binary_data + "\n\n")

    # Aplica a criptografia MLT-3
    mlt3_data = mlt3_encode(binary_data)
    text_box.insert(tk.END, "Binário codificado com MLT-3:" + mlt3_data + "\n\n")

    text_box.pack()

    # Cria o gráfico
    create_graph(mlt3_data)

    # Envia os dados para o outro computador
    send_data(mlt3_data)

def ascii_encode(string):
    ascii = []
    for char in string:
        ascii.append(ord(char))
    return ascii

def caesar_encrypt(data, key, mode):
    alphabet = 'abcdefghijklmnopqrstuvwyzàáãâéêóôõíúçABCDEFGHIJKLMNOPQRSTUVWYZÀÁÃÂÉÊÓÕÍÚÇ'
    new_data = ''
    for c in data:
        index = alphabet.find(c)
        if index == -1:
            new_data += c
        else:
            new_index = index + key if mode == 1 else index - key
            new_index = new_index % len(alphabet)
            new_data += alphabet[new_index:new_index+1]
    return new_data

def print_list(lista):
    formatted_list = ', '.join(str(item) for item in lista)  # Convert list to a formatted string with comma separator
    text_box.insert(tk.END, formatted_list)  # Insert the formatted list into the text field

# Configuração da interface gráfica usando tkinter
root = tk.Tk()
root.title('Comunicação de Dados')

label = tk.Label(root, text='Digite o texto:')
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text='Enviar', command=send_text)
button.pack()

text_box = tk.Text(root)

root.mainloop()

# Fecha o socket
server_socket.close()
