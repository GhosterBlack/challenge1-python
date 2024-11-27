import re
import getpass
import bcrypt
from datetime import datetime

# Definición de los menús, que se usan más adelante en las funciones principales.
MENU_PRINCIPAL = """
Menu principal
1. Agregar experimento
2. Ver experimentos
3. Análisis de resultados
4. Generar informe
5. Configuración
6. Cerrar sesión
7. Salir
"""

MENU_AGREGAR_EXPERIMENTO = """
--- Menú Agregar Experimento ---
1. Ingresar Nombre del Experimento
2. ¿Ya realizó el experimento?
3. Guardar Experimento
4. Cancelar
"""

MENU_VER_EXPERIMENTOS = """
--- Menú Ver Experimentos ---
1. Ver Todos los Experimentos
2. Buscar Experimento
3. Ordenar Experimentos
4. Filtrar por Tipo de Experimento
5. Volver al Menú Principal
"""

MENU_ANALISIS_RESULTADOS = """
--- Menú Análisis de Resultados ---
1. Calcular Promedio
2. Calcular Máximo
3. Calcular Mínimo
4. Ver Análisis Completo
5. Volver al Menú Principal
"""

MENU_GENERAR_INFORME = """
--- Menú Generar Informe ---
1. Generar Informe Completo
2. Seleccionar Experimentos para Informe
3. Exportar Informe a TXT
4. Vista Previa del Informe
5. Volver al Menú Principal
"""

MENU_CONFIGURACION = """
--- Menú Configuración ---
1. Opciones de Exportación
2. Opciones de Seguridad
3. Restablecer Base de Datos
4. Ver Datos de Usuario
5. Volver al Menú Principal
"""

MENU_LOGIN = """
--- Menú de Login ---
1. Registrarse
2. Iniciar Sesión
3. Salir
"""

