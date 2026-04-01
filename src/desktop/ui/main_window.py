from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from ui.ventana_crear_encuesta import VentanaCrearEncuesta
from ui.ventana_encuesta import VentanaEncuesta

class MainWindow(QMainWindow):
    def __init__(self, servicio_encuestas, servicio_materias):
        super().__init__()
        self.setWindowTitle("Encuestas Estudio")
        self.setMinimumSize(1066, 600)
        self.showMaximized()

        self.servicio_encuestas = servicio_encuestas
        self.servicio_materias = servicio_materias

        self.ventana_crear_encuesta = None
        self.ventana_encuesta = None

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        boton_nueva_encuesta = QPushButton("Nueva Encuesta", self)
        boton_nueva_encuesta.clicked.connect(self.crear_nueva_encuesta)
        boton_nueva_encuesta.setFixedSize(200, 50)
        layout.addWidget(boton_nueva_encuesta)
        boton_abrir_encuesta = QPushButton("Abrir Encuesta", self)
        boton_abrir_encuesta.clicked.connect(self.abrir_encuesta)
        boton_abrir_encuesta.setFixedSize(200, 50)
        layout.addWidget(boton_abrir_encuesta)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def crear_nueva_encuesta(self):
        if (self.ventana_crear_encuesta is None):
            self.ventana_crear_encuesta = VentanaCrearEncuesta(self, self.servicio_encuestas)
            self.ventana_crear_encuesta.show()

    def finalizar_crear_encuesta(self, encuesta):
        self.ventana_crear_encuesta = None
        if (encuesta is not None):
            self.mostrar_encuesta(encuesta.id)

    def abrir_encuesta(self):
        print("Abrir encuesta")

    def mostrar_encuesta(self, id_encuesta):
        self.ventana_encuesta = VentanaEncuesta(self.servicio_encuestas, self.servicio_materias, id_encuesta)
        self.ventana_encuesta.show()
        self.close()

    def closeEvent(self, event):
        if (self.ventana_crear_encuesta is not None):
            self.ventana_crear_encuesta = None
        event.accept()


def launch(servicio_encuestas, servicio_materias):
    app = QApplication([])
    window = MainWindow(servicio_encuestas, servicio_materias)
    window.show()
    app.exec()
    return window