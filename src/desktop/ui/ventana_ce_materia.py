from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QWidget

class VentanaCrearEditarMateria(QMainWindow):
    def __init__(self, ventana_materias, es_crear: bool, param: int, codigo: str = "", nombre: str = "", tipo: int = 0, nombre_corto: str = "", nombre_sin_espacios: str = "", año: int = 1):
        super().__init__()
        self.ventana_materias = ventana_materias
        self.param = param
        nombre_ventana = "Crear materia" if es_crear else "Editar materia"
        self.setWindowTitle(nombre_ventana)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        layout_codigo = QVBoxLayout()
        layout_codigo.setSpacing(10)
        label_codigo = QLabel("Código:")
        self.input_codigo = QLineEdit()
        self.input_codigo.setText(codigo)
        layout_codigo.addWidget(label_codigo)
        layout_codigo.addWidget(self.input_codigo)
        layout.addLayout(layout_codigo)

        layout_nombre = QVBoxLayout()
        layout_nombre.setSpacing(10)
        label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setText(nombre)
        layout_nombre.addWidget(label_nombre)
        layout_nombre.addWidget(self.input_nombre)
        layout.addLayout(layout_nombre)

        layout_tipo = QVBoxLayout()
        layout_tipo.setSpacing(10)
        label_tipo = QLabel("Tipo:")
        self.input_tipo = QComboBox()
        self.input_tipo.addItems(["Teorico/Practico", "Teorico", "Practico"])
        if es_crear:
            self.input_tipo.setCurrentIndex(0)
        else:
            self.input_tipo.setCurrentIndex(tipo)
        layout_tipo.addWidget(label_tipo)
        layout_tipo.addWidget(self.input_tipo)
        layout.addLayout(layout_tipo)

        layout_nombre_corto = QVBoxLayout()
        layout_nombre_corto.setSpacing(10)
        label_nombre_corto = QLabel("Nombre corto:")
        self.input_nombre_corto = QLineEdit()
        self.input_nombre_corto.setText(nombre_corto)
        layout_nombre_corto.addWidget(label_nombre_corto)
        layout_nombre_corto.addWidget(self.input_nombre_corto)
        layout.addLayout(layout_nombre_corto)

        layout_nombre_sin_espacios = QVBoxLayout()
        layout_nombre_sin_espacios.setSpacing(10)
        label_nombre_sin_espacios = QLabel("Nombre sin espacios (opcional):")
        self.input_nombre_sin_espacios = QLineEdit()
        self.input_nombre_sin_espacios.setText(nombre_sin_espacios)
        layout_nombre_sin_espacios.addWidget(label_nombre_sin_espacios)
        layout_nombre_sin_espacios.addWidget(self.input_nombre_sin_espacios)
        layout.addLayout(layout_nombre_sin_espacios)

        layout_año = QVBoxLayout()
        layout_año.setSpacing(10)
        label_año = QLabel("Año:")
        self.input_año = QSpinBox()
        self.input_año.setMinimum(1)
        self.input_año.setValue(año)
        layout_año.addWidget(label_año)
        layout_año.addWidget(self.input_año)
        layout.addLayout(layout_año)

        nombre_boton = "Crear" if es_crear else "Guardar"
        boton_guardar = QPushButton(nombre_boton)
        boton_guardar.clicked.connect(self.crear_materia if es_crear else self.editar_materia)
        layout.addWidget(boton_guardar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def crear_materia(self):
        codigo = self.input_codigo.text()
        nombre = self.input_nombre.text()
        tipo = self.input_tipo.currentText()
        nombre_corto = self.input_nombre_corto.text()
        nombre_sin_espacios = self.input_nombre_sin_espacios.text()
        año = self.input_año.value()
        self.ventana_materias.agregar_materia(codigo, nombre, tipo, nombre_corto, nombre_sin_espacios, año, self.param)

    def editar_materia(self):
        codigo = self.input_codigo.text()
        nombre = self.input_nombre.text()
        tipo = self.input_tipo.currentText()
        nombre_corto = self.input_nombre_corto.text()
        nombre_sin_espacios = self.input_nombre_sin_espacios.text()
        año = self.input_año.value()
        self.ventana_materias.editar_materia(self.param, codigo, nombre, tipo, nombre_corto, nombre_sin_espacios, año)

