import math
import random

class crear_laberinto:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.laberinto = self.generar_laberinto()

    def generar_laberinto(self):
        # Asegurar dimensiones impares
        if self.ancho % 2 == 0: self.ancho += 1
        if self.alto % 2 == 0: self.alto += 1

        # Crear una matriz llena de paredes (1)
        lab = [[1 for _ in range(self.ancho)] for _ in range(self.alto)]

        def generar(x, y):
            lab[y][x] = 0  # Marcar como camino
            direcciones = [(0,2), (0,-2), (2,0), (-2,0)]
            random.shuffle(direcciones)  # Orden aleatorio

            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.ancho-1 and 1 <= ny < self.alto-1:
                    if lab[ny][nx] == 1:  # Si no ha sido visitado
                        # Romper la pared intermedia
                        lab[y + dy//2][x + dx//2] = 0
                        generar(nx, ny)

        # Punto de inicio aleatorio (impar)
        generar(1, 1)
        return lab

    def mostrar_laberinto(self):
        for fila in self.laberinto:
            print("".join("█" if celda == 1 else " " for celda in fila))
# Ejemplo de uso
lab = crear_laberinto(5, 5)
print(lab.laberinto)
lab.mostrar_laberinto()