from crypto_modes import cifrado_des
from crypto_modes import decifrado_des
from Crypto.Cipher import DES

import tkinter as tk
from tkinter import messagebox, filedialog, IntVar

from PIL import Image, ImageTk

# Variable global para almacenar el nombre del archivo cargado
nombre_archivo = ""
imagen_original = None

def cargar_archivo():
    global nombre_archivo, imagen_original
    nombre_archivo = filedialog.askopenfilename(filetypes=[("Mapas de bits (BMP)", "*.bmp")])
    if nombre_archivo:
        imagen_original = Image.open(nombre_archivo)
        imagen_original.thumbnail((200, 200))  # Redimensionar la imagen para visualización
        imagen_tk = ImageTk.PhotoImage(imagen_original)
        imagen_label.config(image=imagen_tk)
        imagen_label.image = imagen_tk  # Mantener una referencia para que no se elimine
	

def get_selected_mode():
    modo_sel = modo_cifrado.get()
    return DES.MODE_ECB if modo_sel == 1 else \
           DES.MODE_CBC if modo_sel == 2 else \
           DES.MODE_CFB if modo_sel == 3 else \
           DES.MODE_OFB if modo_sel == 4 else None

def update_image_label( byte_data: bytes ):
	"""Modifica la etiqueta de la imagen de la ventana a partir de los datos de pixel de la imágen BMP

	Args:
		byte_data (bytes): Los datos de pixel de la imágen BMP
	"""
    # Mostrar la imagen descifrada
	imagen = Image.frombytes(imagen_original.mode, imagen_original.size, byte_data)
	imagen.thumbnail((200, 200))  # Redimensionar la imagen a un tamaño no mayor a 200x200
	imagen_tk = ImageTk.PhotoImage(imagen)
	imagen_label.config(image=imagen_tk)
	imagen_label.image = imagen_tk  # Mantener una referencia para que no se elimine

# Definición de las funciones lambda para utilizarse en los botones
cifrado = lambda: update_image_label( cifrado_des(clave_entry.get(), iv_entry.get(), nombre_archivo, get_selected_mode()) )
decifrado = lambda: update_image_label( decifrado_des(clave_entry.get(), iv_entry.get(), nombre_archivo, get_selected_mode()) )

# Crear la ventana principal
ventana = tk.Tk(screenName="Cifrado y Descifrado de Imágenes BMP")
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

# Etiqueta del vector de inicialización
iv_label = tk.Label(ventana, text="Vector de inicialización (8 bytes):")
iv_label.pack()

# Campo de entrada del vector de inicialización
iv_entry = tk.Entry(ventana)
iv_entry.pack()

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
cifrar_button = tk.Button(ventana, text="Cifrar", command=cifrado )
descifrar_button = tk.Button(ventana, text="Descifrar", command=decifrado )
cifrar_button.pack()
descifrar_button.pack()
