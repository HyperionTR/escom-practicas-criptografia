import tkinter as tk
from tkinter import filedialog, messagebox
import os

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, a, b):
    result = ""
    m = 26  # Tamaño del alfabeto inglés

    for char in text:
        if char.isalpha():
            if char.islower():
                result += chr(((a * (ord(char) - ord('a')) + b) % m) + ord('A'))
            elif char.isupper():
                result += chr(((a * (ord(char) - ord('A')) + b) % m) + ord('A'))
        else:
            result += char

    return result

def affine_decrypt(ciphertext, a, b):
    result = ""
    m = 26  # Tamaño del alfabeto inglés
    a_inverse = mod_inverse(a, m)

    for char in ciphertext:
        if char.isalpha():
            if char.islower():
                result += chr(((a_inverse * (ord(char) - ord('a') - b)) % m) + ord('a'))
            elif char.isupper():
                result += chr(((a_inverse * (ord(char) - ord('A') - b)) % m) + ord('a'))
        else:
            result += char

    return result


def load_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        text.delete('1.0', tk.END)
        text.insert(tk.END, file.read())
    global original_file_path
    original_file_path = file_path


def save_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)


def get_output_path(file_path, suffix):
    file_dir, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)
    output_file_name = f"{base_name}{suffix}{ext}"
    output_file_path = os.path.join(file_dir, output_file_name)
    return output_file_path


def encrypt_text():
    a = int(a_entry.get())
    b = int(b_entry.get())
    message = text.get('1.0', tk.END)

    # Eliminar espacios y saltos de línea
    message = ''.join(message.split())

    try:
        encrypted_message = affine_encrypt(message, a, b)
        result.delete('1.0', tk.END)
        result.insert(tk.END, encrypted_message)

        # Guardar el texto cifrado en un archivo en la misma carpeta que el archivo original
        output_path = get_output_path(original_file_path, "_c")
        save_file(encrypted_message, output_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error durante el cifrado: {str(e)}")

def decrypt_text():
    a = int(a_entry.get())
    b = int(b_entry.get())
    ciphertext = text.get('1.0', tk.END)

    try:
        decrypted_message = affine_decrypt(ciphertext, a, b)
        result.delete('1.0', tk.END)
        result.insert(tk.END, decrypted_message)

        # Guardar el texto descifrado en un archivo en la misma carpeta que el archivo original
        output_path = get_output_path(original_file_path, "_d")
        save_file(decrypted_message, output_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error durante el descifrado: {str(e)}")


# Crear la ventana principal
root = tk.Tk()
root.title("Cifrador Afín")

# Crear elementos de la interfaz gráfica
original_file_path = ""
load_button = tk.Button(root, text="Cargar Archivo", command=load_file)
a_label = tk.Label(root, text="Valor de Alpha (Multiplicativo):")
a_entry = tk.Entry(root)
b_label = tk.Label(root, text="Valor de Beta (Aditivo):")
b_entry = tk.Entry(root)
text_label = tk.Label(root, text="Texto:")
text = tk.Text(root, height=10, width=40)
encrypt_button = tk.Button(root, text="Cifrar Texto", command=encrypt_text)
decrypt_button = tk.Button(root, text="Descifrar Texto", command=decrypt_text)
result_label = tk.Label(root, text="Resultado:")
result = tk.Text(root, height=10, width=40)

# Colocar elementos en la ventana
load_button.grid(row=0, column=0)
a_label.grid(row=1, column=0)
a_entry.grid(row=1, column=1)
b_label.grid(row=2, column=0)
b_entry.grid(row=2, column=1)
text_label.grid(row=3, column=0)
text.grid(row=3, column=1)
encrypt_button.grid(row=4, column=0)
decrypt_button.grid(row=4, column=1)
result_label.grid(row=5, column=0)
result.grid(row=5, column=1)

# Ejecutar la aplicación
root.mainloop()
