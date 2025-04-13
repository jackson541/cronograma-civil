from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)

from project.models import Client


class NewClientScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Cadastrar Cliente")
        layout = QVBoxLayout()

        self.label = QLabel("Nome:")
        layout.addWidget(self.label)

        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        self.submit_button = QPushButton("Adicionar Cliente")
        self.submit_button.clicked.connect(self.add_client)
        layout.addWidget(self.submit_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_list_client_screen)
        layout.addWidget(self.back_button)

        self.message = QLabel("")
        layout.addWidget(self.message)

        self.setLayout(layout)

    def add_client(self):
        client_name = self.name_input.text().strip()
        if not client_name:
            QMessageBox.warning(self, "Input Error", "Client name cannot be empty.")
            return

        # Check if client already exists
        existing = self.session.query(Client).filter_by(name=client_name).first()
        if existing:
            QMessageBox.information(self, "Duplicate", "Client already exists.")
            return

        # Create and save the client
        new_client = Client(name=client_name)
        self.session.add(new_client)
        self.session.commit()

        self.message.setText(f"Client '{client_name}' added!")
        self.name_input.clear()
