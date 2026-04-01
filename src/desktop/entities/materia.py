class Materia:
    def __init__(self, codigo: str, nombre: str, tipo: int, nombre_corto: str, nombre_sin_espacios: str, año: int):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.nombre_corto = nombre_corto
        self.año = año
        if (not nombre_sin_espacios):
            self.nombre_sin_espacios = nombre_corto.strip(" ").replace(" ", "_")
        else:
            self.nombre_sin_espacios = nombre_sin_espacios

    def tipo_str(self) -> str:
        if self.tipo == 0:
            return "Teorico/Practico"
        elif self.tipo == 1:
            return "Teorico"
        elif self.tipo == 2:
            return "Practico"
        else:
            return "Desconocido"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "nombre_corto": self.nombre_corto,
            "nombre_sin_espacios": self.nombre_sin_espacios,
            "año": self.año,
        }

    @staticmethod
    def from_dict(data):
        return Materia(
            data["codigo"],
            data["nombre"],
            data["tipo"],
            data["nombre_corto"],
            data.get("nombre_sin_espacios"),
            data["año"],
        )