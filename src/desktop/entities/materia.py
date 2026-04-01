class Materia:
    def __init__(self, codigo: str, nombre: str, nombre_corto: str, nombre_sin_espacios: str, año: int):
        self.codigo = codigo
        self.nombre = nombre
        self.nombre_corto = nombre_corto
        self.año = año
        if (not nombre_sin_espacios):
            self.nombre_sin_espacios = nombre_corto.strip(" ").replace(" ", "_")
        else:
            self.nombre_sin_espacios = nombre_sin_espacios