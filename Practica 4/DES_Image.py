import tkinter as tk
from tkinter import messagebox, filedialog, IntVar
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image, ImageTk

# Variable global para almacenar el nombre del archivo cargado
nombre_archivo = ""
imagen_original = None


def cargar_archivo():
    global nombre_archivo, imagen_original
    nombre_archivo = filedialog.askopenfilename(filetypes=[("Imágenes BMP", "*.bmp")])
    if nombre_archivo:
        imagen_original = Image.open(nombre_archivo)
        imagen_original.thumbnail((200, 200))  # Redimensionar la imagen para visualización
        imagen_tk = ImageTk.PhotoImage(imagen_original)
        imagen_label.config(image=imagen_tk)
        imagen_label.image = imagen_tk  # Mantener una referencia para que no se elimine


def cifrar():
    clave = clave_entry.get()

    # Validar que se haya ingresado una clave de 8 bytes
    if len(clave) != 8:
        messagebox.showerror("Error", "La clave debe tener 8 bytes")
        return

    if nombre_archivo:
        try:
            clave_bytes = bytes(clave, 'utf-8')
            selected_mode = get_selected_mode()

            if selected_mode in [DES.MODE_ECB, DES.MODE_CBC]:
                # Modos que funcionan con datos en bloques
                cipher = DES.new(clave_bytes, selected_mode)

                with open(nombre_archivo, 'rb') as file:
                    datos = file.read()
                    datos_cifrados = cipher.encrypt(pad(datos, 8))

            elif selected_mode in [DES.MODE_CFB, DES.MODE_OFB]:
                # Modos que funcionan con flujo de datos
                iv = get_random_bytes(8)
                cipher = DES.new(clave_bytes, selected_mode, iv=iv)

                with open(nombre_archivo, 'rb') as file:
                    datos = file.read()
                    datos_cifrados = cipher.encrypt(datos)

            # Determinar el modo en formato de texto
            modo_texto = get_selected_mode_text()

            # Guardar los datos cifrados en un archivo con el nombre modificado
            archivo_salida = nombre_archivo.replace(".bmp", f"_e{modo_texto}.bmp")
            with open(archivo_salida, 'wb') as output_file:
                output_file.write(datos_cifrados)

            messagebox.showinfo("Información", f"Imagen cifrada guardada en {archivo_salida}")

            # Mostrar la imagen cifrada
            imagen_cifrada = Image.frombytes(imagen_original.mode, imagen_original.size, datos_cifrados)
            imagen_cifrada.thumbnail((200, 200))  # Redimensionar la imagen para visualización
            imagen_tk = ImageTk.PhotoImage(imagen_cifrada)
            imagen_label.config(image=imagen_tk)
            imagen_label.image = imagen_tk  # Mantener una referencia para que no se elimine

        except Exception as e:
            messagebox.showerror("Error", str(e))


def descifrar():
    clave = clave_entry.get()

    # Validar que se haya ingresado una clave de 8 bytes
    if len(clave) != 8:
        messagebox.showerror("Error", "La clave debe tener 8 bytes")
        return

    if nombre_archivo:
        try:
            clave_bytes = bytes(clave, 'utf-8')
            selected_mode = get_selected_mode()

            if selected_mode in [DES.MODE_ECB, DES.MODE_CBC]:
                # Modos que funcionan con datos en bloques
                cipher = DES.new(clave_bytes, selected_mode)

                with open(nombre_archivo, 'rb') as file:
                    datos_cifrados = file.read()
                    datos_descifrados = unpad(cipher.decrypt(datos_cifrados), 8)

            elif selected_mode in [DES.MODE_CFB, DES.MODE_OFB]:
                # Modos que funcionan con flujo de datos
                iv = get_random_bytes(8)
                cipher = DES.new(clave_bytes, selected_mode, iv=iv)

                with open(nombre_archivo, 'rb') as file:
                    datos_cifrados = file.read()
                    datos_descifrados = cipher.decrypt(datos_cifrados)

            # Determinar el modo en formato de texto
            modo_texto = get_selected_mode_text()

            # Guardar los datos descifrados en un archivo con el nombre modificado
            archivo_salida = nombre_archivo.replace(f".bmp", f"_d{modo_texto}.bmp")
            with open(archivo_salida, 'wb') as output_file:
                output_file.write(datos_descifrados)

            messagebox.showinfo("Información", f"Imagen descifrada guardada en {archivo_salida}")

            # Mostrar la imagen descifrada
            imagen_descifrada = Image.frombytes(imagen_original.mode, imagen_original.size, datos_descifrados)
            imagen_descifrada.thumbnail((200, 200))  # Redimensionar la imagen para visualización
            imagen_tk = ImageTk.PhotoImage(imagen_descifrada)
            imagen_label.config(image=imagen_tk)
            imagen_label.image = imagen_tk  # Mantener una referencia para que no se elimine

        except Exception as e:
            messagebox.showerror("Error", str(e))


def get_selected_mode():
    if modo_cifrado.get() == 1:
        return DES.MODE_ECB
    elif modo_cifrado.get() == 2:
        return DES.MODE_CBC
    elif modo_cifrado.get() == 3:
        return DES.MODE_CFB
    elif modo_cifrado.get() == 4:
        return DES.MODE_OFB


def get_selected_mode_text():
    if modo_cifrado.get() == 1:
        return "ECB"
    elif modo_cifrado.get() == 2:
        return "CBC"
    elif modo_cifrado.get() == 3:
        return "CFB"
    elif modo_cifrado.get() == 4:
        return "OFB"


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Cifrado y Descifrado de Imágenes BMP")

# Opciones de modo de cifrado DES
modo_cifrado = IntVar()
cifrado_label = tk.Label(ventana, text="Elige un modo de operación")
ecb_radio = tk.Radiobutton(ventana, text="ECB", variable=modo_cifrado, value=1)
cbc_radio = tk.Radiobutton(ventana, text="CBC", variable=modo_cifrado, value=2)
cfb_radio = tk.Radiobutton(ventana, text="CFB", variable=modo_cifrado, value=3)
ofb_radio = tk.Radiobutton(ventana, text="OFB", variable=modo_cifrado, value=4)

cifrado_label.pack()
ecb_radio.pack()
cbc_radio.pack()
cfb_radio.pack()
ofb_radio.pack()

# Etiqueta de la clave
clave_label = tk.Label(ventana, text="Clave DES (8 bytes):")
clave_label.pack()

# Campo de entrada de la clave
clave_entry = tk.Entry(ventana)
clave_entry.pack()

# Etiqueta del archivo de imagen
archivo_label = tk.Label(ventana, text="Selecciona una imagen BMP:")
archivo_label.pack()

# Botón para cargar una imagen BMP
cargar_button = tk.Button(ventana, text="Cargar Imagen", command=cargar_archivo)
cargar_button.pack()

# Etiqueta para mostrar la imagen
imagen_label = tk.Label(ventana)
imagen_label.pack()

# Botones para cifrar y descifrar
cifrar_button = tk.Button(ventana, text="Cifrar", command=cifrar)
descifrar_button = tk.Button(ventana, text="Descifrar", command=descifrar)
cifrar_button.pack()
descifrar_button.pack()

ventana.mainloop()
