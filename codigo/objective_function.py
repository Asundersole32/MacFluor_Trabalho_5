import numpy as np
import pandas as pd
from scipy.linalg import solve


def resolver_trelica(nos, barras, areas, forcas, apoios, forca_virtual=None, E=200e6):

    n_nos = len(nos)
    n_barras = len(barras)
    dof_total = 2 * n_nos

    # Mapear graus de liberdade
    node_index = {node: idx for idx, node in enumerate(nos.keys())}
    dof_map = {}
    for node, idx in node_index.items():
        dof_map[node] = (2 * idx, 2 * idx + 1)

    # Montar matriz de rigidez global
    K = np.zeros((dof_total, dof_total))
    L = []
    T = []

    for b, (ni, nj) in enumerate(barras):
        xi, yi = nos[ni]
        xj, yj = nos[nj]
        dx = xj - xi
        dy = yj - yi
        l = np.sqrt(dx ** 2 + dy ** 2)
        c = dx / l
        s = dy / l

        L.append(l)
        T.append((c, s))

        A = areas[b]
        k_local = (E * A / l) * np.array([
            [c * c, c * s, -c * c, -c * s],
            [c * s, s * s, -c * s, -s * s],
            [-c * c, -c * s, c * c, c * s],
            [-c * s, -s * s, c * s, s * s]
        ])

        dof_i = dof_map[ni]
        dof_j = dof_map[nj]
        dof = [dof_i[0], dof_i[1], dof_j[0], dof_j[1]]

        for i in range(4):
            for j in range(4):
                K[dof[i], dof[j]] += k_local[i, j]

    # Vetor de forças externas
    F = np.zeros(dof_total)
    for node, (fx, fy) in forcas.items():
        i, j = dof_map[node]
        F[i] = fx
        F[j] = fy

    # Restrições (apoios)
    fixos = []
    for node, (fx, fy) in apoios.items():
        i, j = dof_map[node]
        if fx: fixos.append(i)
        if fy: fixos.append(j)

    livres = [i for i in range(dof_total) if i not in fixos]
    K_ll = K[np.ix_(livres, livres)]
    F_l = F[livres]

    # Resolver deslocamentos
    U = np.zeros(dof_total)
    U[livres] = solve(K_ll, F_l)

    # Calcular forças internas N
    N = []
    for b, (ni, nj) in enumerate(barras):
        i, j = dof_map[ni], dof_map[nj]
        u = np.array([U[i[0]], U[i[1]], U[j[0]], U[j[1]]])
        c, s = T[b]
        l = L[b]
        A = areas[b]
        n_local = (E * A / l) * np.array([-c, -s, c, s]) @ u
        N.append(n_local / 1000)  # converter para kN

    # FORÇA VIRTUAL (n e Δ)
    if forca_virtual:
        Fv = np.zeros(dof_total)
        for node, (fx, fy) in forca_virtual.items():
            i, j = dof_map[node]
            Fv[i] = fx
            Fv[j] = fy

        Fv_l = Fv[livres]
        Uv = np.zeros(dof_total)
        Uv[livres] = solve(K_ll, Fv_l)

        n = []
        for b, (ni, nj) in enumerate(barras):
            i, j = dof_map[ni], dof_map[nj]
            u = np.array([Uv[i[0]], Uv[i[1]], Uv[j[0]], Uv[j[1]]])
            c, s = T[b]
            l = L[b]
            A = areas[b]
            n_local = (E * A / l) * np.array([-c, -s, c, s]) @ u
            n.append(n_local / 1000)
    else:
        n = [0] * n_barras

    #deslocamento via trabalho virtual
    Δ = [N[i] * n[i] * L[i] / (E * areas[i]) * 1000 for i in range(n_barras)]

    # Resultado
    tabela = pd.DataFrame({
        "Barra": list(range(1, n_barras + 1)),
        "Nó_i": [b[0] for b in barras],
        "Nó_j": [b[1] for b in barras],
        "N (kN)": np.round(N, 3),
        "n (kN)": np.round(n, 3),
        "Δ (mm)": np.round(Δ, 100),
    })

    return tabela, U, dof_map
