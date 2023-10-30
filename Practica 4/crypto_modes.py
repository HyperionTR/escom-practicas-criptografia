from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from tkinter import messagebox
from PIL import Image, ImageTk

def cifrado_des( clave, iv, nombre_archivo, selected_mode ):
	try:

		# Validar que se haya ingresado una clave de 8 bytes
		if len(clave) != 8:
			raise ValueError("La clave debe tener 8 bytes")

		if len(iv) != 8 and selected_mode != DES.MODE_ECB:
			raise ValueError("El vector de inicialización debe tener 8 bytes")

		if nombre_archivo:
				clave_bytes = bytes(clave, 'utf-8')
				iv = bytes(iv, 'utf-8')
				cabecera_bmp:bytes = None

				if selected_mode in [DES.MODE_ECB, DES.MODE_CBC]:
					# Modos que funcionan con datos en bloques
					cipher = DES.new(clave_bytes, selected_mode)

					# Abrimos el archivo BMP y guardamos la cabecera y los datos de imágen
					with open(nombre_archivo, 'rb') as file:
						datos = file.read()
						cabecera_bmp = datos[:54] # 0-53
						datos_bmp = datos[54:] # 54-EOF
						datos_cifrados = cipher.encrypt(pad(datos_bmp, 8), iv=iv) if selected_mode == DES.MODE_CBC else\
										 cipher.encrypt(pad(datos_bmp, 8))

				elif selected_mode in [DES.MODE_CFB, DES.MODE_OFB]:
	 				# Modos que funcionan con flujo de datos
					cipher = DES.new(clave_bytes, selected_mode, iv=iv)

					# Abrimos el archivo BMP y guardamos la cabecera y los datos de imágen
					with open(nombre_archivo, 'rb') as file:
						datos = file.read()
						cabecera_bmp = datos[:54] # 0-53
						datos_bmp = datos[54:] # 54-EOF
						datos_cifrados = cipher.encrypt(datos_bmp)

				# Determinar el modo en formato de texto
				modo_texto = "ECB" if selected_mode == DES.MODE_ECB else \
							 "CBC" if selected_mode == DES.MODE_CBC else \
							 "CFB" if selected_mode == DES.MODE_CFB else \
							 "OFB" if selected_mode == DES.MODE_OFB else ""

				# Guardar los datos cifrados en un archivo con el nombre modificado
				archivo_salida = nombre_archivo.replace(".bmp", f"_e{modo_texto}.bmp")
				with open(archivo_salida, 'wb') as output_file:
					output_file.write(cabecera_bmp)
					output_file.write(datos_cifrados)

				messagebox.showinfo("Información", f"Imagen cifrada guardada en {archivo_salida}")

				return datos_cifrados
	except Exception as e:
		messagebox.showerror("Error", str(e))


def decifrado_des( clave, iv, nombre_archivo, selected_mode ):
	try:

		# Validar que se haya ingresado una clave de 8 bytes
		if len(clave) != 8:
			raise ValueError("La clave debe tener 8 bytes")

		if len(iv) != 8 and selected_mode != DES.MODE_ECB:
			raise ValueError("El vector de inicialización debe tener 8 bytes")

		if nombre_archivo:
			clave_bytes = bytes(clave, 'utf-8')
			iv = bytes(iv, 'utf-8')
			cabecera_bmp:bytes = None

			if selected_mode in [DES.MODE_ECB, DES.MODE_CBC]:
				# Modos que funcionan con datos en bloques
				cipher = DES.new(clave_bytes, selected_mode)

				# Abrir archivo de imágen cifrada y descifrar, manteniendo intacta la cabecera
				with open(nombre_archivo, 'rb') as file:
					datos_cifrados = file.read()
					cabecera_bmp = datos_cifrados[:54] # 0-53
					datos_cifrados = datos_cifrados[54:] # 54-EOF
					datos_descifrados = unpad(cipher.decrypt(datos_cifrados), 8, iv=iv) if selected_mode == DES.MODE_CBC else\
         								unpad(cipher.decrypt(datos_cifrados), 8)

			elif selected_mode in [DES.MODE_CFB, DES.MODE_OFB]:
				# Modos que funcionan con flujo de datos
				cipher = DES.new(clave_bytes, selected_mode, iv=iv)

				# Abrir archivo de imágen cifrada y descifrar, manteniendo intacta la cabecera
				with open(nombre_archivo, 'rb') as file:
					datos_cifrados = file.read()
					cabecera_bmp = datos_cifrados[:54] # 0-53
					datos_cifrados = datos_cifrados[54:] # 54-EOF
					datos_descifrados = cipher.decrypt(datos_cifrados)

			# Determinar el modo en formato de texto
			modo_texto = "ECB" if selected_mode == DES.MODE_ECB else \
						 "CBC" if selected_mode == DES.MODE_CBC else \
						 "CFB" if selected_mode == DES.MODE_CFB else \
						 "OFB" if selected_mode == DES.MODE_OFB else ""

			# Guardar los datos descifrados en un archivo con el nombre modificado
			archivo_salida = nombre_archivo.replace(f".bmp", f"_d{modo_texto}.bmp")
			with open(archivo_salida, 'wb') as output_file:
				output_file.write(cabecera_bmp)
				output_file.write(datos_descifrados)

			messagebox.showinfo("Información", f"Imagen descifrada guardada en {archivo_salida}")

			return datos_descifrados
	except Exception as e:
		messagebox.showerror("Error", str(e))
