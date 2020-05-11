# Programa en Python para acceder al EPI-EM de CISCO.
# Acceso a EPIC-EM Publico (User:devnetuser, Password:Cisco123!)
# Funciones:
#   get_ticket()            Solicita un ticket(token) en base al usuario/password definidos.
#   get_Network_Devices()   Obtiene e imprime en pantalla los Dispositivos de Red
#   get_Host()              Obtiene e imprime en pantalla los Dispositivos de Red
#   get_Interfaces()        Obtiene e imprime en pantalla los interfaces de los Dispositivos de Red
#   get_Switch_Vlan()       Obtiene e imprime en pantalla las Vlans de los Equipos de la familia Catalyst (Switches)
#  
#   Autor:Javi Cacho

from os import system
from sys import exit
import requests
import json
import urllib3
from tabulate import *
from pprint import pprint

# VARIABLES GLOBALES
global_ticket=None

requests.packages.urllib3.disable_warnings()

def menuPral(ticket):    
    print(f"""
    MENU DE OPCIONES PARA ACCEDER AL APIC-EM
    ----------------------------------------

    EL VALOR DEL TICKET ACTUAL ES: {ticket}
    
    1.- SOLICITAR TICKET DE ACCESO AL APIC-EM
    2.- OBTERNET LISTADO DE DISPOSITIVOS DE RED
    3.- OBTERNET LISTADO DE HOSTS
    4.- OBTENER LOS INTERFACES DE LOS EQUIPOS
    5.- OBTENER LAS VLANs DE LOS EQUIPOS DE LA FAMILIA 'CATALYST'

    r.- REFRESCAR OPCIONES

    q.- SALIR
    """
    )

def input_opcion_menu():
    OPCIONES=["1","2","3","4","5","r","q"]
    try:
        opcion_elegida=str(input("\nIntroduzca la opcion deseada: "))
        while opcion_elegida not in OPCIONES:
            print("ERROR !!! Opcion elegida incorrecta, intentelo de nuevo")
            opcion_elegida=str(input("\nIntroduzca la opcion deseada: "))             
    except:
        opcion_elegida="ERROR"
    finally:
        return opcion_elegida   

def get_ticket(url):
    get_ticket_url=url+"ticket"
    headers={
        "Content-type":"application/json"
    }
    Authentication={
        "password": "Cisco123!",
        "username": "devnetuser"
    }
    try:
        resp=requests.post(get_ticket_url, json.dumps(Authentication),headers=headers,verify=False)
        resp_json=resp.json()
        ticket=resp_json["response"]["serviceTicket"]
        #print("La peticion tiene el estado: ",resp.status_code)
    except:
        print(" Error no se pudo conseguir el ticket")
        ticket=None
        # print("El ticket del servicio es: ", resp_json["response"]["serviceTicket"])
    finally:
        return ticket

def get_Network_Devices(url, ticket):    
    get_Network_Devices_url=url+"network-device"    
    headers={
        "Content-type":"application/json",
        "X-Auth-Token":ticket,
    }
    resp=requests.get(get_Network_Devices_url,headers=headers,verify=False)     
    if resp.status_code == 200:
        resp_json=resp.json()
        Lista_equipos=[]
        i=0
        for equipo in resp_json["response"]:
            i+=1
            Disp=[
                i,                
                #equipo["family"],
                equipo["series"],
                equipo["hostname"],
                equipo["managementIpAddress"],
                equipo["macAddress"],
                equipo["softwareVersion"]
            ]
            Lista_equipos.append(Disp)
            table_header=["Indice","Modelo","Hostname","IP Gestion","MAC","Version SW"]
        print("\n",tabulate(Lista_equipos, table_header))
    else:
        print("EL CODIGO DE ERROR ES: ", resp.status_code)

def get_Host(url, ticket):    
    get_Network_Devices_url=url+"host"    
    headers={
        "Content-type":"application/json",
        "X-Auth-Token":ticket,
    }
    resp=requests.get(get_Network_Devices_url,headers=headers,verify=False)     
    if resp.status_code == 200:
        resp_json=resp.json()        
        Lista_equipos=[]
        i=0
        for equipo in resp_json["response"]:
            i+=1
            Disp=[
                i,
                equipo["hostType"],                
                equipo["hostMac"],
                equipo["hostIp"]
            ]
            Lista_equipos.append(Disp)
            table_header=["Indice","Tipo","MAC","Direccion IP"]
        print("\n",tabulate(Lista_equipos, table_header))
    else:
        print("EL CODIGO DE ERROR ES: ", resp.status_code)
    
