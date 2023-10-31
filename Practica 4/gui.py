from typing import Literal
from crypto_modes import cifrado_des
from crypto_modes import decifrado_des
from Crypto.Cipher import DES

import tkinter as tk
from tkinter import messagebox, filedialog, IntVar

from PIL import Image, ImageTk

# Variable global para almacenar el nombre del archivo cargado
nombre_archivo: str = ""
imagen_original = None
imagen_thumbnail = None

def cargar_archivo():
    global nombre_archivo, imagen_original, imagen_thumbnail
    nombre_archivo = filedialog.askopenfilename(filetypes=[("Mapas de bits (BMP)", "*.bmp")])
    if nombre_archivo:
        imagen_original = Image.open(nombre_archivo)
        imagen_thumbnail = imagen_original.copy()
        imagen_thumbnail.thumbnail((200, 200))  # Redimensionar la imagen para visualización
        imagen_tk = ImageTk.PhotoImage(imagen_thumbnail)
        imagen_label.config(image=imagen_tk)
        imagen_label.image = imagen_tk  # Mantener una referencia para que no se elimine

def guardar_archivo( byte_data: bytes, *, proceso_cifrado: Literal["cipher", "decipher"] = "cipher" ):
	"""Guarda los datos de pixel de la imágen BMP en un archivo modificando el nombre de archivo según el proceso criptográfico que se le halla aplicado a la imágen

	Args:
		byte_data (bytes): Los datos de pixel de la imágen BMP
	"""
	# ALmacenamos las siglas del modo de operación en formato de texto
	selected_mode = get_selected_mode()
	modo_texto = "ECB" if selected_mode == DES.MODE_ECB else \
				 "CBC" if selected_mode == DES.MODE_CBC else \
				 "CFB" if selected_mode == DES.MODE_CFB else \
				 "OFB" if selected_mode == DES.MODE_OFB else ""	
 
 	# Guardar los datos cifrados en un archivo con el nombre modificado
	if proceso_cifrado == "cipher":
		archivo_salida = nombre_archivo.replace(".bmp", f"_e{modo_texto}.bmp")
	elif proceso_cifrado == "decipher":
		archivo_salida = nombre_archivo.replace(".bmp", f"_d{modo_texto}.bmp")
	else:
		archivo_salida = nombre_archivo.replace(".bmp", f"_{modo_texto}.bmp")

	imagen_salida = Image.frombytes(imagen_original.mode, imagen_original.size, byte_data)
	imagen_salida.save(archivo_salida)

	messagebox.showinfo("Información", f"Imagen cifrada guardada en:\n {archivo_salida}")

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

def cb_cifrado():
    plain_data = imagen_original.tobytes()
    encrypted_data = cifrado_des(clave_entry.get(), iv_entry.get(), plain_data, get_selected_mode())
    update_image_label( encrypted_data )
    guardar_archivo( encrypted_data, proceso_cifrado="cipher" )
    
def cb_descifrado():
    encrypted_data = imagen_original.tobytes()
    decrypted_data = decifrado_des(clave_entry.get(), iv_entry.get(), encrypted_data, get_selected_mode())
    update_image_label( decrypted_data )
    guardar_archivo( decrypted_data, proceso_cifrado="decipher" )

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
cifrar_button = tk.Button(ventana, text="Cifrar", command=cb_cifrado )
descifrar_button = tk.Button(ventana, text="Descifrar", command=cb_descifrado )
cifrar_button.pack()
descifrar_button.pack()
