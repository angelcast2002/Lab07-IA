import numpy as np
import math
import random

# Constantes del juego
CANT_FILAS = 6
CANT_COLUMNAS = 7
JUGADOR = 0 
IA = 1
PIEZA_JUGADOR = 1
PIEZA_IA = 2

# Funciones del juego
def crearTablero():
    tablero = np.zeros((CANT_FILAS, CANT_COLUMNAS), dtype=int)
    return tablero

def soltarFicha(tablero, fila, columna, pieza):
    tablero[fila][columna] = pieza

def esValida(tablero, columna):
    return tablero[CANT_FILAS-1][columna] == 0

def obtenerSiguienteFilaVacia(tablero, columna):
    for r in range(CANT_FILAS):
        if tablero[r][columna] == 0:
            return r

def imprimirTablero(tablero):
    tableroInvertido = np.flip(tablero, 0)
    filas, columnas = tableroInvertido.shape

    tableroInvertido = tableroInvertido.astype(int)

    for i in range(filas):
        print("|", end="")
        for j in range(columnas):
            print(f"{tableroInvertido[i,j]:2}", end=" |")
        print()
    
    print("-" * (columnas * 4))

    print("|", end=" ")
    for j in range(columnas):
        print(f"{j}", end=" | ")

def movimientoGanador(tablero, pieza):
    for i in range(CANT_COLUMNAS - 3):
        for j in range(CANT_FILAS):
            if tablero[j][i] == pieza and tablero[j][i+1] == pieza and tablero[j][i+2] == pieza and tablero[j][i+3] == pieza:
                return True
    
    for i in range(CANT_COLUMNAS):
        for j in range(CANT_FILAS - 3):
            if tablero[j][i] == pieza and tablero[j+1][i] == pieza and tablero[j+2][i] == pieza and tablero[j+3][i] == pieza:
                return True
    
    for i in range(CANT_COLUMNAS - 3):
        for j in range(CANT_FILAS - 3):
            if tablero[j][i] == pieza and tablero[j+1][i+1] == pieza and tablero[j+2][i+2] == pieza and tablero[j+3][i+3] == pieza:
                return True
    
    for i in range(CANT_COLUMNAS - 3):
        for j in range(3, CANT_FILAS):
            if tablero[j][i] == pieza and tablero[j-1][i+1] == pieza and tablero[j-2][i+2] == pieza and tablero[j-3][i+3] == pieza:
                return True

    return False

def obtenerPosicionesValidas(tablero):
    posicionesValidas = []
    for i in range(CANT_COLUMNAS):
        if esValida(tablero, i):
            posicionesValidas.append(i)
    return posicionesValidas

class Agente_IA_QL:
    def __init__(self, alpha = 0.5, gamma = 0.9, epsilon = 0.1):
        self.Q = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
    def getQ(self, estado, accion):
        estado_inmutable = tuple(tuple(x) for x in estado)
        return self.Q.get((estado_inmutable, accion), 0.0)
    
    def seleccionarAccion(self, estado, accionesPosibles):
        if np.random.random() < self.epsilon:
            return random.choice(accionesPosibles)
        else:
            Qs = [self.getQ(estado, a) for a in accionesPosibles]
            return accionesPosibles[np.argmax(Qs)]
    
    def updateQ(self, estado, accion, recompensa, nuevoEstado, nuevaAccion):
        estado_inmutable = tuple(tuple(x) for x in estado)
        nuevoEstado_inmutable = tuple(tuple(x) for x in nuevoEstado)
        self.Q[(estado_inmutable, accion)] = self.getQ(estado, accion) + self.alpha * (recompensa + self.gamma * max([self.getQ(nuevoEstado_inmutable, a) for a in nuevaAccion]) - self.getQ(estado, accion))
 
    def jugar(self, estado):
        accionesPosibles = obtenerPosicionesValidas(estado)
        accion = self.seleccionarAccion(estado, accionesPosibles)
        siguienteEstado = np.copy(estado)  # Create a copy of the current state
        soltarFicha(siguienteEstado, obtenerSiguienteFilaVacia(siguienteEstado, accion), accion, PIEZA_IA)
        recompensa = 1 if movimientoGanador(siguienteEstado, 1) else -1 if len(obtenerPosicionesValidas(siguienteEstado)) == 0 else 0
        siguienteAccion = obtenerPosicionesValidas(siguienteEstado)
        self.updateQ(estado, accion, recompensa, siguienteEstado, siguienteAccion)
        return siguienteEstado

# creamos el tablero
tablero = crearTablero()

# Inicializamos las variables del juego
juegoTerminado = False
turno = random.randint(JUGADOR, IA)
jugadorHumano = True

agente01 = Agente_IA_QL()
agente02 = Agente_IA_QL()

# Imprimimos el tablero
imprimirTablero(tablero)
print("\n")

while not juegoTerminado:
    if turno == JUGADOR:
        # Turno del jugador
        if jugadorHumano:
            print("---> Turno del Jugador <---")
            columna = int(input("Elije una columna (0-6): "))
            
            if esValida(tablero, columna):
                fila = obtenerSiguienteFilaVacia(tablero, columna)
                soltarFicha(tablero, fila, columna, PIEZA_JUGADOR)
                if movimientoGanador(tablero, PIEZA_JUGADOR):
                    print("Ganaste!")
                    juegoTerminado = True
                    imprimirTablero(tablero)
                    break
            
            imprimirTablero(tablero)
            print("\n") 
            turno += 1
            turno = turno % 2

        else:
            print("---> Turno de la IA-01 <---")
            tablero = agente01.jugar(tablero)
            if movimientoGanador(tablero, PIEZA_JUGADOR):
                print("Ganó la IA - 01!")
                juegoTerminado = True
                imprimirTablero(tablero)
                break
                
            imprimirTablero(tablero)
            print("\n")
            turno += 1
            turno = turno % 2
                
    else:
        # Turno de la IA
        print("---> Turno de la IA <---")
        tablero = agente02.jugar(tablero)
        if movimientoGanador(tablero, PIEZA_IA):
            print("Ganó la IA - 02!")
            juegoTerminado = True
            imprimirTablero(tablero)
            break
            
        imprimirTablero(tablero)
        print("\n")
        turno += 1
        turno = turno % 2
            
    
    if len(obtenerPosicionesValidas(tablero)) == 0:
        print("Empate!")
        print("\n")
        imprimirTablero(tablero)
        juegoTerminado = True
