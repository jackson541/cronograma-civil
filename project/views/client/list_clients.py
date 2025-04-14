from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget,
    QPushButton, QLabel, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt

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
        self.client_list.itemClicked.connect(self.view_edit_client)
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
            item = QListWidgetItem(client.name)
            item.setData(Qt.UserRole, client.id)
            self.client_list.addItem(item)

    def view_edit_client(self, item):
        client_id = item.data(Qt.UserRole)
        self.main_window.show_edit_client_screen(client_id)

