import socket
import threading
import os


sesion_aprobada = False
sesion_cliente = False
HOST = "10.24.8.155"
PORT = 6030
ADDR = (HOST, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"El servidor esta escuchando en {ADDR}")

clientes = {}

#FUNCIÓN PRINCIPAL DEL PROGRAMA
def comienzo_servidor():
    hilo_conexion = threading.Thread(target = conexion)
    hilo_conexion.start() 
    #Inicio de sesion del admin del servidor 
    global sesion_aprobada
    while sesion_aprobada == False:
        print("============================================================")
        iniciar_s = input("Bienvenido al servidor\npara usar el servidor necesitas iniciar sesión como administrador\n==================================================\n:>")
        

        if iniciar_s == "iniciar_sesion":
            
            while sesion_aprobada == False:
                print("==========================================")
                print("digita los datos a continuación: ")
                inicio_admin()
        else:
            
            print("ingrese un comando valido como iniciar_sesion")
    #menu de opciones del codigo
    if sesion_aprobada == True:
        menu_de_opciones()

def inicio_admin():

    global sesion_aprobada
    name_user =input('Ingresa el nombre de administrador: ')
    password_user =input('Ingresa la contraseña de administrador: ')

    datos_sesion = open(f'ldap_files/groups/credenciales_admin.txt','r',encoding= FORMAT)

    for line in datos_sesion:
            line = line.replace(" ","").replace("\n","")
            
            if line == f"{name_user}:{password_user}":
                sesion_aprobada = True
            
    if sesion_aprobada:
                
            print("Inicio de sesión aprobado!")
    else:
        print("Tu usuario o contraseña son incorrectos")
                

    datos_sesion.close()

#FUNCIONES QUE EJECUTAN ACCIONES QUE PUEDE HACER EL ADMINISTRADOR DEL SERVIDOR
def menu_de_opciones():
    global sesion_aprobada
    while True:
        print("==========================================")
        print("BIENVENIDO AL SERVIDOR, QUE QUIERES HACER?")
        print("==========================================")

        opcion = input()
        if opcion == "add_group":
            añadir_grupo()
        elif opcion == "add_user":
            añadir_usuario()
        elif opcion == "look_directory":
            ver_directorios()
        elif opcion == "log_out":
            sesion_aprobada = False
            print("¡Haz cerrado sesión!")
            exit()

def añadir_grupo():
    try: 
        name_group=input('ingresa el nombre del grupo/area: ')
        name_group = name_group.replace(" ","")
        fichero = open(f'ldap_files/groups/Group_{name_group}.txt','x',encoding='utf-8')
        fichero.close()
        print(f"El grupo: {name_group} se creo correctamente")
    except FileExistsError:
        print(f"No se puede crear el grupo {name_group} debido a que ya existe")

def añadir_usuario():

      
    name_group = input("A que grupo quieres ingresar el usuario: ")
    name_group = name_group.replace(" ","")
    name_user =input('ingresa el nombre de usuario: ')
    name_user = name_user.replace(" ","")
    contra_user =input('ingresa la contraseña: ')
    contra_user = contra_user.replace(" ","")
    try:
        existencia = open(f'ldap_files/groups/Group_{name_group}.txt','r',encoding='utf-8')
        
        for line in existencia:
            if line.startswith(f"{name_user}:"):
                print("El nombre de usuario ya existe")
                return
         
                
        fichero = open(f'ldap_files/groups/Group_{name_group}.txt','a+',encoding='utf-8')
        fichero.write(f"{name_user}:{contra_user}\n")
        fichero.close()
        print(f"Se agrego el nuevo usuario: {name_user} con exito al grupo: {name_group}")  
        existencia.close()
        
    except FileNotFoundError:
        print("El grupo que ingresaste no existe")

