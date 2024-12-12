from pymongo import MongoClient
from bson.objectid import ObjectId

def conectar_db(uri="mongodb://localhost:27017", db_name="presupuesto"):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        return db
    except Exception as e:
        print("Error al conectar a la base de datos: " + str(e))
        return None

def registrar_articulo(db):
    nombre = input("Ingrese el nombre del artículo: ").strip()
    marca = input("Ingrese la marca del artículo: ").strip()  
    costo = float(input("Ingrese el costo: "))
    articulo = {
        "nombre": nombre,
        "marca": marca,  
        "costo": costo
    }
    try:
        resultado = db.articulos.insert_one(articulo)
        print("Artículo registrado con el ID: " + str(resultado.inserted_id))
    except Exception as e:
        print("Error al registrar artículo: " + str(e))

def buscar_articulo(db):
    ver_articulos(db)  
    articulo_id = input("Ingrese el ID del artículo a buscar: ").strip()  
    try:
        articulo = db.articulos.find_one({"_id": ObjectId(articulo_id)})
        if articulo:
            print("\nArtículo encontrado:")
            print(f"ID: {articulo['_id']} | Nombre: {articulo['nombre']} | Marca: {articulo['marca']} | Costo: ${articulo['costo']:.2f}")
        else:
            print("No se encontró un artículo con ese ID.\n")
    except Exception as e:
        print("Error al buscar artículo: " + str(e))

def editar_articulo(db):
    ver_articulos(db)
    articulo_id = input("Ingrese el ID del artículo a editar: ")
    try:
        articulo = db.articulos.find_one({"_id": ObjectId(articulo_id)})
        if articulo:
            print("Ingrese los datos a cambiar (en blanco para no cambiar):")
            nombre = input(f"Nombre [{articulo['nombre']}]: ") or articulo['nombre']
            marca = input(f"Marca [{articulo['marca']}]: ") or articulo['marca']  
            costo = input(f"Costo [{articulo['costo']}]: ") or articulo['costo']
            nuevos_datos = {
                "nombre": nombre,
                "marca": marca,  
                "costo": float(costo)
            }
            db.articulos.update_one({"_id": ObjectId(articulo_id)}, {"$set": nuevos_datos})
            print("Artículo actualizado exitosamente.\n")
        else:
            print("No existe un artículo con ese ID.\n")
    except Exception as e:
        print("Error al actualizar artículo: " + str(e))

def eliminar_articulo(db):
    ver_articulos(db)
    articulo_id = input("Ingrese el ID del artículo a eliminar: ")
    try:
        resultado = db.articulos.delete_one({"_id": ObjectId(articulo_id)})
        if resultado.deleted_count > 0:
            print("Artículo eliminado exitosamente.\n")
        else:
            print("No se encontró un artículo con ese ID.\n")
    except Exception as e:
        print("Error al eliminar artículo: " + str(e))

def ver_articulos(db):
    try:
        articulos = db.articulos.find()
        print("\nArtículos registrados:")
        for articulo in articulos:
            print(f"ID: {articulo['_id']} | Nombre: {articulo['nombre']} | Marca: {articulo['marca']} | Costo: ${articulo['costo']:.2f}")
        print()
    except Exception as e:
        print("Error al mostrar artículos: " + str(e))

def menu():
    print("\nSistema de Registro de Presupuesto")
    print("a) Registrar artículo")
    print("b) Buscar artículo")
    print("c) Editar artículo")
    print("d) Eliminar artículo")
    print("e) Ver todos los artículos")
    print("f) Salir")

def main():
    db = conectar_db()
    if db is None:
        return
    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "a":
            registrar_articulo(db)
        elif opcion == "b":
            buscar_articulo(db)
        elif opcion == "c":
            editar_articulo(db)
        elif opcion == "d":
            eliminar_articulo(db)
        elif opcion == "e":
            ver_articulos(db)
        elif opcion == "f":
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intente nuevamente.\n")

if __name__ == "__main__":
    main()