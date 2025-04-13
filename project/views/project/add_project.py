from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QComboBox, QCheckBox, QMessageBox
)

from project.models import Project, Client


class AddProjectScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Adicionar Projeto")
        layout = QVBoxLayout()

        # Project Name
        layout.addWidget(QLabel("Nome:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Client Dropdown
        layout.addWidget(QLabel("Cliente:"))
        self.client_dropdown = QComboBox()
        layout.addWidget(self.client_dropdown)

        # Buttons
        self.save_button = QPushButton("Adicionar")
        self.save_button.clicked.connect(self.save_project)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_project_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.load_clients()

    def load_clients(self):
        self.client_dropdown.clear()
        clients = self.session.query(Client).all()
        for client in clients:
            self.client_dropdown.addItem(client.name, client.id)

    def save_project(self):
        name = self.name_input.text().strip()
        client_id = self.client_dropdown.currentData()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Project name cannot be empty.")
            return

        project = Project(name=name, client_id=client_id)
        self.session.add(project)
        self.session.commit()

        QMessageBox.information(self, "Sucesso", "O projeto foi adicionado!")
        self.name_input.clear()
        self.main_window.show_project_screen()

