from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget,
    QPushButton, QLabel, QMessageBox
)

from project.models import Client


class ListClientScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Clientes")
        layout = QVBoxLayout()

        self.label = QLabel("Lista de clientes:")
        layout.addWidget(self.label)

        self.client_list = QListWidget()
        layout.addWidget(self.client_list)

        # Add button to open NewClientScreen
        self.new_client_button = QPushButton("Novo cliente")
        self.new_client_button.clicked.connect(self.main_window.show_new_client_screen)
        layout.addWidget(self.new_client_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_project_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.load_clients()

    def load_clients(self):
        self.client_list.clear()
        clients = self.session.query(Client).all()
        for client in clients:
            self.client_list.addItem(f"{client.name}")

