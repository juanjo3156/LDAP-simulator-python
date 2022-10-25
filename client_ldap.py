import socket
import threading

#Establece la conexión con el servidor, pidiendole al usuario la ip y el puerto
def establecer_conexion():
    global host,port,conexion_server
    data_conexion = input("Escribe bind para iniciar la conexion: ")
    if data_conexion == "bind":
        host = input("Ingresa la ip del servidor: ")
        port = input("Ingresa el puerto del servidor: ")
    conexion_server = True

#se manda a llamar la función del server
establecer_conexion()

#Variable que identifica si el usuario inicio sesion correctamente o no,
#se utiliza posteriormente para la coomprobación de que los datos del
#usuario son correctos y con esto dejar de preguntarlos y mandarlos 
#al servidor.
aprobado_servidor = False

# Variable para identificar que el usuario esta conectado
usuario_conectado = False

ADDR = (host,int(port))
#Formato de envio y reccepción de los bits 
FORMAT = "utf-8"

#creación del socket 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

#emite un input para que el usuario ingrese comandos y los envia 
#con un client.send al servidor
def mandar_comando():
    global usuario_conectado

    try:
        while usuario_conectado:
            msg = input(">:")
            client.send((msg).encode(FORMAT))
            if msg == "unbind":
                usuario_conectado = False
                client.close() 
    except:
        print("Se cerro el hilo para el envio de comandos")
           
#emite una escucha para los datos e información que nos quiera dar
#el servidor      
def recibir_info():
    try:
        while usuario_conectado:
            info = client.recv(1024).decode(FORMAT)
            print(info)
    except:
        print("Se cerro el hilo para el recibo de info")

#Permite inicio de sesion al servidor desde el cliente.
def inicio_sesion():
    
    global aprobado_servidor, usuario_conectado
    name_group = input("Ingrese el nombre de grupo o area: ")
    #remplazamos los espacios vacios para evitar errores de busqueda
    name_group = name_group.replace(" ","")
    client.send(name_group.encode(FORMAT))

    name_user =input('Ingresa tu nombre de usuario: ')
    name_user = name_user.replace(" ","")
    client.send(name_user.encode(FORMAT))

    password_user =input('Ingresa tu contraseña: ')
    password_user = password_user.replace(" ","")
    client.send(password_user.encode(FORMAT))

    aprobado = client.recv(1024).decode(FORMAT)
    print(aprobado)
    aprobado_servidor =client.recv(1024).decode(FORMAT)
    print(aprobado_servidor)

    aprobado_servidor = bool(int(aprobado_servidor))
    usuario_conectado = aprobado_servidor
    print(aprobado_servidor)

#Función principal del cliente que permite la ejecución de las 
#funciones principales. La función de inicio de sesión se repite
#hasta que el usuario haya ingresado sus datos correctamente
def consola():

    while aprobado_servidor == False:
        inicio_sesion()
        #posteriormente se crean e inicializan 2 hilos en los que se iniciara ma funcion 
        #mandar_comando y recibir_info respectivamente

    if usuario_conectado:
        #Estos hilos permiten que el usuario reciba y mande datos 
        #de forma concurrente.
        hilo_de_envio = threading.Thread(target = mandar_comando)
        hilo_de_envio.start()
        hilo_de_recibo = threading.Thread(target = recibir_info)
        hilo_de_recibo.start()

        
#Se llama a la fución principal del servidor
consola()