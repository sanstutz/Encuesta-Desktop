from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QWidget

class VentanaCrearMateria(QMainWindow):
    def __init__(self, ventana_materias):
        super().__init__()
        self.ventana_materias = ventana_materias
        self.setWindowTitle("Crear materia")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        layout_codigo = QVBoxLayout()
        layout_codigo.setSpacing(10)
        label_codigo = QLabel("Código:")
        self.input_codigo = QLineEdit()
        layout_codigo.addWidget(label_codigo)
        layout_codigo.addWidget(self.input_codigo)
        layout.addLayout(layout_codigo)

        layout_nombre = QVBoxLayout()
        layout_nombre.setSpacing(10)
        label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        layout_nombre.addWidget(label_nombre)
        layout_nombre.addWidget(self.input_nombre)
        layout.addLayout(layout_nombre)

        layout_nombre_corto = QVBoxLayout()
        layout_nombre_corto.setSpacing(10)
        label_nombre_corto = QLabel("Nombre corto:")
        self.input_nombre_corto = QLineEdit()
        layout_nombre_corto.addWidget(label_nombre_corto)
        layout_nombre_corto.addWidget(self.input_nombre_corto)
        layout.addLayout(layout_nombre_corto)

        layout_nombre_sin_espacios = QVBoxLayout()
        layout_nombre_sin_espacios.setSpacing(10)
        label_nombre_sin_espacios = QLabel("Nombre sin espacios (opcional):")
        self.input_nombre_sin_espacios = QLineEdit()
        layout_nombre_sin_espacios.addWidget(label_nombre_sin_espacios)
        layout_nombre_sin_espacios.addWidget(self.input_nombre_sin_espacios)
        layout.addLayout(layout_nombre_sin_espacios)

        layout_año = QVBoxLayout()
        layout_año.setSpacing(10)
        label_año = QLabel("Año:")
        self.input_año = QSpinBox()
        self.input_año.setMinimum(1)
        layout_año.addWidget(label_año)
        layout_año.addWidget(self.input_año)
        layout.addLayout(layout_año)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.clicked.connect(self.guardar_materia)
        layout.addWidget(boton_guardar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def guardar_materia(self):
        codigo = self.input_codigo.text()
        nombre = self.input_nombre.text()
        nombre_corto = self.input_nombre_corto.text()
        nombre_sin_espacios = self.input_nombre_sin_espacios.text()
        año = self.input_año.value()
        self.ventana_materias.agregar_materia(codigo, nombre, nombre_corto, nombre_sin_espacios, año)
        self.close()

