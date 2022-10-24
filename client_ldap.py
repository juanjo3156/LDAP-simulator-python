import socket
import threading






def establecer_conexion():
    global host,port,conexion_server
    data_conexion = input("Escribe bind para iniciar la conexion: ")
    if data_conexion == "bind":
        host = input("Ingresa la ip del servidor: ")
        port = input("Ingresa el puerto del servidor: ")
    conexion_server = True

establecer_conexion()

aprobado_servidor = False


ADDR = (host,int(port))
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)


def mandar_comando():
    
    msg = input(">:")
    client.send((msg).encode(FORMAT))
    if msg == "unbind":
        client.close() 
           
        
def recibir_info():
    global conexion_server
 
    info = client.recv(1024).decode(FORMAT)
    print(info)

    # print("\n"+info)
        
        


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
    global conexion_server
    while aprobado_servidor == False:
        inicio_sesion()
    while True:
        hilo_de_envio = threading.Thread(target = mandar_comando)
        hilo_de_envio.start()
        hilo_de_recibo = threading.Thread(target = recibir_info)
        hilo_de_recibo.start()
        

consola()