#contador_palabras.py
#Programa simple para contar palabras en un  textto ingresado por el usuario

def contar_palabras(texto):
    palabras = texto.split()
    return len(palabras)

if __name__ == "__main__":
    texto = input("Escribe una frase o párrafo: ")
    total = contar_palabras(texto)
    print(f"El texto tiene {total} palabras.")