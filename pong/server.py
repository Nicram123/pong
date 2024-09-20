import socket
import threading 
import pickle 

PORT = 4900
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 70
FORMAT = 'utf-8'

clients = []

DISCONNECT_MESSAGE = '!DISCONNECT!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def return_clients():
  return clients


def handle_client(conn, addr):
  connected = True
  while connected:
    try:
      msg_len = conn.recv(HEADER).decode(FORMAT)
      if msg_len:
        print('elo5')
        msg_len = int(msg_len)
        obj = b""
        while len(obj) < msg_len:
          packet = conn.recv(msg_len - len(obj))
          if not packet:
            break
          obj += packet
        board = pickle.loads(obj)
        if board == DISCONNECT_MESSAGE:
          connected = False
        else:
          print('elo4')
          send_to_other_clients(board, conn) # zmieniam
    except ConnectionResetError:
            connected = False
  conn.close() 
  

def send_to_other_clients(board, sender_conn):
  serialized_data = pickle.dumps(board) # zmieniam
  data_header = f'{len(serialized_data):<{HEADER}}'.encode(FORMAT)
  for client in clients:
    print('elo3')
    if client != sender_conn:
      print('elo2')
      try:
        client.send(data_header + serialized_data)
      except Exception as e:
        clients.remove(client)


def start():
  server.listen()
  while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target= handle_client, args=(conn, addr))
    thread.start()

start()
