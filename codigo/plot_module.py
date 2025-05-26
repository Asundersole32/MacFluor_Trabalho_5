import matplotlib.pyplot as plt


def plotar_trelica(nos, barras, U, dof_map, tabela, escala=0.1):

    def deslocado(n, coord):
        dx = U[dof_map[n][0]]
        dy = U[dof_map[n][1]]
        return (coord[0] + escala * dx, coord[1] + escala * dy)

    plt.figure(figsize=(10, 5))
    for i, (n1, n2) in enumerate(barras):
        x1, y1 = nos[n1]
        x2, y2 = nos[n2]
        xn1, yn1 = deslocado(n1, nos[n1])
        xn2, yn2 = deslocado(n2, nos[n2])

        # Força interna na barra
        N = tabela.loc[i, "N (kN)"]

        # Cor por type de esforço
        if N > 1e-3:
            cor = 'blue'  # tração
        elif N < -1e-3:
            cor = 'red'   # compressão
        else:
            cor = 'gray'  # neutra

        # Barra original
        plt.plot([x1, x2], [y1, y2], 'k--', alpha=0.4)

        # Barra deslocada
        plt.plot([xn1, xn2], [yn1, yn2], color=cor, linewidth=2)

        # Rótulo com número da barra
        xm, ym = (x1 + x2)/2, (y1 + y2)/2
        plt.text(xm, ym, f"{i+1}", fontsize=8, ha='center', va='center', color='black')

    # Nós originais
    for n, (x, y) in nos.items():
        plt.plot(x, y, 'ko')
        plt.text(x, y - 0.2, f"N{n}", ha='center', fontsize=8)

    plt.axis('equal')
    plt.title("Treliça Original (tracejada) vs Deslocada (colorida)")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)
    plt.show()