from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QWidget
from services.servicio_encuestas import ServicioEncuestas
from ui.error_dialog import ErrorDialog

class VentanaCrearEncuesta(QMainWindow):
    def __init__(self, main_window, servicio_encuestas: ServicioEncuestas):
        super().__init__()
        self.main_window = main_window
        self.servicio_encuestas = servicio_encuestas

        self.setWindowTitle("Nueva Encuesta")
        self.setMinimumSize(400, 200)
        self.move((1980-400) // 2, (1080-200) // 2)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label_nombre = QLabel("Nombre de la encuesta:")
        layout.addWidget(label_nombre)

        self.input_nombre = QLineEdit()
        layout.addWidget(self.input_nombre)

        label_fecha_inicio = QLabel("Fecha de inicio:")
        self.input_fecha_inicio = QDateEdit()
        self.input_fecha_inicio.setDisplayFormat("dd/MM/yyyy")
        self.input_fecha_inicio.setDate(QDate.currentDate())
        layout.addWidget(label_fecha_inicio)
        layout.addWidget(self.input_fecha_inicio)

        label_fecha_fin = QLabel("Fecha de fin:")
        self.input_fecha_fin = QDateEdit()
        self.input_fecha_fin.setDisplayFormat("dd/MM/yyyy")
        self.input_fecha_fin.setDate(QDate.currentDate())
        layout.addWidget(label_fecha_fin)
        layout.addWidget(self.input_fecha_fin)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.clicked.connect(self.guardar_encuesta)
        layout.addWidget(boton_guardar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def guardar_encuesta(self):
        nombre = self.input_nombre.text()
        fecha_inicio = self.input_fecha_inicio.date().toPyDate()
        fecha_fin = self.input_fecha_fin.date().toPyDate()
        try:
            encuesta = self.servicio_encuestas.crear_encuesta(nombre, fecha_inicio, fecha_fin)
            self.main_window.finalizar_crear_encuesta(encuesta)
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al crear la encuesta: {str(e)}")
            error_dialog.exec()
            self.main_window.finalizar_crear_encuesta(None)

    def closeEvent(self, event):
        self.main_window.finalizar_crear_encuesta(None)
        event.accept()

    