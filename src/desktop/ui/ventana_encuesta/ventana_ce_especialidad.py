from PyQt6.QtWidgets import QMainWindow, QLabel, QSpinBox, QLineEdit, QPushButton, QVBoxLayout, QWidget

class VentanaCrearEditarEspecialidad(QMainWindow):
    def __init__(self, callback, esCrear: bool, nombre_especialidad: str = "", años: int = 1):
        super().__init__()
        self.crear_callback = callback
        nombre_ventana = "Crear especialidad" if esCrear else "Editar especialidad"
        self.setWindowTitle(nombre_ventana)
        self.setMinimumSize(400, 0)

        layout = QVBoxLayout()
        label_nombre = QLabel("Nombre de la especialidad:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setText(nombre_especialidad)
        label_años = QLabel("Duración (años):")
        self.input_años = QSpinBox()
        self.input_años.setRange(1, 10)
        self.input_años.setValue(años)
        boton_crear = QPushButton("Crear" if esCrear else "Editar")
        boton_crear.clicked.connect(self.guardar_especialidad)

        layout.addWidget(label_nombre)
        layout.addWidget(self.input_nombre)
        layout.addWidget(label_años)
        layout.addWidget(self.input_años)
        layout.addWidget(boton_crear)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def guardar_especialidad(self):
        nombre = self.input_nombre.text()
        años = self.input_años.value()
        self.crear_callback(nombre, años)