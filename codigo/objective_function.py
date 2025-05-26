import numpy as np
import pandas as pd

def resolver_trelica(nos, barras, restricoes, forcas, areas, E, forca_virtual=None):
    n_nos = len(nos)
    dof = 2 * n_nos
    K = np.zeros((dof, dof))
    L = []

    # Mapeamento dos graus de liberdade (usado para plotagem)
    dof_map = {}
    for i in range(n_nos):
        dof_map[i] = (2*i, 2*i+1)

    for idx, (i, j) in enumerate(barras):
        xi, yi = nos[i]
        xj, yj = nos[j]
        dx = xj - xi
        dy = yj - yi
        l = np.sqrt(dx**2 + dy**2)
        c = dx / l
        s = dy / l
        A = areas[idx]
        L.append(l)

        k_local = (E * A / l) * np.array([
            [ c*c,  c*s, -c*c, -c*s],
            [ c*s,  s*s, -c*s, -s*s],
            [-c*c, -c*s,  c*c,  c*s],
            [-c*s, -s*s,  c*s,  s*s]
        ])

        indices = [2*i, 2*i+1, 2*j, 2*j+1]
        for m in range(4):
            for n in range(4):
                K[indices[m], indices[n]] += k_local[m, n]

    # Vetor de forças
    F = np.zeros(dof)
    for no, (fx, fy) in forcas.items():
        F[2*no] = fx
        F[2*no+1] = fy

    # Restrições
    fixos = []
    for no, (rx, ry) in restricoes.items():
        if rx:
            fixos.append(2*no)
        if ry:
            fixos.append(2*no+1)

    livres = list(set(range(dof)) - set(fixos))
    K_reduzida = K[np.ix_(livres, livres)]
    F_reduzido = F[livres]

    # Resolver sistema
    U_reduzido = np.linalg.solve(K_reduzida, F_reduzido)

    U = np.zeros(dof)
    for idx, i in enumerate(livres):
        U[i] = U_reduzido[idx]

    # Esforços internos (forças reais N)
    N = []
    for idx, (i, j) in enumerate(barras):
        xi, yi = nos[i]
        xj, yj = nos[j]
        dx = xj - xi
        dy = yj - yi
        l = np.sqrt(dx**2 + dy**2)
        c = dx / l
        s = dy / l
        A = areas[idx]
        u = np.array([U[2*i], U[2*i+1], U[2*j], U[2*j+1]])
        n_local = (E * A / l) * np.array([-c, -s, c, s]) @ u
        N.append(n_local)

    # Análise de força virtual, se fornecida
    Δ = None
    if forca_virtual:
        Fv = np.zeros(dof)
        for no, (fx, fy) in forca_virtual.items():
            Fv[2*no] = fx
            Fv[2*no+1] = fy

        Fv_reduzido = Fv[livres]
        Uv_reduzido = np.linalg.solve(K_reduzida, Fv_reduzido)

        Uv = np.zeros(dof)
        for idx, i in enumerate(livres):
            Uv[i] = Uv_reduzido[idx]

        n = []
        for idx, (i, j) in enumerate(barras):
            xi, yi = nos[i]
            xj, yj = nos[j]
            dx = xj - xi
            dy = yj - yi
            l = np.sqrt(dx**2 + dy**2)
            c = dx / l
            s = dy / l
            A = areas[idx]
            u = np.array([Uv[2*i], Uv[2*i+1], Uv[2*j], Uv[2*j+1]])
            n_local = (E * A / l) * np.array([-c, -s, c, s]) @ u
            n.append(n_local)

        # Trabalho virtual: deslocamento Δ (em mm)
        Δ = [N[i] * n[i] * L[i] / (E * areas[i]) * 1e3 for i in range(len(barras))]

    # Construção do DataFrame
    resultados = pd.DataFrame({
        "Barra": list(range(len(barras))),
        "Nós": barras,
        "Comprimento (m)": np.round(L, 3),
        "Área (cm²)": np.round(np.array(areas) * 1e4, 2),
        "N (kN)": np.round(np.array(N) / 1e3, 3),
    })

    if Δ:
        resultados["n (kN)"] = np.round(np.array(n) / 1e3, 3)
        resultados["Δ (mm)"] = np.round(Δ, 4)

    return resultados, U, Δ, dof_map
