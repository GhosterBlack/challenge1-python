from datetime import datetime

# Declaramos una clase datos que sera usada por la funcion principal para controlar el archivo donde se guardan los datos
class Datos:
    usuarios = []
    experimentos = []
    
    def agregarUsuario (self, correo: str, clave: str):
        usuario = {
            'correo': correo,
            'clave': clave
        }
        self.usuarios.append(usuario)
        print("*** Usuario agregado con exito ***")

    def agregarExperimento (self, nombre:str, fecha:str, tipo, resultado):
        try:
            experimento = {
                'nombre': nombre,
                'fecha': datetime.strptime(fecha, "%d/%m/%Y"),
                'tipo': tipo,
                'resultado': resultado
            }
            self.experimentos.append(experimento)
            print("*** Experimento cargado con exito ***")
        except ValueError:
            print("! Datos ingresados no validos")
        
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
                text += f"\n{usuario['correo']}@\n{usuario['clave']}"
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
                        'clave': usuario_list[1]
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
                            'fecha': datetime.strptime(experimento_list[1], "%d/%m/%Y"),
                            'tipo': experimento_list[2],
                            'resultados': experimento_list[3]
                        }
                        self.experimentos.append(experimento)


def main ():
    datos = Datos()
    nombre = ""
    clave = ""

    print(datos.usuarios)

    print("Por favor escriba su correo")
    nombre = input("Correo: ")
    print("Por favor dijite su clave")
    clave = input("Clave: ")

    datos.agregarUsuario(nombre, clave)
    datos.guardar()


if __name__ == "__main__":
    main()
