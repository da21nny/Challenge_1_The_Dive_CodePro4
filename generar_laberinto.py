import random

def crear_laberinto(ancho, alto):
    # Asegurar dimensiones impares
    if ancho % 2 == 0: ancho += 1
    if alto % 2 == 0: alto += 1

    # Crear una matriz llena de paredes (1)
    lab = [[1 for _ in range(ancho)] for _ in range(alto)]

    def generar(x, y):
        lab[y][x] = 0  # Marcar como camino
        direcciones = [(0,2), (0,-2), (2,0), (-2,0)]
        random.shuffle(direcciones)  # Orden aleatorio

        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 1 <= nx < ancho-1 and 1 <= ny < alto-1:
                if lab[ny][nx] == 1:  # Si no ha sido visitado
                    # Romper la pared intermedia
                    lab[y + dy//2][x + dx//2] = 0
                    generar(nx, ny)

    # Punto de inicio aleatorio (impar)
    start_x, start_y = 1, 1
    generar(start_x, start_y)
    return lab

def mostrar_laberinto(lab):
    for fila in lab:
        print("".join("█" if celda == 1 else " " for celda in fila))

# Ejemplo de uso
lab = crear_laberinto(30, 15)
mostrar_laberinto(lab)
