from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

from tkinter import messagebox

def cifrado_des( key: str | bytes, iv: str | bytes, plain_data: bytes, selected_mode ):
	try:
		# Validar que se haya ingresado una clave de 8 bytes
		if len(key) != 8:
			raise ValueError("La clave debe tener 8 bytes")

		if len(iv) != 8 and selected_mode != DES.MODE_ECB:
			raise ValueError("El vector de inicialización debe tener 8 bytes")

		clave_bytes = bytes(key, 'utf-8')
		iv = bytes(iv, 'utf-8')
		datos_cifrados:bytes = None

		# No se hace distinción entre algoritmos con y sin bloques, ya que se elimina el padding por completo del programa
		cipher = DES.new(clave_bytes, selected_mode, iv=iv) if selected_mode != DES.MODE_ECB else\
				 DES.new(clave_bytes, selected_mode)
		datos_cifrados = cipher.encrypt(plain_data) 

		return datos_cifrados
	except Exception as e:
		messagebox.showerror("Error", str(e))


def decifrado_des( key: str | bytes, iv: str | bytes, encrypted_data: bytes, selected_mode ):
	try:
		# Validar que se haya ingresado una clave de 8 bytes
		if len(key) != 8:
			raise ValueError("La clave debe tener 8 bytes")

		if len(iv) != 8 and selected_mode != DES.MODE_ECB:
			raise ValueError("El vector de inicialización debe tener 8 bytes")

		clave_bytes = bytes(key, 'utf-8')
		iv = bytes(iv, 'utf-8')
		datos_descifrados:bytes = None

		# No se hace distinción entre algoritmos con y sin bloques, ya que se elimina el padding por completo del programa
		cipher = DES.new(clave_bytes, selected_mode, iv=iv) if selected_mode != DES.MODE_ECB else\
					DES.new(clave_bytes, selected_mode)
		datos_descifrados = cipher.decrypt(encrypted_data)

		return datos_descifrados
	except Exception as e:
		messagebox.showerror("Error", str(e))