def ver_directorios():

    i = 1
    c =0 
    carpetas = ['ldap_files']
    print("Carpetas disponibles:")
    lista = os.listdir('ldap_files')
    for line in lista:
        print("\n"+str(i) +".-"+ line)
        i +=1
    while True:
        
        i = 1
        try:
                if c > 0:

                    volver_anterior = input('para volver a la carpeta anterior digita "back"\nsi no es así digita cualquier tecla: ')
                    if volver_anterior == "back":
                        if carpetas == ['ldap_files']:
                            print('No puedes volver mas atras de la carpeta actual "ldap_files"')
                            lista = os.listdir('ldap_files')
                            for line in lista:
                                print("\n"+str(i) +".-"+ line)
                                i+=1
                                c=0
                            continue
                        else:
                            carpetas.pop()
                            dato = "/".join(carpetas)
                            directorio = os.listdir(dato)
                            for line in directorio:
                                print("\n"+str(i)+".-"+line)
                                i+=1
                            continue
                carpeta = input('Ingresa la carpeta a que quieres revisar: ')
                carpetas.append(carpeta)
                dato = "/".join(carpetas)
                
                directorio = os.listdir(dato)
                for line in directorio:
                    print("\n"+str(i)+".-"+line)
                    i+=1
                print(dato)
                c +=1

        except FileNotFoundError:
            
            print(dato)
            print("No se encontro el directorio escrito\n")
            carpetas.pop()
            dato = "/".join(carpetas)
            directorio = os.listdir(dato)
            for line in directorio:
                print("\n"+str(i)+".-"+line)
                i+=1

#FUNCIONES QUE PUEDE EJECUTAR EL CLIENTE DE FORMA REMOTA
def solicitar_directorio(conn,group):
    conn.send(f'Este es el directorio correspondiente al grupo de "{group}":\n'.encode(FORMAT))
    conn.send("usa el comando abrir".encode(FORMAT))
    # conn.send("Carpetas y archivos disponibles:".encode(FORMAT))
    i = 1
    c =0 
    carpetas_disponibles = ["ldap_files/directorios"]
    carpetas_disponibles.append(group)
    carpetas_disponibles = "/".join(carpetas_disponibles)
    
    line_archivos_carpetas = []
    lista = os.listdir(f'{carpetas_disponibles}')
    for line in lista:
        line_archivos_carpetas.append(f"{i}.{line}")
        i+=1
    line_archivos_carpetas = "\n".join(line_archivos_carpetas)
    conn.send(f"{line_archivos_carpetas}".encode(FORMAT))
    
#FUNCIONES DE SOCKECTS
def inicio_sesion_cliente(conn,addr):

    global sesion_cliente
    
    aprobado = False

    while aprobado == False: 
       
        name_group = conn.recv(1024).decode(FORMAT)
        # print(name_group)
        name_user = conn.recv(1024).decode(FORMAT)
        # print(name_user)
        password_user = conn.recv(1024).decode(FORMAT)
        # print(password_user)
        try: 
            datos_sesion = open(f'ldap_files/groups/Group_{name_group}.txt','r',encoding= FORMAT)
            #Recorre el archivo entre los usuarios buscando el nombre y contraseña indicados
            for line in datos_sesion:
                line = line.replace(" ","").replace("\n","")
                if line == f"{name_user}:{password_user}":
                    aprobado = True
                
            if aprobado:
                    inicio_aprobado ="Inicio de sesion aprobado!" 
                    conn.send(inicio_aprobado.encode(FORMAT))
                    aprobado_cliente = "1"
                    sesion_cliente = True
                    conn.send(aprobado_cliente.encode(FORMAT))
                    clientes[f"{addr[0]}:{str(len(clientes)+1)}"]={"group":name_group} 
                    t2 = threading.Thread(target=recibir_comando,args=(conn,name_group))
                    t2.start()
                    break

            else:
                inicio_denegado ="Inicio de sesion denegado!\nTu usuario o contraseña son incorrectos"
                conn.send(inicio_denegado.encode(FORMAT))
                conn.send(str(0).encode(FORMAT))        
                

            datos_sesion.close()
        except FileNotFoundError:
        
            error_group = "El grupo que indicaste no existe"
            conn.send(error_group.encode(FORMAT))
            conn.send(str(0).encode(FORMAT))

def conexion():
     
    while True:
        conn,addr = server.accept()
        t1 = threading.Thread(target = inicio_sesion_cliente,args=(conn,addr))
        t1.start()
    
def recibir_comando(conn,group):
    try:
        while True:
            msg_client = conn.recv(1024).decode(FORMAT)
            if msg_client == "look":
                solicitar_directorio(conn,group)
            if msg_client == "":
                pass
    except:
        print("\nSe cerro el canal de ricibir comandos de la conexión: ", conn)
    
def enviar_data(conn):

        msg = input()
        conn.send(("server: "+msg).encode(FORMAT))

comienzo_servidor()