# Clase que maneja los datos principales del sistema (experimentos, usuarios, etc.).
class Datos:
    def __init__(self):
        # Lista de experimentos y un diccionario de usuarios.
        self.experimentos = []
        self.usuarios = {
            "EdIv": {
                "contraseña": self.hash_password("EdIv1025*"),
                "telefono": "3122003538",
                "nombreArchivo": "",
                "formatoArchivo": "",
                "clave": "EdIv1025*",
                "nombre": "Ed",
                "apellido": "Iv",
                "correo": "ediv1025@gmail.com"
            }
        }

    def agregar_experimento(self, experimento):
        """Agregar un nuevo experimento a la lista."""
        self.experimentos.append(experimento)

    def agregar_usuario(self, usuario, contraseña, telefono, nombreArchivo, formatoArchivo):
        """Agregar un nuevo usuario al sistema."""
        self.usuarios[usuario] = {"contraseña": contraseña, "telefono": telefono,
                                   "nombreArchivo": nombreArchivo, "formatoArchivo": formatoArchivo}

    def obtener_experimentos(self):
        """Obtener la lista de experimentos."""
        return self.experimentos

    def obtener_usuarios(self):
        """Obtener la lista de usuarios."""
        return self.usuarios

    def obtener_usuario(self, usuario):
        """Obtener los detalles de un usuario específico."""
        return self.usuarios.get(usuario)

    def ver_experimentos(self):
        """Mostrar todos los experimentos registrados."""
        for experimento in self.experimentos:
            experimento.ver_experimento()

    def hash_password(self, password):
        """Generar el hash de una contraseña usando bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def check_password(self, hashed, password):
        """Verificar si una contraseña coincide con su hash."""
        return bcrypt.checkpw(password.encode(), hashed)

    def validar_nombre_usuario(self, nombre):
        """Validar el formato del nombre del usuario (solo letras y espacio)."""
        return bool(re.match(r'^[A-Z][a-z]*(?: [A-Z][a-z]*)*$', nombre))

    def validar_telefono(self, telefono):
        """Validar el formato del número de teléfono (10 dígitos)."""
        return bool(re.match(r'^\d{10}$', telefono))

    def validar_contraseña(self, contraseña):
        """Validar el formato de la contraseña (mínimo 8 caracteres, letras, números y símbolo)."""
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[*_\-])[A-Za-z\d*_\-]{8,}$', contraseña))

# Clase que maneja los experimentos registrados en el sistema.
class Experimento:
    def __init__(self, nombre, fecha, tipo, resultados):
        # Atributos que definen un experimento.
        self.nombre = nombre
        self.fecha = fecha
        self.tipo = tipo
        self.resultados = resultados
        self.historial = []

    def editar_experimento(self, nuevo_nombre, nueva_fecha, nuevo_tipo, nuevos_resultados):
        """Editar los datos de un experimento y registrar los cambios en el historial."""
        self.historial.append({
            'nombre': self.nombre,
            'fecha': self.fecha,
            'tipo': self.tipo,
            'resultados': self.resultados
        })
        self.nombre = nuevo_nombre
        self.fecha = nueva_fecha
        self.tipo = nuevo_tipo
        self.resultados = nuevos_resultados

    def ver_experimento(self):
        """Mostrar los detalles de un experimento."""
        print(f"Nombre: {self.nombre}")
        print(f"Fecha: {self.fecha}")
        print(f"Tipo: {self.tipo}")
        print("Resultados:")
        for i, resultado in enumerate(self.resultados):
            print(f"{i + 1}. {resultado}")
        print("Historial de cambios:")
        for cambio in self.historial:
            print(cambio)

# Clase principal que gestiona los experimentos y su interacción con el usuario.
class AsistenteDeExperimentos:
    def __init__(self, datos):
        self.datos = datos

    def agregar_experimento(self):
        """Función para agregar un nuevo experimento."""
        nombre = input("Ingrese el nombre del experimento: ")
        tipo = input("Ingrese el tipo de experimento: ")
        fecha = ""
        resultados = []

        while True:
            print("¿Ya realizó el experimento? (si/no)")
            confirm_Realiz_Experimento = input().strip().lower()
            if confirm_Realiz_Experimento == "si":
                fecha = input("Ingrese la fecha en que realizó el experimento (YYYY-MM-DD): ")
                if not self.validar_fecha(fecha):
                    print("Fecha inválida. Intente de nuevo.")
                    continue
                datos_resultados = int(input("¿Cuántos datos desea almacenar en los resultados? "))
                for i in range(datos_resultados):
                    dato_resultado = input(f"Ingrese el resultado {i + 1}: ")
                    resultados.append(dato_resultado)
                break
            elif confirm_Realiz_Experimento == "no":
                fecha = input("Ingrese la fecha en que realizará su experimento (YYYY-MM-DD): ")
                if not self.validar_fecha(fecha):
                    print("Fecha inválida. Intente de nuevo.")
                    continue
                break
            else:
                print("Solo puede escoger: si o no")

        experimento = Experimento(nombre, fecha, tipo, resultados)
        self.datos.agregar_experimento(experimento)
        print("Experimento agregado exitosamente.")

    def validar_fecha(self, fecha):
        """Validar el formato de la fecha del experimento (YYYY-MM-DD)."""
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def ver_experimentos(self):
        """Mostrar todos los experimentos registrados."""
        self.datos.ver_experimentos()

    def menu_principal(self):
        """Mostrar el menú principal del asistente de experimentos."""
        while True:
            print(MENU_PRINCIPAL)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.agregar_experimento()
            elif opcion == '2':
                self.ver_experimentos()
            elif opcion == '3':
                self.analisis_de_resultados()
            elif opcion == '4':
                self.generar_informe()
            elif opcion == '5':
                self.configuracion()
            elif opcion == '6':
                print("Cerrando sesión...")
                return
            elif opcion == '7':
                print("Saliendo...")
                exit()
            else:
                print("Opción inválida. Intente de nuevo.")

    def analisis_de_resultados(self):
        """Mostrar el menú de análisis de resultados."""
        while True:
            print(MENU_ANALISIS_RESULTADOS)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.calcular_promedio()
            elif opcion == '2':
                self.calcular_maximo()
            elif opcion == '3':
                self.calcular_minimo()
            elif opcion == '4':
                self.ver_analisis_completo()
            elif opcion == '5':
                return
            else:
                print("Opción inválida. Intente de nuevo.")

    def calcular_promedio(self):
        """Calcular el promedio de los resultados de los experimentos."""
        print("Calculando el promedio...")

    def calcular_maximo(self):
        """Calcular el máximo de los resultados de los experimentos."""
        print("Calculando el máximo...")

    def calcular_minimo(self):
        """Calcular el mínimo de los resultados de los experimentos."""
        print("Calculando el mínimo...")

    def ver_analisis_completo(self):
        """Ver análisis completos de los experimentos."""
        print("Mostrando el análisis completo...")

    def generar_informe(self):
        """Mostrar el menú para generar el informe de los experimentos."""
        while True:
            print(MENU_GENERAR_INFORME)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.exportar_informe()
            elif opcion == '2':
                self.seleccionar_experimentos_para_informe()
            elif opcion == '3':
                self.exportar_informe_a_txt()
            elif opcion == '4':
                self.vista_previa_informe()
            elif opcion == '5':
                return
            else:
                print("Opción inválida. Intente de nuevo.")

    def exportar_informe(self):
        """Exportar el informe completo de experimentos."""
        print("Exportando el informe...")

    def seleccionar_experimentos_para_informe(self):
        """Seleccionar qué experimentos incluir en el informe."""
        print("Seleccionando experimentos para el informe...")

    def exportar_informe_a_txt(self):
        """Exportar el informe a un archivo .txt"""
        print("Informe exportado a archivo de texto...")

    def vista_previa_informe(self):
        """Mostrar una vista previa del informe."""
        print("Mostrando vista previa del informe...")

    def configuracion(self):
        """Mostrar el menú de configuración."""
        while True:
            print(MENU_CONFIGURACION)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.opciones_de_exportacion()
            elif opcion == '2':
                self.opciones_de_seguridad()
            elif opcion == '3':
                self.restablecer_base_de_datos()
            elif opcion == '4':
                self.ver_datos_usuario()
            elif opcion == '5':
                return
            else:
                print("Opción inválida. Intente de nuevo.")

    def opciones_de_exportacion(self):
        """Mostrar opciones de exportación de informes."""
        print("Configurando opciones de exportación...")

    def opciones_de_seguridad(self):
        """Mostrar opciones de seguridad."""
        print("Configurando opciones de seguridad...")

    def restablecer_base_de_datos(self):
        """Restablecer la base de datos."""
        print("Restableciendo base de datos...")

    def ver_datos_usuario(self):
        """Ver los datos del usuario."""
        print("Mostrando datos del usuario...")

# Crear los datos e iniciar la aplicación
datos = Datos()
asistente = AsistenteDeExperimentos(datos)
asistente.menu_principal()
