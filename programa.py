import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

def divided_diff(x, y):
    n = len(y)
    coefficients = np.copy(y)
    
    for i in range(1, n):
        for j in range(n-1, i-1, -1):
            coefficients[j] = (coefficients[j] - coefficients[j-1]) / (x[j] - x[j-i])
    
    return coefficients

def newton_interpolation(x, y, xi):
    n = len(x)
    assert n == len(y), "Arrays x e y devem ter o mesmo comprimento"
    
    coefficients = divided_diff(x, y)
    n -= 1
    result = coefficients[n]
    
    for i in range(n-1, -1, -1):
        result = result * (xi - x[i]) + coefficients[i]
    
    return result

def calcular_interpolacao():
    try:
        x_vals = list(map(float, entrada_x.get().split()))
        y_vals = list(map(float, entrada_y.get().split()))
        xi_val = float(entrada_xi.get())
        
        # verifica se o número de pontos x e y é o mesmo
        if len(x_vals) != len(y_vals):
            messagebox.showerror("Erro", "O número de pontos de x e y deve ser o mesmo.")
            return
        
        # calcula interpolação
        interpolated_value = newton_interpolation(x_vals, y_vals, xi_val)
        
        # gera pontos para o gráfico
        x_interpolate = np.linspace(min(x_vals), max(x_vals), 100)
        y_interpolate = [newton_interpolation(x_vals, y_vals, xi) for xi in x_interpolate]
        
        # ajusta uma reta aos pontos usando numpy
        coefficients = np.polyfit(x_vals, y_vals, 1)
        linear_eq = f'y = {coefficients[0]:.3f}x + {coefficients[1]:.3f}'
        
        # calcula R^2
        p = np.poly1d(coefficients)
        y_hat = p(x_vals)
        y_mean = np.mean(y_vals)
        ss_tot = np.sum((y_vals - y_mean) ** 2)
        ss_res = np.sum((y_vals - y_hat) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, 'ro', label='Pontos dados')
        plt.plot(x_interpolate, y_interpolate, 'b-', label='Curva interpolada')
        plt.plot(xi_val, interpolated_value, 'go', label=f'Interpolado em xi={xi_val}')
        plt.title('Interpolação usando o Método de Diferenças Divididas')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        
        # exibe o valor interpolado e a equação da reta ajustada no gráfico
        plt.text(0.5, 0.02, f'Valor interpolado em xi={xi_val} é y={interpolated_value}\n{linear_eq}\nR² = {r_squared:.3f}', ha='center', va='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
        
        # mostra o gráfico
        plt.show()
        
        # exibe a equação da reta ajustada na interface
        label_resultado.config(text=f"Equação da reta ajustada: {linear_eq}\nR²: {r_squared:.3f}\nValor interpolado em xi={xi_val}: {interpolated_value:.3f}")
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para x, y e xi.")

# configurando interface gráfica com tkinter
root = tk.Tk()
root.title("Interpolação por Diferenças Divididas")

# entradas para os valores de x, y e xi
tk.Label(root, text="Valores de x (separados por espaço):").pack()
entrada_x = tk.Entry(root, width=50)
entrada_x.pack()

tk.Label(root, text="Valores de y correspondentes (separados por espaço):").pack()
entrada_y = tk.Entry(root, width=50)
entrada_y.pack()

tk.Label(root, text="Valor de xi para interpolação:").pack()
entrada_xi = tk.Entry(root, width=20)
entrada_xi.pack()

# botão para calcular a interpolação
btn_calcular = tk.Button(root, text="Calcular Interpolação", command=calcular_interpolacao)
btn_calcular.pack(pady=10)

# label para mostrar a equação da reta ajustada, o R² e o valor interpolado
label_resultado = tk.Label(root, text="")
label_resultado.pack(pady=10)

# roda a interface
root.mainloop()
