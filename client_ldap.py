import socket
import threading

aprobado_servidor = False

HOST = "localhost"
PORT = 6030
ADDR = (HOST,PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def mandar_comando():
    
    msg = input(">:")
    client.send((msg).encode(FORMAT))
        
def recibir_info():
    
    info = client.recv(1024).decode(FORMAT)
    
    print("\n"+info)

def inicio_sesion():

    global aprobado_servidor
    name_group = input("Ingrese el nombre de su grupo o area sin espacios al final: ")
    client.send(name_group.encode(FORMAT))
    name_user =input('Ingresa tu nombre de usuario: ')
    client.send(name_user.encode(FORMAT))
    password_user =input('Ingresa tu contraseña: ')
    client.send(password_user.encode(FORMAT))
        

    
    aprobado = client.recv(1024).decode(FORMAT)
    print(aprobado)
    aprobado_servidor =client.recv(1024).decode(FORMAT)
    print(aprobado_servidor)

    aprobado_servidor = bool(int(aprobado_servidor))
    print(aprobado_servidor)
     
def consola():
    while aprobado_servidor == False:
        inicio_sesion()
    while True:
        hilo_de_envio = threading.Thread(target = mandar_comando)
        hilo_de_envio.start()
        hilo_de_recibo = threading.Thread(target = recibir_info)
        hilo_de_recibo.start()

consola()