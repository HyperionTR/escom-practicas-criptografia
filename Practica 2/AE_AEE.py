import tkinter as tk
from tkinter import messagebox


def euclides(alpha, n):
    while n:
        alpha, n = n, alpha % n
    return alpha

def euclides_extendido(alpha, n):
    if n == 0:
        return (1, 0, alpha)
    else:
        x, y, gcd = euclides_extendido(n, alpha % n)
        return (y, x - (alpha // n) * y, gcd)

def encontrar_inverso_mul(alpha, n):
    mcd = euclides(alpha, n)

    if mcd == 1:
        x, _, _ = euclides_extendido(alpha, n)
        while x < 0:
            x += n
        return x
    else:
        return None

def encontrar_inverso_ad(beta, n):
    inverso = n - beta % n
    return inverso

def calcular_ek_dk():
    try:
        alpha = int(entry_alpha.get())
        beta = int(entry_beta.get())
        n = int(entry_n.get())

        inverso_mul = encontrar_inverso_mul(alpha, n)
        inverso_ad = encontrar_inverso_ad(beta, n)

        if inverso_mul is not None:
            if beta <= 0 or beta > n:
                messagebox.showerror("Error", "El valor de beta debe estar en el rango (0, n].")
            else:
                resultado_label.config(text=f"Función de Cifrado (Ek): C = {alpha} p + {beta} mod {n}\nFunción de Descifrado (Dk): {inverso_mul} [C + ({inverso_ad})] mod {n}")
        else:
            messagebox.showerror("Error", "Alpha es invalido, ingresa otro valor para alpha.")

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores enteros válidos para alpha, beta y n.")

# Crear una ventana
ventana = tk.Tk()
ventana.title("AE y AEE")
ventana.geometry("300x200")

# Etiquetas y entradas para alpha, beta y n
label_alpha = tk.Label(ventana, text="Alpha:")
label_alpha.pack()
entry_alpha = tk.Entry(ventana)
entry_alpha.pack()

label_beta = tk.Label(ventana, text="Beta:")
label_beta.pack()
entry_beta = tk.Entry(ventana)
entry_beta.pack()

label_n = tk.Label(ventana, text="n:")
label_n.pack()
entry_n = tk.Entry(ventana)
entry_n.pack()

# Botón para calcular cifrado y descifrado
calcular_button = tk.Button(ventana, text="Obtener funciones Ek y Dk", command=calcular_ek_dk)
calcular_button.pack()

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

ventana.mainloop()
