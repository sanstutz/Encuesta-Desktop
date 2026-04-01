from services.servicio_encuestas import ServicioEncuestas
from services.servicio_materias import ServicioMaterias
from ui.main_window import launch as launch_main_window


def main():
    servicio_encuestas = ServicioEncuestas()
    servicio_materias = ServicioMaterias(servicio_encuestas)

    launch_main_window(servicio_encuestas, servicio_materias)


if __name__ == "__main__":
    main()