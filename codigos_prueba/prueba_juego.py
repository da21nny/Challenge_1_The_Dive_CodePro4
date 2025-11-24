import random
import os
import time

# Dimensiones del laberinto
ANCHO = 15
ALTO = 10

# Símbolos
PARED = '█'
CAMINO = ' '
RATON = 'R'
GATO = 'G'
SALIDA = 'S'

def limpiar_pantalla():
    """Limpia la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def crear_laberinto():
    """Crea un laberinto aleatorio usando el algoritmo de división recursiva"""
    laberinto = [[PARED for _ in range(ANCHO)] for _ in range(ALTO)]
    
    # Crear caminos
    def hacer_camino(x1, y1, x2, y2):
        # Llenar el área con caminos
        for y in range(y1, y2):
            for x in range(x1, x2):
                laberinto[y][x] = CAMINO
        
        # Si el área es muy pequeña, no dividir más
        if x2 - x1 < 3 or y2 - y1 < 3:
            return
        
        # Decidir si dividir horizontal o verticalmente
        if x2 - x1 > y2 - y1:
            # División vertical
            if x2 - x1 > 4:
                pared_x = random.randrange(x1 + 2, x2 - 2, 2)
                for y in range(y1, y2):
                    laberinto[y][pared_x] = PARED
                # Hacer un hueco en la pared
                hueco = random.randrange(y1, y2)
                laberinto[hueco][pared_x] = CAMINO
                
                hacer_camino(x1, y1, pared_x, y2)
                hacer_camino(pared_x + 1, y1, x2, y2)
        else:
            # División horizontal
            if y2 - y1 > 4:
                pared_y = random.randrange(y1 + 2, y2 - 2, 2)
                for x in range(x1, x2):
                    laberinto[pared_y][x] = PARED
                # Hacer un hueco en la pared
                hueco = random.randrange(x1, x2)
                laberinto[pared_y][hueco] = CAMINO
                
                hacer_camino(x1, y1, x2, pared_y)
                hacer_camino(x1, pared_y + 1, x2, y2)
    
    # Iniciar la creación del laberinto
    hacer_camino(1, 1, ANCHO - 1, ALTO - 1)
    
    return laberinto

def encontrar_posicion_valida(laberinto, excepto=None):
    """Encuentra una posición válida en el laberinto"""
    if excepto is None:
        excepto = []
    
    while True:
        x = random.randint(1, ANCHO - 2)
        y = random.randint(1, ALTO - 2)
        if laberinto[y][x] == CAMINO and (x, y) not in excepto:
            return x, y

def mostrar_laberinto(laberinto, pos_raton, pos_gato, pos_salida, turnos):
    """Muestra el laberinto en la consola"""
    limpiar_pantalla()
    print("=" * (ANCHO + 2))
    print(f"  🐭 RATÓN vs GATO 🐱  |  Turno: {turnos}")
    print("=" * (ANCHO + 2))
    
    for y in range(ALTO):
        linea = ""
        for x in range(ANCHO):
            if (x, y) == pos_raton:
                linea += RATON
            elif (x, y) == pos_gato:
                linea += GATO
            elif (x, y) == pos_salida:
                linea += SALIDA
            else:
                linea += laberinto[y][x]
        print(linea)
    
    print("=" * (ANCHO + 2))
    print("Controles: W=Arriba, S=Abajo, A=Izquierda, D=Derecha")
    print("Objetivo: ¡Llega a la SALIDA (S) antes de que el gato te atrape!")

def obtener_vecinos(pos, laberinto):
    """Obtiene las posiciones vecinas válidas"""
    x, y = pos
    vecinos = []
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Arriba, Abajo, Izq, Der
    
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ANCHO and 0 <= ny < ALTO and laberinto[ny][nx] != PARED:
            vecinos.append((nx, ny))
    
    return vecinos

def mover_gato(pos_gato, pos_raton, laberinto):
    """El gato se mueve hacia el ratón usando un algoritmo simple"""
    vecinos = obtener_vecinos(pos_gato, laberinto)
    
    if not vecinos:
        return pos_gato
    
    # Calcular distancia Manhattan para cada vecino
    mejor_pos = pos_gato
    mejor_distancia = abs(pos_gato[0] - pos_raton[0]) + abs(pos_gato[1] - pos_raton[1])
    
    for vecino in vecinos:
        distancia = abs(vecino[0] - pos_raton[0]) + abs(vecino[1] - pos_raton[1])
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_pos = vecino
    
    return mejor_pos

def jugar():
    """Función principal del juego"""
    print("🎮 ¡BIENVENIDO AL LABERINTO!")
    print("\nGenerando laberinto...")
    time.sleep(1)
    
    # Crear laberinto y posiciones
    laberinto = crear_laberinto()
    pos_raton = encontrar_posicion_valida(laberinto)
    pos_gato = encontrar_posicion_valida(laberinto, [pos_raton])
    pos_salida = encontrar_posicion_valida(laberinto, [pos_raton, pos_gato])
    
    turnos = 0
    
    while True:
        mostrar_laberinto(laberinto, pos_raton, pos_gato, pos_salida, turnos)
        
        # Verificar victoria
        if pos_raton == pos_salida:
            print("\n🎉 ¡FELICIDADES! ¡El ratón escapó!")
            print(f"Turnos: {turnos}")
            break
        
        # Verificar derrota
        if pos_raton == pos_gato:
            print("\n😿 ¡Oh no! ¡El gato atrapó al ratón!")
            print(f"Turnos: {turnos}")
            break
        
        # Turno del ratón
        movimiento = input("\nTu movimiento (W/A/S/D): ").strip().upper()
        
        nueva_pos = pos_raton
        if movimiento == 'W':
            nueva_pos = (pos_raton[0], pos_raton[1] - 1)
        elif movimiento == 'S':
            nueva_pos = (pos_raton[0], pos_raton[1] + 1)
        elif movimiento == 'A':
            nueva_pos = (pos_raton[0] - 1, pos_raton[1])
        elif movimiento == 'D':
            nueva_pos = (pos_raton[0] + 1, pos_raton[1])
        else:
            print("Movimiento inválido. Usa W/A/S/D")
            time.sleep(1)
            continue
        
        # Verificar si el movimiento es válido
        if 0 <= nueva_pos[0] < ANCHO and 0 <= nueva_pos[1] < ALTO:
            if laberinto[nueva_pos[1]][nueva_pos[0]] != PARED:
                pos_raton = nueva_pos
                turnos += 1
                
                # Turno del gato
                pos_gato = mover_gato(pos_gato, pos_raton, laberinto)
            else:
                print("¡No puedes atravesar paredes!")
                time.sleep(1)
        else:
            print("¡Movimiento fuera del laberinto!")
            time.sleep(1)
    
    jugar_de_nuevo = input("\n¿Jugar de nuevo? (S/N): ").strip().upper()
    if jugar_de_nuevo == 'S':
        jugar()
    else:
        print("¡Gracias por jugar! 🐭🐱")

# Iniciar el juego
if __name__ == "__main__":
    jugar()