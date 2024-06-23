import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def divided_diff(x, y):
    n = len(y)
    table = np.zeros((n, n))
    table[:, 0] = y
    
    for j in range(1, n):
        for i in range(n-j):
            table[i][j] = (table[i+1][j-1] - table[i][j-1]) / (x[i+j] - x[i])
    
    coefficients = table[0, :]
    return coefficients, table

def newton_interpolation(x, y, xi):
    n = len(x)
    assert n == len(y), "Arrays x e y devem ter o mesmo comprimento"
    
    coefficients, table = divided_diff(x, y)
    result = coefficients[0]
    
    for i in range(1, n):
        term = coefficients[i]
        for j in range(i):
            term *= (xi - x[j])
        result += term
    
    return result, table

def calcular_interpolacao():
    try:
        x_vals = list(map(float, entrada_x.get().split()))
        y_vals = list(map(float, entrada_y.get().split()))
        xi_val = float(entrada_xi.get())
        
        if len(x_vals) != len(y_vals):
            messagebox.showerror("Erro", "O número de pontos de x e y deve ser o mesmo.")
            return
        
        interpolated_value, diff_table = newton_interpolation(x_vals, y_vals, xi_val)
        
        x_interpolate = np.linspace(min(x_vals), max(x_vals), 100)
        y_interpolate = [newton_interpolation(x_vals, y_vals, xi)[0] for xi in x_interpolate]
        
        fig = plt.figure(figsize=(14, 6))
        gs = GridSpec(2, 1, height_ratios=[3, 1])
        
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        
        ax1.plot(x_vals, y_vals, 'ro', label='Pontos dados')
        ax1.plot(x_interpolate, y_interpolate, 'b-', label='Curva interpolada')
        ax1.plot(xi_val, interpolated_value, 'go', label=f'Interpolado em xi={xi_val}')
        ax1.set_title('Interpolação usando o Método de Diferenças Divididas')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.legend()
        ax1.grid(True)
        
        col_labels = [f'Δ^{i}' for i in range(diff_table.shape[1])]
        row_labels = [f'x{i}' for i in range(diff_table.shape[0])]
        ax2.axis('tight')
        ax2.axis('off')
        table = ax2.table(cellText=np.round(diff_table, 4), colLabels=col_labels, rowLabels=row_labels, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.2)
        
        plt.figtext(0.5, 0.02, f"O valor da interpolação é: {interpolated_value:.4f}", ha="center", fontsize=12)
        
        plt.tight_layout()
        plt.show()
        
        label_resultado.config(text=f"Valor interpolado em xi={xi_val}: {interpolated_value:.4f}")
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para x, y e xi.")

root = tk.Tk()
root.title("Interpolação por Diferenças Divididas")

tk.Label(root, text="Valores de x (separados por espaço):").pack()
entrada_x = tk.Entry(root, width=50)
entrada_x.pack()

tk.Label(root, text="Valores de y correspondentes (separados por espaço):").pack()
entrada_y = tk.Entry(root, width=50)
entrada_y.pack()

tk.Label(root, text="Valor de xi para interpolação:").pack()
entrada_xi = tk.Entry(root, width=20)
entrada_xi.pack()

btn_calcular = tk.Button(root, text="Calcular Interpolação", command=calcular_interpolacao)
btn_calcular.pack(pady=10)

label_resultado = tk.Label(root, text="")
label_resultado.pack(pady=10)

root.mainloop()
