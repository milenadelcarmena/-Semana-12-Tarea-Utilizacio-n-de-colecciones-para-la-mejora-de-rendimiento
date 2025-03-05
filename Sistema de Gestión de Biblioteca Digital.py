class Libro:
    """
    Representa un libro con atributos como título, autor, categoría y ISBN.
    Utiliza una tupla para almacenar el autor y el título, ya que estos no cambiarán una vez creados.
    """
    def __init__(self, titulo, autor, categoria, isbn):
        # Almacenar título y autor como tupla para mantenerlos inmutables
        self.info_inmutable = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn
        self.prestado = False  # Indicador de si el libro está prestado

    def __str__(self):
        return f"Título: {self.info_inmutable[0]}, Autor: {self.info_inmutable[1]}, Categoría: {self.categoria}, ISBN: {self.isbn}"


class Usuario:
    """
    Representa a un usuario de la biblioteca con atributos como nombre, ID de usuario (único) y una lista de libros actualmente prestados.
    """
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista para almacenar los libros prestados

    def __str__(self):
        return f"Nombre: {self.nombre}, ID: {self.id_usuario}"


class Biblioteca:
    """
    Gestiona las colecciones de libros, usuarios y préstamos.
    Utiliza un diccionario para almacenar los libros disponibles, con el ISBN como clave y el objeto Libro como valor.
    Usa un conjunto para manejar los IDs de usuarios únicos.
    """
    def __init__(self):
        self.libros = {}  # Diccionario para almacenar libros por ISBN
        self.usuarios = set()  # Conjunto para IDs de usuarios únicos
        self.usuarios_registrados = {}  # Diccionario para almacenar usuarios registrados por ID

    def agregar_libro(self, libro):
        """
        Añade un libro a la biblioteca.
        """
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
            print(f"Libro agregado: {libro}")
        else:
            print("El libro ya existe en la biblioteca.")

    def quitar_libro(self, isbn):
        """
        Quita un libro de la biblioteca.
        """
        if isbn in self.libros:
            del self.libros[isbn]
            print(f"Libro quitado con ISBN: {isbn}")
        else:
            print("El libro no existe en la biblioteca.")

    def registrar_usuario(self, usuario):
        """
        Registra un nuevo usuario en la biblioteca.
        """
        if usuario.id_usuario not in self.usuarios:
            self.usuarios.add(usuario.id_usuario)
            self.usuarios_registrados[usuario.id_usuario] = usuario
            print(f"Usuario registrado: {usuario}")
        else:
            print("El ID de usuario ya está registrado.")

    def dar_baja_usuario(self, id_usuario):
        """
        Da de baja a un usuario existente.
        """
        if id_usuario in self.usuarios:
            self.usuarios.remove(id_usuario)
            del self.usuarios_registrados[id_usuario]
            print(f"Usuario dado de baja con ID: {id_usuario}")
        else:
            print("El ID de usuario no está registrado.")

    def prestar_libro(self, isbn, id_usuario):
        """
        Presta un libro a un usuario.
        """
        if isbn in self.libros and id_usuario in self.usuarios:
            libro = self.libros[isbn]
            if not libro.prestado:
                libro.prestado = True
                usuario = self.usuarios_registrados[id_usuario]
                usuario.libros_prestados.append(libro)
                print(f"Libro prestado a {usuario.nombre}: {libro}")
            else:
                print("El libro ya está prestado.")
        else:
            print("El libro o el usuario no están disponibles.")

    def devolver_libro(self, isbn, id_usuario):
        """
        Devuelve un libro prestado por un usuario.
        """
        if isbn in self.libros and id_usuario in self.usuarios:
            libro = self.libros[isbn]
            usuario = self.usuarios_registrados[id_usuario]
            if libro in usuario.libros_prestados:
                libro.prestado = False
                usuario.libros_prestados.remove(libro)
                print(f"Libro devuelto: {libro}")
            else:
                print("El usuario no tiene este libro prestado.")
        else:
            print("El libro o el usuario no están disponibles.")

    def buscar_libros(self, criterio, valor):
        """
        Busca libros por título, autor o categoría.
        """
        resultados = []
        for libro in self.libros.values():
            if criterio == "titulo" and valor.lower() in libro.info_inmutable[0].lower():
                resultados.append(libro)
            elif criterio == "autor" and valor.lower() in libro.info_inmutable[1].lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor.lower() == libro.categoria.lower():
                resultados.append(libro)
        return resultados

    def listar_libros_prestados(self, id_usuario):
        """
        Muestra una lista de todos los libros actualmente prestados a un usuario.
        """
        if id_usuario in self.usuarios:
            usuario = self.usuarios_registrados[id_usuario]
            return usuario.libros_prestados
        else:
            print("El ID de usuario no está registrado.")
            return []


# Prueba del sistema
if __name__ == "__main__":
    biblioteca = Biblioteca()

    # Crear libros
    libro1 = Libro("El Señor de los Anillos", "J.R.R. Tolkien", "Fantasía", "978-84-01-01303-3")
    libro2 = Libro("Harry Potter y la Piedra Filosofal", "J.K. Rowling", "Fantasía", "978-84-01-01304-0")

    # Agregar libros a la biblioteca
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)

    # Crear usuarios
    usuario1 = Usuario("Rogelio Alvarado", "U001")
    usuario2 = Usuario("Mariana Leiva", "U002")

    # Registrar usuarios
    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)

    # Prestar libros
    biblioteca.prestar_libro(libro1.isbn, usuario1.id_usuario)
    biblioteca.prestar_libro(libro2.isbn, usuario2.id_usuario)

    # Listar libros prestados
    print("\nLibros prestados a Rogelio Alvarado:")
    for libro in biblioteca.listar_libros_prestados(usuario1.id_usuario):
        print(libro)

    # Buscar libros
    print("\nBuscar libros por autor 'J.K. Rowling':")
    resultados = biblioteca.buscar_libros("autor", "J.K. Rowling")
    for libro in resultados:
        print(libro)

    # Devolver libros
    biblioteca.devolver_libro(libro1.isbn, usuario1.id_usuario)

    # Dar de baja un usuario
    biblioteca.dar_baja_usuario(usuario2.id_usuario)
