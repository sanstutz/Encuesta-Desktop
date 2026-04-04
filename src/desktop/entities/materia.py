class Materia:
    def __init__(self, codigo: str, nombre: str, tipo: int, nombre_corto: str, nombre_sin_espacios: str, año: int, especialidades: list[int] = []):
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.tipo: int = tipo
        self.nombre_corto: str = nombre_corto
        self.año: int = año
        self.especialidades: list[int] = especialidades
        if (not nombre_sin_espacios):
            self.nombre_sin_espacios: str = nombre_corto.strip(" ").replace(" ", "_")
        else:
            self.nombre_sin_espacios: str = nombre_sin_espacios

    def añadir_especialidad(self, especialidad_id: int):
        if especialidad_id not in self.especialidades:
            self.especialidades.append(especialidad_id)

    def eliminar_especialidad(self, especialidad_id: int):
        if especialidad_id in self.especialidades:
            self.especialidades.remove(especialidad_id)

    def tipo_str(self) -> str:
        if self.tipo == 0:
            return "Teorico/Practico"
        elif self.tipo == 1:
            return "Teorico"
        elif self.tipo == 2:
            return "Practico"
        else:
            return "Desconocido"

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "nombre_corto": self.nombre_corto,
            "nombre_sin_espacios": self.nombre_sin_espacios,
            "año": self.año,
            "especialidades": self.especialidades,
        }

    @staticmethod
    def from_dict(data: dict):
        return Materia(
            data["codigo"],
            data["nombre"],
            data["tipo"],
            data["nombre_corto"],
            data.get("nombre_sin_espacios"),
            data["año"],
            data.get("especialidades", []),
        )