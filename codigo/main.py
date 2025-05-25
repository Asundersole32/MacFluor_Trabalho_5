from objective_function import resolver_trelica
from plot_module import plotar_trelica


nos = {
    0: (0, 0),
    1: (2, 0),
    2: (4, 0),
    3: (6, 0),
    4: (8, 0),
    5: (2, 1),
    6: (6, 1),
    7: (4, 2)
}

barras = [
    (0, 1),
    (0, 5),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 4),
    (3, 6),
    (4, 6),
    (5, 7),
    (6, 7)
]

areas = [0.0005] * len(barras)

forcas = {
    0: (0, -10000),
    2: (0, -20000),
    4: (0, -10000),
    5: (0, -10000),
    6: (0, -10000),
    7: (0, -10000)
}

apoios = {
    0: (True, True),
    4: (False, True)
}

forca_virtual = {
    2: (0, 1)
}

tabela, U, dof_map = resolver_trelica(nos, barras, areas, forcas, apoios, forca_virtual)
plotar_trelica(nos, barras, U, dof_map, tabela, escala=0.1)
print('Primeiro Exemplo')
print(tabela.to_string(index=False))
print("\n")

nos = {
    0: (0, 0),
    1: (2, 0),
    2: (4, 0),
    3: (6, 0),
    4: (8, 0),
    5: (2, 1),
    6: (6, 1),
    7: (4, 2)
}

barras = [
    (0, 1),
    (0, 5),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 4),
    (3, 6),
    (4, 6),
    (5, 7),
    (6, 7)
]

areas = [0.0005] * len(barras)

forcas = {
    0: (0, 10000),
    2: (0, 20000),
    4: (0, 10000),
    5: (0, 10000),
    6: (0, 10000),
    7: (0, 10000)
}

apoios = {
    0: (True, True),
    4: (False, True)
}

forca_virtual = {
    2: (0, 1)
}

tabela, U, dof_map = resolver_trelica(nos, barras, areas, forcas, apoios, forca_virtual)
plotar_trelica(nos, barras, U, dof_map, tabela, escala=0.1)
print('Segundo Exemplo')
print(tabela.to_string(index=False))
print("\n")


nos = {
    0: (0, 0),
    1: (2, 0),
    2: (4, 0),
    3: (6, 0),
    4: (8, 0),
    5: (2, 1),
    6: (6, 1),
    7: (4, 2)
}

barras = [
    (0, 1),
    (0, 5),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 4),
    (3, 6),
    (4, 6),
    (5, 7),
    (6, 7)
]

areas = [0.001] * len(barras)

forcas = {
    0: (0, 10000),
    2: (0, 20000),
    4: (0, 10000),
    5: (0, 10000),
    6: (0, 10000),
    7: (0, 10000)
}

apoios = {
    0: (True, True),
    4: (False, True)
}

forca_virtual = {
    2: (0, 1)
}

tabela, U, dof_map = resolver_trelica(nos, barras, areas, forcas, apoios, forca_virtual)
plotar_trelica(nos, barras, U, dof_map, tabela, escala=0.1)
print('Terceiro Exemplo')
print(tabela.to_string(index=False))
print("\n")


nos = {
    0: (0, 0),
    1: (2, 0),
    2: (4, 0),
    3: (6, 0),
    4: (8, 0),
    5: (2, 1),
    6: (6, 1),
    7: (4, 2)
}

barras = [
    (0, 1),
    (0, 5),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 4),
    (3, 6),
    (4, 6),
    (5, 7),
    (6, 7)
]

areas = [0.0005] * len(barras)

forcas = {
    0: (0, 10000),
    2: (0, -20000),
    4: (0, 10000),
    5: (0, 10000),
    6: (0, 20000),
    7: (0, -20000)
}

apoios = {
    0: (True, True),
    4: (False, True)
}

forca_virtual = {
    2: (0, 1)
}

tabela, U, dof_map = resolver_trelica(nos, barras, areas, forcas, apoios, forca_virtual)
plotar_trelica(nos, barras, U, dof_map, tabela, escala=0.1)
print('Quarto Exemplo')
print(tabela.to_string(index=False))
