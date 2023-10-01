import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import DES

# Variable global para almacenar el nombre del archivo cargado
nombre_archivo = ""

def cargar_archivo():
    global nombre_archivo
    nombre_archivo = filedialog.askopenfilename()
    if nombre_archivo:
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            texto_entry.delete(0, tk.END)
            texto_entry.insert(0, file.read())

def cifrar():
    clave = clave_entry.get()
    texto_a_cifrar = texto_entry.get()

    # Validar que se haya ingresado una clave de 8 bytes
    if len(clave) != 8:
        messagebox.showerror("Error", "La clave debe tener 8 bytes")
        return

    try:
        clave_bytes = bytes(clave, 'utf-8')
        cipher = DES.new(clave_bytes, DES.MODE_ECB)

        # Asegurarse de que los datos tengan una longitud múltiplo de 8 (bloque DES)
        padding_length = 8 - (len(texto_a_cifrar) % 8)
        texto_a_cifrar += ' ' * padding_length

        datos_cifrados = cipher.encrypt(texto_a_cifrar.encode('utf-8'))
        resultado_entry.delete(0, tk.END)
        resultado_entry.insert(0, datos_cifrados.hex())

        if nombre_archivo:
            # Obtener la extensión del archivo original
            extension = nombre_archivo.split('.')[-1]
            # Guardar el texto cifrado en un archivo con _c antes de la extensión
            archivo_salida = nombre_archivo.replace(f".{extension}", f"_c.{extension}")
            with open(archivo_salida, 'w', encoding='utf-8') as file:
                file.write(datos_cifrados.hex())
                messagebox.showinfo("Información", f"Texto cifrado guardado en {archivo_salida}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def descifrar():
    clave = clave_entry.get()
    datos_cifrados_hex = texto_entry.get()

    # Validar que se haya ingresado una clave de 8 bytes
    if len(clave) != 8:
        messagebox.showerror("Error", "La clave debe tener 8 bytes")
        return

    try:
        clave_bytes = bytes(clave, 'utf-8')
        datos_cifrados = bytes.fromhex(datos_cifrados_hex)
        cipher = DES.new(clave_bytes, DES.MODE_ECB)
        datos_descifrados = cipher.decrypt(datos_cifrados)

        # No quitar el relleno aquí, simplemente mostrar los datos descifrados
        resultado_entry.delete(0, tk.END)
        resultado_entry.insert(0, datos_descifrados.decode('utf-8'))

        if nombre_archivo:
            # Obtener la extensión del archivo original
            extension = nombre_archivo.split('.')[-1]
            # Guardar el texto descifrado en un archivo con _d antes de la extensión
            archivo_salida = nombre_archivo.replace(f".{extension}", f"_d.{extension}")
            with open(archivo_salida, 'w', encoding='utf-8') as file:
                file.write(datos_descifrados.decode('utf-8'))
                messagebox.showinfo("Información", f"Texto descifrado guardado en {archivo_salida}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Cifrado y Descifrado DES")

# Etiqueta de la clave
clave_label = tk.Label(ventana, text="Clave DES (8 bytes):")
clave_label.pack()

# Campo de entrada de la clave
clave_entry = tk.Entry(ventana)
clave_entry.pack()

# Etiqueta del archivo de texto
archivo_label = tk.Label(ventana, text="Selecciona un archivo de texto:")
archivo_label.pack()

# Botón para cargar un archivo de texto
cargar_button = tk.Button(ventana, text="Cargar Archivo", command=cargar_archivo)
cargar_button.pack()

# Etiqueta del texto a cifrar o descifrar
texto_label = tk.Label(ventana, text="Texto a cifrar/descifrar:")
texto_label.pack()

# Campo de entrada del texto
texto_entry = tk.Entry(ventana)
texto_entry.pack()

# Etiqueta del resultado
resultado_label = tk.Label(ventana, text="Resultado:")
resultado_label.pack()

# Campo de entrada del resultado
resultado_entry = tk.Entry(ventana)
resultado_entry.pack()

# Botones para cifrar y descifrar
cifrar_button = tk.Button(ventana, text="Cifrar", command=cifrar)
descifrar_button = tk.Button(ventana, text="Descifrar", command=descifrar)
cifrar_button.pack()
descifrar_button.pack()

ventana.mainloop()
