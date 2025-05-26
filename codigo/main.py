from objective_function import resolver_trelica
from plot_module import plotar_trelica

# Lista de exemplos
exemplos = [
    {
        "nome": "Primeiro Exemplo",
        "areas": [0.0005] * 13,
        "forcas": {
            0: (0, -10000),
            2: (0, -20000),
            4: (0, -10000),
            5: (0, -10000),
            6: (0, -10000),
            7: (0, -10000)
        },
        "forca_virtual": {
            2: (0, 1000)
        }
    },
    {
        "nome": "Segundo Exemplo",
        "areas": [0.0005] * 13,
        "forcas": {
            0: (0, 10000),
            2: (0, 20000),
            4: (0, 10000),
            5: (0, 10000),
            6: (0, 10000),
            7: (0, 10000)
        },
        "forca_virtual": {
            2: (0, 1)
        }
    },
    {
        "nome": "Terceiro Exemplo",
        "areas": [0.001] * 13,
        "forcas": {
            0: (0, 10000),
            2: (0, 20000),
            4: (0, 10000),
            5: (0, 10000),
            6: (0, 10000),
            7: (0, 10000)
        },
        "forca_virtual": {
            2: (0, 1)
        }
    },
    {
        "nome": "Quarto Exemplo",
        "areas": [0.0005] * 13,
        "forcas": {
            0: (0, 10000),
            2: (0, -20000),
            4: (0, 10000),
            5: (0, 10000),
            6: (0, 20000),
            7: (0, -20000)
        },
        "forca_virtual": {
            2: (0, 1)
        }
    }
]

# Dados fixos para todos os exemplos
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

apoios = {
    0: (True, True),
    4: (False, True)
}

E = 210e9  # Módulo de Young em Pascal (Aço)

# Loop pelos exemplos
for exemplo in exemplos:
    tabela, U, Δ, dof_map = resolver_trelica(
        nos=nos,
        barras=barras,
        restricoes=apoios,
        forcas=exemplo["forcas"],
        areas=exemplo["areas"],
        E=E,
        forca_virtual=exemplo["forca_virtual"]
    )

    plotar_trelica(nos, barras, U, dof_map, tabela, escala=100)
    print(exemplo["nome"])
    print(tabela.to_string(index=False))
    print("\n")
