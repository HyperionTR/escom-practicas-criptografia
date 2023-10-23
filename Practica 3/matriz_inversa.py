import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import numpy as np
from fractions import Fraction

matrix_entries = []
inverse = None  # Variable para almacenar la matriz inversa

def create_matrix():
    size = matrix_size_var.get()
    n_value = n_var.get()

    try:
        size = int(size)
        n_value = int(n_value)
    except ValueError:
        messagebox.showerror("Error", "Debes ingresar valores válidos para m y n.")
        return

    if size not in [2, 3, 4]:
        messagebox.showerror("Error", "Solo se pueden crear matrices de 2x2, 3x3 o 4x4.")
        return

    global matrix_entries
    matrix_entries = []

    for i in range(size):
        row_entries = []
        for j in range(size):
            label = Label(matrix_frame, text=f'M[{i + 1},{j + 1}]:')
            entry = Entry(matrix_frame, width=6)
            label.grid(row=i, column=j * 2)
            entry.grid(row=i, column=j * 2 + 1)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

    calculate_button.config(state="active")

def calculate_inverse():
    global inverse  # Guarda la matriz inversa como una variable global para poder copiarla posteriormente
    if not matrix_entries:
        messagebox.showerror("Error", "Primero debes crear una matriz.")
        return

    try:
        matrix = []
        for row in matrix_entries:
            matrix_row = [entry.get() for entry in row]
            if any(value == '' for value in matrix_row):
                messagebox.showerror("Error", "Debes llenar todos los campos de la matriz.")
                return
            matrix_row = [Fraction(value) for value in matrix_row]
            matrix.append(matrix_row)

        result_label.config(text="Matriz Inversa:")

        # Obtener el valor de n
        n_value = n_var.get()
        try:
            n_value = int(n_value)
        except ValueError:
            messagebox.showerror("Error", "Debes ingresar un valor válido para n.")
            return

        # Calcular la matriz inversa
        inverse = np.linalg.inv(np.array(matrix, dtype=float))
        
        # Convertimos la matriz inversa en fracciones   
        inverse = np.array([[Fraction(value).limit_denominator() for value in row] for row in inverse])
        
        # Calcular la matriz inversa módulo n
        inverse_mod_n = calculate_inverse_mod_n(inverse, n_value)

        # Mostrar ambas matrices
        display_matrices(inverse, inverse_mod_n)
    except ValueError:
        result_label.config(text="No se puede calcular la matriz inversa")
        messagebox.showerror("Error", "Los valores ingresados en la matriz deben ser números válidos.")
    except np.linalg.LinAlgError:
        result_label.config(text="No se puede calcular la matriz inversa")
        messagebox.showerror("Error", "La matriz no es invertible")

def calculate_inverse_mod_n(matrix, n_value):
    size = len(matrix)
    inverse_mod_n = np.zeros((size, size), dtype=int)

    for i in range(size):
        for j in range(size):
            a = Fraction(matrix[i][j]).numerator  # Numerador de la fracción
            b = Fraction(matrix[i][j]).denominator  # Denominador de la fracción
            if a < 0:
                a_mod_n = a % n_value  # Inverso aditivo en modularidad
            else:
                a_mod_n = a
            b_mod_n = pow(b, -1, n_value)  # Inverso multiplicativo en modularidad

            result = a_mod_n * b_mod_n % n_value
            inverse_mod_n[i][j] = result

    return inverse_mod_n

def copy_inverse_to_matrix():
    if inverse is not None:
        for i in range(len(inverse)):
            for j in range(len(inverse)):
                matrix_entries[i][j].delete(0, tk.END)
                matrix_entries[i][j].insert(0, str(Fraction(inverse[i, j]).limit_denominator()))

def display_matrices(inverse, inverse_mod_n):
    # Limpia el marco de resultados
    for widget in result_frame.winfo_children():
        widget.grid_forget()

    # Muestra la matriz inversa
    result_label.config(text="Matriz Inversa:")
    for i in range(len(inverse)):
        for j in range(len(inverse)):
            inverse_entry = Entry(result_frame, width=10)
            inverse_entry.insert(0, str(Fraction(inverse[i, j]).limit_denominator()))
            inverse_entry.grid(row=i, column=j)

    # Muestra la matriz inversa módulo n
    result_label_mod_n = Label(result_frame, text=f"Matriz Inversa Modulo n ({n_var.get()}):")
    result_label_mod_n.grid(row=len(inverse) + 1, columnspan=len(inverse_mod_n))
    for i in range(len(inverse_mod_n)):
        for j in range(len(inverse_mod_n)):
            inverse_mod_n_entry = Entry(result_frame, width=10)
            inverse_mod_n_entry.insert(0, str(inverse_mod_n[i, j]))
            inverse_mod_n_entry.grid(row=len(inverse) + i + 2, column=j)

    # Crear un botón para copiar la matriz inversa a la matriz de entrada
    copy_button = Button(result_frame, text="Copiar a Matriz", command=copy_inverse_to_matrix)
    copy_button.grid(row=len(inverse) + len(inverse_mod_n) + 2, columnspan=len(inverse))

root = tk.Tk()
root.title("Calculadora de Matriz Inversa")

matrix_size_var = tk.StringVar()
matrix_entries_var = tk.StringVar()
n_var = tk.StringVar()

matrix_size_label = Label(root, text="Tamaño de la Matriz (2, 3, o 4):")
matrix_size_entry = Entry(root, textvariable=matrix_size_var)
n_label = Label(root, text="Valor de n:")
n_entry = Entry(root, textvariable=n_var)
create_matrix_button = Button(root, text="Crear Matriz", command=create_matrix)

matrix_size_label.pack()
matrix_size_entry.pack()
n_label.pack()
n_entry.pack()
create_matrix_button.pack()

matrix_frame = tk.Frame(root)
matrix_frame.pack()

calculate_button = Button(root, text="Calcular Inversa", state="disabled", command=calculate_inverse)
calculate_button.pack()

result_label = Label(root, text="")
result_label.pack()

result_frame = tk.Frame(root)
result_frame.pack()

root.mainloop()