from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QWidget

class VentanaAbrirEncuesta(QMainWindow):
    def __init__(self, main_window, lista_nombres_con_id):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Abrir Encuesta")
        self.setMinimumSize(400, 400)
        self.move((1980-400) // 2, (1080-400) // 2)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for (id, nombre) in lista_nombres_con_id:
            boton_encuesta = QPushButton(nombre)
            boton_encuesta.clicked.connect(lambda checked, id=id: self.abrir_encuesta(id))
            layout.addWidget(boton_encuesta)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrir_encuesta(self, id):
        self.main_window.mostrar_encuesta(id)
