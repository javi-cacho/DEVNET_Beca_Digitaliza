from os import system
from sys import exit
import requests
import xmltodict
from tabulate import *
from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from paramiko.ssh_exception import SSHException 
from netmiko.ssh_exception import  AuthenticationException
from ncclient import manager

# VARIABLES 
OPCIONES=["1","2","3","4","5","6","r","q"]
datos_ifaz={"TIPO INTERFACE":"", "NOMBRE INTERFACE":"","DIRECCION IPv4":"","MASCARA IPv4":""}
datos_equipo=False
var_hostIP=None
var_user=None
var_password=None

#DEFINICION DE FUNCIONES

def menuPral():    
    print(f"""
    MENU DE OPCIONES
    ----------------
    
    DATOS ACTUALES DEL EQUIPO:(Direccion IP: {var_hostIP}, Usuario: {var_user}, Password:{var_password})

    1.- INTRODUCIR LOS DATOS DEL EQUIPO 
    2.- OBTERNET LISTADO DE INTERFACES
    3.- CREAR UN INTERFACE
    4.- BORRAR UN INTERFACE
    5.- OBTENER LA TABLA DE RUTAS
    6.- YANG

    r.- REFRESCAR OPCIONES

    q.- SALIR
    """
    )

def de_acuerdo():
    respuesta="Z"         
    while respuesta != "s" and respuesta != "S" and respuesta != "n" and respuesta != "N":
        try: 
            respuesta=input("\n Esta de acuerdo con los datos introducidos (S/N) ")
        except:
            respuesta="Z"
    if respuesta == "s" or respuesta == "S":
        return True                
    else:
        return False   
                
def input_opcion_menu():
    try:
        opcion_elegida=str(input("\nIntroduzca la opcion deseada: "))
        while opcion_elegida not in OPCIONES:
            print("ERROR !!! Opcion elegida incorrecta, intentelo de nuevo")
            opcion_elegida=str(input("\nIntroduzca la opcion deseada: "))             
    except:
        opcion_elegida="ERROR"
    finally:
        return opcion_elegida   

def input_datos_equipo():
    global var_hostIP, var_password, var_user, datos_equipo
    input_ok=False    
    while not input_ok:     
        try:
            var_hostIP=str(input("\nIntroduzca la direccion IP del Router: "))
            var_user=str(input("Introduzca el usuario de acceso al router: "))
            var_password=str(input("Introduzca la password de acceso al router: "))                     
            input_ok=de_acuerdo()            
        except:
            input_ok=False
    datos_equipo=True
    system('cls')
    menuPral()

def show_interfaces():
    try:
        sshCli = ConnectHandler(
            device_type='cisco_ios',
            host=var_hostIP,
            port=22,
            username=var_user,
            password=var_password,
            )
        output=sshCli.send_command("show ip int brief")
        print("\n",format(output))
    except (NetMikoTimeoutException, AuthenticationException, SSHException):
        print("\nERROR !!! CON LOS DATOS INTRODUCIDOS NO SE HA PODIDO CONECTAR CON EL EQUIPO")
        return    
    try:
        m=manager.connect(
            host=var_hostIP,
            port=830,
            username=var_user,
            password=var_password,
            hostkey_verify=False
            )    
    except:
        print("\nERROR !!! CON LOS DATOS INTRODUCIDOS NO SE HA PODIDO CONECTAR CON EL EQUIPO")
        return
    interface_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>  
    </filter>
    """
    interface_replay = m.get(filter=interface_filter)
    interface_reply_dict = xmltodict.parse(interface_replay.xml)
    interface_list=[]
    for key  in interface_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
        interface=[
            key["name"],
            key["phys-address"],
            key["statistics"]["in-octets"],
            key["statistics"]["out-octets"]            
        ]
        interface_list.append(interface)
        table_header = ["Nombre","MAC","Input bytes","Output bytes"] 
    print("\n",tabulate(interface_list, table_header))

def input_crear_interface(crear_datos_interface):
    input_crear_interface=crear_datos_interface
    input_ok=False

    while not input_ok:
        try:
            tipo_ifaz=str(input("\nIntroduzca el tipo del interface: "))            
            nombre_ifaz=str(input("Introduzca el nombre del interface: "))
            direccion_ipv4=str(input("Introduzca la direccion IPv4: "))
            mascara_ipv4=str(input("Introduzca la mascara IPv4: "))
            input_ok=de_acuerdo()
        except:
            input_ok=False
    input_crear_interface["TIPO INTERFACE"]=tipo_ifaz
    input_crear_interface["NOMBRE INTERFACE"]=nombre_ifaz
    input_crear_interface["DIRECCION IPv4"]=direccion_ipv4
    input_crear_interface["MASCARA IPv4"]=mascara_ipv4    
    return input_crear_interface    
    
def crear_interface(crear_datos_interface):
    netconf_data = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <{crear_datos_interface["TIPO INTERFACE"]}>
                    <name>{crear_datos_interface["NOMBRE INTERFACE"]}</name>
                    <description>TEST1</description>
                    <ip>
                        <address>
                            <primary>
                                <address>{crear_datos_interface["DIRECCION IPv4"]}</address>
                                <mask>{crear_datos_interface["MASCARA IPv4"]}</mask>
                            </primary>
                        </address>
                    </ip>
                </{crear_datos_interface["TIPO INTERFACE"]}>
            </interface>
        </native>
    </config>
    """    
    try:
        m=manager.connect(
            host=var_hostIP,
            port=830,
            username=var_user,
            password=var_password,
            hostkey_verify=False
            )    
    except:
        print("\nERROR !!! CON LOS DATOS INTRODUCIDOS NO SE HA PODIDO CONECTAR CON EL EQUIPO")
        return
    try:
        netconf_reply = m.edit_config(target="running", config=netconf_data)
        print(f"\nInterface {crear_datos_interface['TIPO INTERFACE']}{crear_datos_interface['NOMBRE INTERFACE']} creado correctamente")
    except:
        print("\nERROR !!! NO SE HA PODIDO CREAR EL INTERFACE CON LOS DATOS INTRODUCIDOS")

