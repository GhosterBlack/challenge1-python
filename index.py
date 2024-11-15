# trabaja aqui edi
usuario = []
contraseña = []
acceso = ['Iniciar sesión', 'Registrarse']

print("Bienvenido a nuestro Asistente de Laboratorio")
def menuUsuario():
    print("\nAcceso:")
    for i, opcion_Acceso in enumerate(acceso):
        print(f"{i+1}: {acceso}")

    acceso_Seleccionado = int(input())
    if acceso_Seleccionado > 0 and acceso_Seleccionado <= len(acceso):
        opcion_Acceso = acceso[acceso_Seleccionado-1]