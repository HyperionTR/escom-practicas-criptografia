import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Variables globales
resultado_label = None

def cifrar_texto(texto, corrimiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            if caracter.isupper():
                codigo = ord(caracter) - ord('A')
                codigo = (codigo + corrimiento) % 26
                nuevo_caracter = chr(codigo + ord('A'))
                resultado += nuevo_caracter
            else:
                codigo = ord(caracter) - ord('a')
                codigo = (codigo + corrimiento) % 26
                nuevo_caracter = chr(codigo + ord('A'))
                resultado += nuevo_caracter
    return resultado

def descifrar_texto(texto, corrimiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            if caracter.isupper():
                codigo = ord(caracter) - ord('A')
                codigo = (codigo - corrimiento) % 26
                nuevo_caracter = chr(codigo + ord('a'))
                resultado += nuevo_caracter
            else:
                codigo = ord(caracter) - ord('a')
                codigo = (codigo - corrimiento) % 26
                nuevo_caracter = chr(codigo + ord('a'))
                resultado += nuevo_caracter
    return resultado

def procesar_texto():
    global resultado_label  # Utilizamos la variable global resultado_label
    archivo_entrada = filedialog.askopenfilename(title="Selecciona un archivo de texto")
    if not archivo_entrada:
        return

    corrimiento = int(corrimiento_entry.get())
    operacion = operacion_var.get()

    try:
        with open(archivo_entrada, 'r') as archivo:
            texto = archivo.read()
            if operacion == "Cifrar Texto":
                resultado = cifrar_texto(texto, corrimiento)
                archivo_salida = archivo_entrada.replace('.', '_c.')
            else:
                resultado = descifrar_texto(texto, corrimiento)
                archivo_salida = archivo_entrada.replace('.', '_d.')

        with open(archivo_salida, 'w') as archivo:
            archivo.write(resultado)

        resultado_label.config(text="Texto {} y guardado en {}".format(operacion.lower(), archivo_salida))
    except FileNotFoundError:
        resultado_label.config(text="El archivo de entrada no existe.")

def procesar_imagen():
    global resultado_label  # Utilizamos la variable global resultado_label
    try:
        shift_value = int(shift_entry.get()) % 256
        operacion = operacion_imagen_var.get()
        input_path = filedialog.askopenfilename(filetypes=[("BMP Files", "*.bmp")])
        imagen = Image.open(input_path)

        if operacion == "Cifrar Imagen":
            imagen_procesada = imagen.point(lambda p: (p + shift_value) % 256)
            output_path = input_path.replace(".bmp", "_c.bmp")
        elif operacion == "Descifrar Imagen":
            imagen_procesada = imagen.point(lambda p: (p - shift_value) % 256)
            output_path = input_path.replace(".bmp", "_d.bmp")

        imagen_procesada.save(output_path, "BMP")

        resultado_label.config(text=f"Imagen {operacion.lower()} y guardada con éxito.")
    except Exception as e:
        resultado_label.config(text=f"Error al {operacion.lower()} la imagen: {str(e)}")

# VENTANA
ventana = tk.Tk()
ventana.title("Cifrador/Descifrador de Archivos")

# Configuración para el cifrado/decifrado de texto
operacion_var = tk.StringVar()
operacion_var.set("Cifrar Texto")
operacion_label = tk.Label(ventana, text="Selecciona una operación para el texto:")
operacion_label.pack()
operacion_cifrar_texto = tk.Radiobutton(ventana, text="Cifrar Texto", variable=operacion_var, value="Cifrar Texto")
operacion_cifrar_texto.pack()
operacion_descifrar_texto = tk.Radiobutton(ventana, text="Descifrar Texto", variable=operacion_var, value="Descifrar Texto")
operacion_descifrar_texto.pack()

corrimiento_label = tk.Label(ventana, text="Valor del Corrimiento para Texto:")
corrimiento_label.pack()
corrimiento_entry = tk.Entry(ventana)
corrimiento_entry.pack()
procesar_texto_button = tk.Button(ventana, text="Seleccionar archivo de texto", command=procesar_texto)
procesar_texto_button.pack()

# Configuración para el cifrado/decifrado de imagen
operacion_imagen_var = tk.StringVar()
operacion_imagen_var.set("Cifrar Imagen")
operacion_imagen_label = tk.Label(ventana, text="Selecciona una operación para la imagen:")
operacion_imagen_label.pack()
operacion_cifrar_imagen = tk.Radiobutton(ventana, text="Cifrar Imagen", variable=operacion_imagen_var, value="Cifrar Imagen")
operacion_cifrar_imagen.pack()
operacion_descifrar_imagen = tk.Radiobutton(ventana, text="Descifrar Imagen", variable=operacion_imagen_var, value="Descifrar Imagen")
operacion_descifrar_imagen.pack()

shift_label = tk.Label(ventana, text="Valor de Corrimiento para Imagen:")
shift_label.pack()
shift_entry = tk.Entry(ventana)
shift_entry.pack()
procesar_imagen_button = tk.Button(ventana, text="Seleccionar archivo de imagen", command=procesar_imagen)
procesar_imagen_button.pack()

resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

ventana.mainloop()
