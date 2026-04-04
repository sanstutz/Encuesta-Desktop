from services.servicio_encuestas import ServicioEncuestas
from services.servicio_materias import ServicioMaterias
from services.servicio_formulario import ServicioFormulario
from repositories.repositorio_encuestas import RepositorioEncuestas
from ui.main_window import launch as launch_main_window
from pathlib import Path

from entities.encuesta import Encuesta
from datetime import date


def main():
    # base_dir = Path(__file__).resolve().parent
    # save_path = base_dir / "data"


    save_path = Path("data")
    repositorio_encuestas = RepositorioEncuestas(save_path)

    servicio_encuestas = ServicioEncuestas(repositorio_encuestas)
    servicio_materias = ServicioMaterias(servicio_encuestas)

    launch_main_window(servicio_encuestas, servicio_materias)


if __name__ == "__main__":
    main()