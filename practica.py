# matriz = [[1,2,3],[4,5,6]]
# print("Valores de la matriz")
# for fila in range(len(matriz)):
    # for columna in range(len(matriz[0])):
        # print(f"{matriz[fila][columna]}")
# 
# lista = [7,8,9,10,11,12]
# print("Valores de la lista")
# for indice in range(len(lista)):
    # print(f"{lista[indice]}")
# 
# mi_set = {1,2,3,4,4,5,5}
# print(f"{mi_set}")

diccionario = {"GPU": ["Nvidia", "Rtx 2080Ti", 1000]}

for clave, valor in diccionario.items():
    print(f"{clave} - {valor}")

nombre = input("Ingrese nombre del producto: ")
marca = input("Ingrese marca del producto: ")
modelo = input("Ingrese modelo del producto: ")
precio = int(input("Ingrese precio del producto"))

detalle_producto = [marca, modelo, precio]
diccionario[nombre] = detalle_producto
for clave, valor in diccionario.items():
    print(f"{clave} - {valor}")