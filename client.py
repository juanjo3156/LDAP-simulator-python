import socket
import threading



HOST = "localhost"
PORT = 6030
ADDR = (HOST,PORT)
FORMAT = "utf-8"
aprobado_servidor = False
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def mandar_mensaje():
    
    msg = input()
    client.send(("cliente: "+msg).encode(FORMAT))
        
        
            
def recibir_mensaje():
    
    inst = client.recv(1024).decode(FORMAT)
    print(inst)


def inicio_sesion():
    global aprobado_servidor
    while aprobado_servidor == False:
        name_group = input("Ingrese el nombre de su grupo o area sin espacios al final: ")
        client.send(name_group.encode(FORMAT))
        name_user =input('Ingresa tu nombre de usuario: ')
        client.send(name_user.encode(FORMAT))
        password_user =input('Ingresa tu contraseña: ')
        client.send(password_user.encode(FORMAT))
        

    
        aprobado = client.recv(1024).decode(FORMAT)
        print(aprobado)
        aprobado_servidor =client.recv(1024).decode(FORMAT)
        if aprobado_servidor == 'True':
            aprobado_servidor = True
    
        
    # if aprobado_servidor == True:
    #     consola()

 


# def conexion():

#     while True: 
#         t1 = threading.Thread(target=recibir_mensaje)
#         t1.start()
#         t2 = threading.Thread(target = mandar_mensaje)
#         t2.start()
        
def consola():
    connect = True
    while consola:
        pass

    
inicio_sesion()
