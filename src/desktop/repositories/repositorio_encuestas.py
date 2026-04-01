from entities.encuesta import Encuesta
import json
import os

class RepositorioEncuestas:
    def __init__(self, save_path: str):
        self.save_path = os.fspath(save_path)
        os.makedirs(self.save_path, exist_ok=True)

    def guardar_encuesta(self, encuesta: Encuesta):
        path = os.path.join(self.save_path, f"encuesta_{encuesta.id}.json")
        with open(path, "w") as file:
            json.dump(encuesta.to_dict(), file, ensure_ascii=False, indent=2)

    def cargar_encuesta(self, id: int) -> Encuesta:
        path = os.path.join(self.save_path, f"encuesta_{id}.json")
        if not os.path.exists(path):
            raise Exception(f"No se encontró la encuesta con id {id}")
        with open(path, "r") as file:
            data = json.load(file)
            return Encuesta.from_dict(data)
        
    def cargar_encuestas(self):
        encuestas = []
        for filename in os.listdir(self.save_path):
            if filename.startswith("encuesta_") and filename.endswith(".json"):
                with open(os.path.join(self.save_path, filename), "r") as file:
                    data = json.load(file)
                    encuestas.append(Encuesta.from_dict(data))
        return encuestas
