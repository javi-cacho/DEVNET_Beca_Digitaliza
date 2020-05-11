# Programa en Python (CALCULADORA v1.0)
# Modelo POO
# Funciones incluidas
#       Sumar
#       Restar
#       Multiplicar
#       Dicidir
#       Potencias
#       Raiz Cuadrada
#
#   Autor:Javi Cacho

from math import sqrt
from os import system

class calculadora():
    def __init__(self):
        self.POWEROFF=True
        self.opcion="q"
        self.OPCIONES={"1":"Sumar","2":"Restar","3":"Multiplicar","4":"Dividir","5":"Potencias","6":"Raiz Cuadrada","r":"REFRESCAR OPCIONES","q":"EXIT"}
        system("cls") 
        print("        CALCULADORA ENCENDIDA\n")
        print("        Proyecto Calculadora v1.0")
    
    def power_off(self):
        print("\n        CALCULADORA APAGADA\n")        
        
    def display_opciones(self):               
        print("\nOperaciones disponibles")
        for i in self.OPCIONES.keys():            
            if not i.isdigit():
                print("")
            print(f"{i}.- {self.OPCIONES[i]}")            
        
    def input_opcion(self):
        try:
            opcion_elegida=str(input("\nIntruduzca la opcion deseada: "))
            while opcion_elegida not in calc1.OPCIONES.keys():
                print("Opcion elegida incorrecta, intentelo de nuevo")
                opcion_elegida=str(input("intruduzca la opcion deseada: "))             
        except:
           opcion_elegida="ERROR"
        finally:
            return opcion_elegida        
    
    def input_data(self, operacion, index):
        dato_valido=False
        while not dato_valido:
            dato_valido=True            
            try:
                if operacion == "1":
                    if index== "1":
                        print("Introduzca los numeros a sumar \n")
                    numero=float(input(f"Intruduzca el numero {index}: "))        
                elif operacion == "2":
                    if index== "1":
                        print("Introduzca los numeros a restar \n")
                    numero=float(input(f"Intruduzca el numero {index}: "))                
                elif operacion == "3":
                    if index== "1":
                        numero=float(input("Introduzca el multiplicando: "))
                    else:
                        numero=float(input("Introduzca el multiplicador: "))        
                elif operacion == "4":
                    if index== "1":
                        numero=float(input("Introduzca el dividendo: "))
                    else:                
                        numero=float(input("Introduzca el divisoror: "))
                elif operacion == "5":
                    if index== "1":
                        numero=float(input("Introduzca el numero: "))
                    else:                
                        numero=float(input("Introduzca la potencia: "))
                elif operacion == "6":
                    numero=float(input("Introduzca el numero: "))
            except:
                dato_valido=False
        return numero

    def suma(self,num1, num2):
        result_suma=num1 + num2
        return result_suma

    def resta(self,num1, num2):
        result_resta=num1 - num2
        return result_resta

    def multiplicacion(self,num1, num2):
        result_multiplicacion=num1*num2
        return result_multiplicacion

    def division(self,num1, num2):
        try:
            result_division=num1 / num2            
        except:
            result_division="ERROR DIVISION POR CERO"
        finally:    
            return result_division

    def potencia(self,num1, num2):
        try:
            result_potencia=num1**num2
            return result_potencia
        except OverflowError:
            print("\nRESULTADO MUY GRANDE")
            return None
        except:
            print("RESULTADO ERRONEO")
            return None

    def raiz_cuadrada(self,num1):
        result_raiz_cuadrada=sqrt(num1)
        return result_raiz_cuadrada

    def run_operacion(self,operacion, num1, num2=None):
        if operacion == "1":
            result=self.suma(num1,num2)
            return result
        elif operacion == "2":
            result=self.resta(num1,num2)
            return result
        elif operacion == "3":
            result=self.multiplicacion(num1,num2)
            return result
        elif operacion == "4":
            result=self.division(num1,num2)            
            return result
        elif operacion == "5":
            result=self.potencia(num1,num2)            
            return result
        elif operacion == "6":
            result=self.raiz_cuadrada(num1)            
            return result

# PROGRAM PRINCIPAL

calc1=calculadora()
calc1.display_opciones()
calc1.opcion="r"
while calc1.opcion != "q":
    calc1.opcion=calc1.input_opcion()
    if calc1.opcion.isdigit():
        if not calc1.opcion=="6":
            operando1=calc1.input_data(calc1.opcion, "1")
            operando2=calc1.input_data(calc1.opcion, "2")
            resultado=calc1.run_operacion(calc1.opcion,operando1,operando2)
        else:
            operando1=calc1.input_data(calc1.opcion, "1")
            resultado=calc1.run_operacion(calc1.opcion,operando1)
        if resultado != None:
            print(f"\nEL RESULTADO ES: {resultado}")        
    elif calc1.opcion == "r" or calc1.opcion == "R":
        system("cls")
        calc1.display_opciones()
    else:
        calc1.power_off()
        break