def input_borrar_interface(borrar_datos_interface):
    input_borrar_interface=borrar_datos_interface
    input_ok=False
    while not input_ok:
        try:
            tipo_ifaz=str(input("\nIntroduzca el tipo del interface: "))            
            nombre_ifaz=str(input("Introduzca el nombre del interface: "))
            input_ok=de_acuerdo()
        except:
            input_ok=False
    input_borrar_interface["TIPO INTERFACE"]=tipo_ifaz
    input_borrar_interface["NOMBRE INTERFACE"]=nombre_ifaz    
    return input_borrar_interface

def borrar_interface(borrar_datos_interface):
        
    requests.packages.urllib3.disable_warnings()
    
    tipo_interface=borrar_datos_interface["TIPO INTERFACE"]
    numero_interface= borrar_datos_interface['NOMBRE INTERFACE']
    interface=tipo_interface+numero_interface    

    url = f"https://{var_hostIP}/restconf/data/ietf-interfaces:interfaces/interface={interface}"
    headers = {"Accept": "application/yang-data+json","Content-type":"application/yang-data+json"}
    
    respuesta= requests.request("DELETE", url, auth=(var_user, var_password), headers=headers, verify=False)       
    if(respuesta.status_code >= 200 and respuesta.status_code <= 299):
        print(f"\nInterface {interface} borrado correctamente")
    else:        
        print("\nERROR !!! NO SE HA PODIDO BORRAR EL INTERFACE CON LOS DATOS INTRODUCIDOS")

def get_routes():
    netconf_filter = """
    <filter>
        <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
    </filter>
    """
    try:
        m=manager.connect(
            host=var_hostIP,
            port=830,
            username=var_user,
            password=var_password,
            hostkey_verify=False
            )    
    except:
        print("\nERROR !!! CON LOS DATOS INTRODUCIDOS NO SE HA PODIDO CONECTAR CON EL EQUIPO")
        return  
    routes_replay = m.get(filter=netconf_filter)
    routes_reply_dict = xmltodict.parse(routes_replay.xml)
    route_list=[]
    i = 0
    for key in routes_reply_dict["rpc-reply"]["data"]["routing-state"]["routing-instance"]["ribs"]["rib"]["routes"]["route"]:
        i+=1
        route=[
            i,
            key["destination-prefix"],
            key["next-hop"]["outgoing-interface"],key["source-protocol"]]
        route_list.append(route)
        table_header = ["Indice","Number","Type","IP"]
    print("\n",tabulate(route_list, table_header))

def Principal():
    global var_hostIP, var_password, var_user, datos_equipo
    opcion="r"
    input_ok=False
    while opcion != "q":
        opcion=input_opcion_menu()    
        if opcion.isdigit():        
            if opcion == "1":
                input_datos_equipo()
            elif opcion in ("2","3","4","5","6") and not datos_equipo:
                print("\nERROR !!! DEBE INTRODUCIR LOS DATOS DEL EQUIPO (Opcion 1)")            
            elif opcion == "2":
                show_interfaces()
            elif opcion == "3":
                crear_datos_interface=datos_ifaz
                crear_datos_interface=input_crear_interface(crear_datos_interface)            
                crear_interface(crear_datos_interface)
            elif opcion == "4":
                borrar_datos_interface=datos_ifaz
                borrar_datos_interface=input_borrar_interface(borrar_datos_interface)            
                borrar_interface(borrar_datos_interface)
            elif opcion == "5":
                get_routes()
            elif opcion == "6":
                pass
        elif opcion == "r" or opcion == "R":
            menuPral()
        else:        
            exit()

# MAIN 

system('cls')
menuPral()
Principal()
