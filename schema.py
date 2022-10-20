# Creación de una lista de instrucciones a ejecutar en la base de datos.
instructions = [
    'DROP TABLE IF EXISTS empleados;',
    """
        CREATE TABLE empleados (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL,
            foto VARCHAR(5000) NOT NULL
        )
    """
]