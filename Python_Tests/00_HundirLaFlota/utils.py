import subprocess
import os
import time
import numpy as np

def limpiar_pantalla():
    if (os.name == "nt"):
        subprocess.run('cls')
    else:
        subprocess.run('clear')

def esperar_y_limpiar(segundos):
    time.sleep(segundos)
    limpiar_pantalla()

def pantalla_titulo():
    matriz_titulo = np.full((20,20)," ")
    matriz_titulo[0:1,0:] = "*"
    matriz_titulo[:,:1] = "*"
    matriz_titulo[-1] = "*"
    matriz_titulo[:,-1] = "*"
    print(matriz_titulo)

    for i in range(matriz_titulo.shape[0]):
        for j in range(matriz_titulo.shape[1]):
            print(matriz_titulo[i,j],end=" ")
        print("")

# pantalla_titulo()

def crear_tablero(numero = 10):
    tablero_jugador1 = Tablero(10)
    tablero_jugador2 = Tablero(10)

    tablero_jugador1.colocar_barco(0)
    tablero_jugador2.colocar_barco(0)

def colocar_barco(barco, tablero):
    pass

def disparar(casilla,tablero):
    letras = "ABCDEFGHIJ"
    indice_0 = letras.index(casilla[0])
    if (tablero[indice_0, casilla[1]] == "O"):
        tablero[indice_0, casilla[1]] = "X"
    else:
        tablero[indice_0, casilla[1]] = "A"

import numpy as np 

def crear_coordenadas(tamano):
    numeroX = np.random.randint(0,10)
    numeroY = np.random.randint(0,10)

    checking = True
    while checking == True:
        # print(numeroX,numeroY)
        if (numeroX > 8 or numeroY > 8):
            numeroX = np.random.randint(0,10)
            numeroY = np.random.randint(0,10)
        else:
            checking = False
            break

    return [numeroX, numeroY]


class Tablero():

    puntuacion_actual = 0
    casilla_inicial = "0"

    vidas_barcos = [4,3,3,2,2,2]
    
    
    barcos = np.full((6,2), "*")
    posiciones_barcos = []
    

    def __init__(self,tamano = 10):
        self.tamano = tamano
        self.matriz = np.full((tamano, tamano), "-")

    def colocar_barco(self, contador):

        # print("Contador =", contador)
        tablero = self.matriz.copy() # Aqui hacemos la copia del tablero para intentar colocar las casillas

        if (contador >= len(self.vidas_barcos)):
            return
        
        sentido = np.random.randint(0,4)
        
        # print("Sentido", sentido)
        numeros = crear_coordenadas(self.tamano)
        print("Coordenada incial:",numeros)
        # 0 = izquierda
        # 1 = derecha
        # 2 = arriba
        # 3 = abajo
        print("Eslora:", self.vidas_barcos[contador])

        generating = True
        while generating == True:
            print("Sentido:", sentido)
            longitud = self.vidas_barcos[contador]
            if (sentido < 2): # Horizontal
                fil_inicial = max(0, numeros[0] - 1)
                fil_final = min(self.tamano, numeros[0] + 2)

                if(sentido == 0): # Izquierda -- ABSOLUTE VICOTORY: 14-10-26 12:41 
                    
                    if((numeros[1] < longitud) or np.any(tablero[fil_inicial:fil_final,
                                                                max(0, (numeros[1] - (longitud) -1)):min(self.tamano,numeros[1] + 2)] != "-")):
                        numeros = crear_coordenadas(self.tamano)
                        continue
                    else:
                        tablero[numeros[0], max(0,numeros[1] - longitud):(numeros[1])] = "O"
                        # (fila:ini;fila_fin;columna:ini;columna:fin;eslora,sentido)
                        self.posiciones_barcos.append([[numeros[0],numeros[0]],[numeros[1],numeros[1] - longitud],self.vidas_barcos[contador], sentido]) 
                        generating = False

                else: # Derecha
                    if ((numeros[1] + longitud > self.tamano) or np.any(tablero[fil_inicial:fil_final,
                                                                     max(0, numeros[1] - 1):min(self.tamano, (numeros[1] +longitud) + 1)] != "-")):
                        numeros = crear_coordenadas(self.tamano)
                        continue
                    else:
                        tablero[numeros[0], numeros[1]: (numeros[1] + longitud)] = "O"
                        self.posiciones_barcos.append([[numeros[0],numeros[0]],[numeros[1],numeros[1] + longitud], self.vidas_barcos[contador], sentido])
                        generating = False

            else:
                col_inicial = max(0, numeros[1] - 1)
                col_final = min(self.tamano, numeros[1] + 2)

                if(sentido == 2): # Arriba
                   if ((numeros[0] < longitud) or np.any(tablero[max(0, (numeros[0] - longitud) - 1):min(self.tamano, numeros[0] + 2),
                                                                 col_inicial:col_final] != "-")):
                       numeros = crear_coordenadas(self.tamano)
                       continue
                   else:
                       tablero[(numeros[0] - longitud):(numeros[0]), numeros[1]] = "O"
                       self.posiciones_barcos.append([[numeros[0],numeros[0] - longitud], [numeros[1], numeros[1]],self.vidas_barcos[contador], sentido])
                       generating = False
                else:
                    if (numeros[0] + longitud > self.tamano) or np.any(tablero[max(0, numeros[0] - 1):min(self.tamano, numeros[0] + longitud) +2,
                                                                               col_inicial:col_final] != "-"):
                        numeros = crear_coordenadas(self.tamano)
                        continue
                    else:
                        tablero[numeros[0]:(numeros[0] + longitud), numeros[1]] = "O"
                        self.posiciones_barcos.append([[numeros[0], numeros[0]], [numeros[1], numeros[1] + longitud], self.vidas_barcos[contador], sentido])
                        generating = False

                
        
        print("Representacion: ")
        print(tablero)
        contador += 1
        self.matriz = tablero
        self.colocar_barco(contador)

    def comprobar_puntuacion(self):
        if self.puntuacion_actual < 15:
            return 1
        else:
            return 0
           
    def disparar(self,casilla):
        letras = "ABCDEFGHIJ"
        indice_0 = letras.index(casilla[0])
        if(self.matriz[indice_0, casilla[1]] == "O"):
            self.matriz[indice_0, casilla[1]] = "X"
        else:
            self.matriz[indice_0, casilla[1]] = "A"

        self.comprobar_puntuacion([indice_0, casilla[1]], 0)