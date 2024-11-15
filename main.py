from datetime import datetime
# constantes
SELECT = "Seleccione una opcion: "
BADOPTION = "Opcion incorrecta"
BADINFOREQUEST = "! Datos ingresados no validos"

# Declaramos una clase datos que sera usada por la funcion principal para controlar el archivo donde se guardan los datos
class Datos:
    usuarios = []
    experimentos = []
    
    def agregarUsuario (self, correo: str, clave: str, nombreArchivo: str, formatoArchivo: str, telefono: str, fecha: str, nombre: str, apellido: str):
        try: 
            usuario = {
                'correo': correo,
                'clave': clave,
                'nombreArchivo': nombreArchivo,
                'formatoArchivo': formatoArchivo,
                'telefono': telefono,
                'fecha': datetime(fecha, "%d/%m/%Y"),
                'nombre': nombre,
                'apellido': apellido
            }
            self.usuarios.append(usuario)
            print("*** Usuario agregado con exito ***")
        except ValueError:
            print(BADINFOREQUEST)

    def agregarExperimento (self, nombre:str, fecha:str, tipo, resultado):
        try:
            experimento = {
                'nombre': nombre,
                'fecha': fecha,
                'tipo': tipo,
                'resultado': resultado
            }
            self.experimentos.append(experimento)
            print("*** Experimento cargado con exito ***")
        except ValueError:
            print(BADINFOREQUEST)
        
    # el metodo guardar nos permite guardar la informacion ya establecida
    def guardar (self): 
        if len(self.usuarios) == 0 and len(self.experimentos) == 0:
            # evitamos que el programa siga en ejecucion si no hay nada que guardar
            return
        
        # definimos la variable text como una cadena vacia para modificarla posteriormente
        text = ""
        #escribimos la informacion de los usuarios
        if len(self.usuarios) > 0:
            for i in range(len(self.usuarios)):
                usuario = self.usuarios[i]
                text += f"\n{usuario['correo']}@\n{usuario['clave']}@\n{usuario['nombreArchivo']}@\n{usuario['formatoArchivo']}"
                text += f"\n@{usuario['telefono']}\n@{usuario['fecha']}\n@{usuario['nombre']}\n@{usuario['apellido']}"
                if i < len(self.usuarios)-1:
                    text += "\n----"
        else:
            #si no hay usuarios se escribe uno por defecto
            text += "usuario@\n0000"
        # solo si hay experimentos se agrega informacion
        if len(self.experimentos) > 0:
            text += "\n####"
            for i in range(len(self.experimentos)):
                experimento = self.experimentos[i]
                text += f"\n{experimento['nombre']}@\n{experimento['fecha']}@\n{experimento['tipo']}@\n{experimento['resultados']}"
        # abrimos el archivo donde estan los datos
        with open("datos.txt", "w") as datos:
            #escribimos la informacion
            datos.write(text)
            



# declaramos la funcion iniciadora
    def __init__(self) -> None:
        # abrimos el archivo de datos
        with open("datos.txt", "r") as datos:
            text: str = datos.read()
            text = text.replace("\n", "")
            # solo ejecutamos el codigo si el texto no esta vacio
            if text != "":
                #diferenciamos las tablas de contenido con el separador dispuesto para ellas
                tablasContenido = text.split("####")
                # obtenemos los usuarios como primer item de las tablas de contenido y lo separamos
                usuarios = tablasContenido[0].split("----")
                for i in range(len(usuarios)):
                    # separamos los datos de cada usuario para formatearlo
                    usuario_list = usuarios[i].split("@")
                    usuario = {
                        'correo': usuario_list[0],
                        'clave': usuario_list[1],
                        'nombreArchivo': usuario_list[2],
                        'formatoArchivo': usuario_list[3],
                        'telefono': usuario_list[4],
                        'fecha': usuario_list[5],
                        'nombre': usuario_list[6],
                        'apellido': usuario_list[7]
                    }
                    if usuario['correo'] != "usuario":
                        self.usuarios.append(usuario)
                
                if len(tablasContenido) > 1:
                    # hacemos lo mismo con los experimentos
                    experimentos = tablasContenido[1].split("----")
                    for i in range(len(experimentos)):
                        # y lo mismo con experimentos
                        experimento_list = experimentos[i].split("@")
                        experimento = {
                            'nombre': experimento_list[0],
                            'fecha': experimento_list[1],
                            'tipo': experimento_list[2],
                            'resultados': experimento_list[3]
                        }
                        self.experimentos.append(experimento)


def configuracion ():
    def optionExport ():
        pass
    def optionSecure ():
        pass
    def dataBaseRestore ():
        pass
    while True:
        print("\n-------------------")
        print("** Menu de configuracion **")
        print("1. Opciones de exportacion")
        print("2. Opciones de seguridad")
        print("3. Restablecer base de datos")
        print("4. Volver al menu principal")
        print("-------------------")
        respuesta = input(SELECT)
        if respuesta == "1":
            optionExport()
        elif respuesta == "2":
            optionSecure()
        elif respuesta == "3":
            dataBaseRestore()
        elif respuesta == "4":
            break
        else:
            print(BADOPTION)
    
    return

# trabaja aqui edi


def menuUsuario():
    # vamos a abrir la base de datos
    datos = Datos()
    # viejo a partir de ahora todos los print dentro de funciones
    acceso = ['Iniciar sesión', 'Registrarse']
    # aqui van a estar todos los usuarios
    usuarios = datos.usuarios
    print("Bienvenido a nuestro Asistente de Laboratorio")
    print("\nAcceso:")
    for i, opcion_Acceso in enumerate(acceso):
        print(f"{i+1}: {opcion_Acceso}")

    acceso_Seleccionado = int(input())
    if acceso_Seleccionado > 0 and acceso_Seleccionado <= len(acceso):
        opcion_Acceso = acceso[acceso_Seleccionado-1]

def main ():
    while True:
        print("--------------------")
        print("Menu principal")
        print("1. Configuracion")
        print("2. Salir")
        print("--------------------")
        respuesta = input(SELECT)
        if respuesta == "1":
            configuracion()
        elif respuesta == "2":
            print("Saliendo del programa...")
            break
        else:
            print(BADOPTION)


if __name__ == "__main__":
    menuUsuario()
