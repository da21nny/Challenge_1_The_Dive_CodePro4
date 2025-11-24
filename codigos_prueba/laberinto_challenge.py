import random

def crear_laberinto(ancho, alto):
    if ancho % 2 == 0: ancho += 1
    if alto % 2 == 0: alto += 1

    laberinto = [[1 for _ in range(ancho)] for _ in range(alto)]

    def generar(x,y):
        laberinto[y][x] = 0
        direccion = [(0,2), (0,-2), (2,0), (-2,0)]
        random.shuffle(direccion)

        for dx, dy in direccion:
            nx = x + dx
            ny = y + dy
            if 1 <= nx < ancho-1 and 1 <= ny < alto-1:
                if laberinto[ny][nx] == 1:
                    laberinto[y + dy//2][x + dx//2] = 0
                    generar(nx,ny)

    inicio_x, inicio_y = 1, 1
    generar(inicio_x, inicio_y)


    for _ in range(max(ancho, alto) // 6):
        x = random.randrange(1, ancho-1, 2)
        y = random.randrange(1, alto-1, 2)
        if laberinto[y][x] == 1:
            laberinto[y][x] = 0
            # Conectar a un vecino existente
            vecinos = [(0,2), (0,-2), (2,0), (-2,0)]
            random.shuffle(vecinos)
            for dx, dy in vecinos:
                nx, ny = x + 1 * dx, y + 1 * dy
                if 1 <= nx < ancho-1 and 1 <= ny < alto-1:
                    if laberinto[ny][nx] == 0:
                        laberinto[y + dy//2][x + dx//2] = 0
                        break

    return laberinto


def mostrar_laberinto(laberinto):
    for fila in laberinto:
        print("".join("█" if celda == 1 else " " for celda in fila))

#laberinto = crear_laberinto(30, 15)
#mostrar_laberinto(laberinto)