def get_Interfaces(url, ticket):    
    get_Interface_url=url+"interface"    
    headers={
        "Content-type":"application/json",
        "X-Auth-Token":ticket,
    }
    resp=requests.get(get_Interface_url,headers=headers,verify=False)     
    if resp.status_code == 200:
        resp_json=resp.json()
        Lista_items=[]
        i=1
        device_id=None
        for item in resp_json["response"]:           
            if device_id != item["deviceId"]:
                device_id = item["deviceId"]                                               
                i+=1
                Disp=[
                    i,                                
                    item["series"],
                    item["pid"],
                    item["portName"],
                    item["ipv4Address"],
                    item["ipv4Mask"]
                ]
            else:
                Disp=[
                    "",                                
                    "",
                    "",
                    item["portName"],
                    item["ipv4Address"],
                    item["ipv4Mask"]
                ]
            Lista_items.append(Disp)
            table_header=["Indice","Familia","Equipo","Interface","Direccion IP","Mascara"]
        print("\n",tabulate(Lista_items, table_header))
    else:
        print("EL CODIGO DE ERROR ES: ", resp.status_code)

def get_Switch_Vlan(url, ticket):    
    get_Switch_Vlan_url=url+"network-device"
    headers={
        "Content-type":"application/json",
        "X-Auth-Token":ticket,
    }
    resp=requests.get(get_Switch_Vlan_url,headers=headers,verify=False)
    if resp.status_code == 200:
        resp_json=resp.json()
        Lista_ID_Equipos=[]        
        for equipo in resp_json["response"]:            
            Disp=[                   
                equipo["id"],
                equipo["series"],
                equipo["hostname"]                
            ]
            Lista_ID_Equipos.append(Disp)        
    else:
        print("EL CODIGO DE ERROR ES: ", resp.status_code)  

    for id_device in Lista_ID_Equipos:
        modelo=id_device[1]
        if modelo.find("Catalyst") != -1:
            #print(id_device)
            get_Switch_Vlan_url=url+"network-device/"+id_device[0]+"/vlan"
            resp=requests.get(get_Switch_Vlan_url,headers=headers,verify=False)            
            if resp.status_code == 200:
                resp_json=resp.json()
                #print(resp_json)
                Lista_Vlan_Switch=[]
                i=0
                for equipo in resp_json["response"]:
                    if i==0:
                        if len(equipo) > 2:
                            vlan=[                   
                                id_device[1],
                                id_device[2],
                                equipo["vlanNumber"],
                                equipo["ipAddress"],
                                equipo["prefix"]
                            ]
                        else:
                            vlan=[                   
                                id_device[1],
                                id_device[2],
                                equipo["vlanNumber"],
                                "<None>",
                                "<None>"
                            ]
                        i+=1
                    else:
                        if len(equipo) > 2:
                            vlan=[                   
                                "",
                                "",
                                equipo["vlanNumber"],
                                equipo["ipAddress"],
                                equipo["prefix"]
                            ]
                        else:
                            vlan=[                   
                                "",
                                "",
                                equipo["vlanNumber"],
                                "<None>",
                                "<None>"
                            ]
                    Lista_Vlan_Switch.append(vlan)
                    #print(Lista_Switches)
                    table_header=["Modelo", "Equipo","VLAN id","IP Vlan", "Prefijo de Red"]
                print("\n",tabulate(Lista_Vlan_Switch, table_header))
            else:
                print("EL CODIGO DE ERROR ES: ", resp.status_code)  

def Principal():
    url="https://sandboxapicem.cisco.com/api/v1/"
    #global var_hostIP, var_password, var_user, datos_equipo    
    global global_ticket
    opcion="r"
    while opcion != "q":
        opcion=input_opcion_menu()    
        if opcion.isdigit():        
            if opcion == "1":
                global_ticket=get_ticket(url)
                system('cls')
                menuPral(global_ticket)
            elif opcion in ("2","3","4","5") and global_ticket==None:
                print("\nERROR !!! DEBE SOLICITAR UN TICKET VALIDO (Opcion 1)")            
            elif opcion == "2":
                get_Network_Devices(url, global_ticket)
            elif opcion == "3":
                get_Host(url, global_ticket)
            elif opcion == "4":
                get_Interfaces(url, global_ticket)
            elif opcion == "5":
                get_Switch_Vlan(url, global_ticket)
        elif opcion == "r" or opcion == "R":
            system('cls')
            menuPral(global_ticket)
        else:        
            exit()

# MAIN()

system('cls')
menuPral(global_ticket)
Principal()



